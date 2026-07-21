from Segmenter import Segmenter
from PacketSender import PacketSender
from VirtualChannel import VirtualChannel
from Packets import Packet
from Convert import Convert


class Host:

    def __init__(self, data: str, payload_size, channel, HEADER_SIZE, CRC_SIZE):
        self.data = data
        self.payload_size = payload_size
        self.channel = channel
        self.header_size = HEADER_SIZE
        self.crc_size = CRC_SIZE

    def transmit(self):

        data_bytes = self.data.encode("utf-8")

        packet_train = Segmenter.segment(
            data_bytes,
            payload_size=self.payload_size
        )

        print(f"\nSegmented into {len(packet_train)} packets.")

        for packet in packet_train:
            print(f"Packet Seq={packet.seq_num}")

        bytes_sent = PacketSender.send_packet_train(
            packet_train,
            self.channel
        )

        print(f"\nTransmitted {bytes_sent} bytes.")
        print(f"Channel Queue Size: {self.channel.available()} bytes")

        return packet_train

    def receive(self):

        self.received_packets = []

        while self.channel.available():

            header = self.channel.read(self.header_size)

            if len(header) < self.header_size:
                break

            payload_length = header[3]

            body = self.channel.read(payload_length + self.crc_size)

            if len(body) < payload_length + self.crc_size:
                break

            frame = header + body

            try:
                packet = Packet.deserialize_packet(frame)
                self.received_packets.append(packet)
                print(f"Received Packet Seq={packet.seq_num}")

            except ValueError as e:
                print("The packet couldn't be received.")
                print(e)

        return self.received_packets

    @staticmethod
    def compare(packet_train, received_packets):

        if len(received_packets) != len(packet_train):
            print(
                f"Packets Sent     : {len(packet_train)}\n"
                f"Packets Received : {len(received_packets)}"
            )

        sent_data = Segmenter.reassemble(packet_train)
        received_data = Segmenter.reassemble(received_packets)

        if sent_data == received_data:
            print("\nSUCCESS: Packets were received correctly.")
            return True

        print("\nERROR: Data mismatch!")

        print("\nSent:")
        print(sent_data)

        print("\nReceived:")
        print(received_data)

        print("\nSent (hex):")
        print(sent_data.hex())

        print("\nReceived (hex):")
        print(received_data.hex())

        return False