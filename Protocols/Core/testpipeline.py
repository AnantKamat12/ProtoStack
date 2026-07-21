from Segmenter import Segmenter
from PacketSender import PacketSender
from VirtualChannel import VirtualChannel
from Packets import Packet


def run_pipeline_test():
    print("=" * 60)
    print("🚀 STARTING PROTOSTACK END-TO-END PIPELINE TEST")
    print("=" * 60)

    raw_message = "Hello, ProtoStack! Testing the continuous byte stream."
    payload_size = 8

    channel = VirtualChannel(byte_drop_rate=0,bit_flip_rate=0.0)

    print(f"\nOriginal Message: '{raw_message}'")
    print(f"Message Size: {len(raw_message)} bytes")
    print(f"Payload Size per Packet: {payload_size} bytes")

    data_bytes = raw_message.encode("utf-8")
    packet_train = Segmenter.segment(data_bytes, payload_size=payload_size)

    print(f"\nSegmented into {len(packet_train)} packets.")

    for packet in packet_train:
        print(f"Packet Seq={packet.seq_num}")

    bytes_sent = PacketSender.send_packet_train(packet_train, channel)

    print(f"\nTransmitted {bytes_sent} bytes.")
    print(f"Channel Queue Size: {channel.available()} bytes")

    HEADER_SIZE = 4
    CRC_SIZE = 4

    received_packets = []

    while channel.available():

        header = channel.read(HEADER_SIZE)

        if len(header) < HEADER_SIZE:
            break

        payload_length = header[3]

        body = channel.read(payload_length + CRC_SIZE)

        if len(body) < payload_length + CRC_SIZE:
            break

        frame = header + body

        try:
            packet = Packet.deserialize_packet(frame)
            received_packets.append(packet)
            print(f"Received Packet Seq={packet.seq_num}")

        except ValueError as e:
            print(e)

    reconstructed = Segmenter.reassemble(received_packets)
    reconstructed_message = reconstructed.decode('utf-8')
    print("\n" + "=" * 60)
    print(f"Original      : {raw_message}")
    print(f"Reconstructed : {reconstructed_message}")
    print("=" * 60)

    assert raw_message == reconstructed_message

    print("Pipeline Test Passed")


if __name__ == "__main__":
    run_pipeline_test()