import sys
import os


from Segmenter import Segmenter
from PacketSender import PacketSender
from VirtualChannel import VirtualChannel
from Packets import Packet


def run_pipeline_test():
    print("=" * 60)
    print("🚀 STARTING PROTOSTACK END-TO-END PIPELINE TEST")
    print("=" * 60)

    # 1. SETUP PIPELINE & CONFIGURATION
    raw_message = "Hello, ProtoStack! Testing the continuous byte stream."
    payload_size = 8  # Small payload size to force multiple packets
    
    # Initialize VirtualChannel with 0% drop rate for baseline validation
    channel = VirtualChannel(capacity=2048, byte_drop_rate=0.0)
    
    print(f"\n[1] Original Message: '{raw_message}'")
    print(f"    Message Size: {len(raw_message)} bytes")
    print(f"    Payload Size per Packet: {payload_size} bytes")

    # 2. SEGMENTATION (App Data -> Packet Train)
    data_bytes = raw_message.encode("utf-8")
    packet_train = Segmenter.segment(data_bytes, payload_size=payload_size)
    
    print(f"\n[2] Segmented into {len(packet_train)} packets.")
    for i, pkt in enumerate(packet_train):
        print(f"    📦 Packet {i}: Seq={pkt.seq_num}")

    # 3. TRANSMISSION (Packet Train -> Raw Byte Stream -> Channel FIFO)
    bytes_sent = PacketSender.send_packet_train(packet_train)
    print(f"\n[3] PacketSender serialized packets and transmitted {bytes_sent} bytes.")
    print(f"    Channel FIFO Current Queue Size: {len(channel.queue)} bytes")

    # 4. RECEIVER & DESERIALIZATION (Channel FIFO -> Stream -> Packets)
    HEADER_SIZE = 4
    CRC_SIZE = 4
    received_packets = []

    print("\n[4] Receiver pulling raw bytes off VirtualChannel FIFO...")

    while channel.has_data():
        # Step A: Read fixed-length Header bytes
        header_bytes = channel.read(HEADER_SIZE)
        if len(header_bytes) < HEADER_SIZE:
            print("    ⚠️ Incomplete header received. Wire stream truncated.")
            break

        # Extract payload length byte from header
        payload_len = header_bytes[3]

        # Step B: Read exact variable Payload + fixed CRC32 Trailer bytes
        remaining_bytes_needed = payload_len + CRC_SIZE
        rest_bytes = channel.read(remaining_bytes_needed)

        if len(rest_bytes) < remaining_bytes_needed:
            print("    ⚠️ Incomplete payload/CRC received. Wire stream truncated.")
            break

        # Step C: Reconstruct full raw frame bytes & deserialize
        full_frame_bytes = header_bytes + rest_bytes
        
        try:
            pkt = Packet.deserialize_packet(full_frame_bytes)
            received_packets.append(pkt)
            print(f"    ✅ Deserialized & Validated Packet Seq {pkt.seq_num} (CRC PASS)")
        except ValueError as e:
            print(f"    ❌ Packet Deserialization/CRC Error: {e}")

    # 5. REASSEMBLY & INTEGRITY CHECK (Packets -> Reconstructed Data)
    print(f"\n[5] Reassembling {len(received_packets)} received packets...")
    reconstructed_bytes = Segmenter.reassemble(received_packets)
    reconstructed_message = reconstructed_bytes.decode("utf-8")

    print("\n" + "=" * 60)
    print(f"Original:      '{raw_message}'")
    print(f"Reconstructed: '{reconstructed_message}'")
    print("=" * 60)

    # Integrity Assertion
    assert raw_message == reconstructed_message, "❌ Test Failed: Reconstructed message does not match original!"
    print("🎉 SUCCESS: Pipeline test passed with 100% data integrity!\n")


if __name__ == "__main__":
    run_pipeline_test()