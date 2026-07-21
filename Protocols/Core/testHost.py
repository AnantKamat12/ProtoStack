from Host import Host
from VirtualChannel import VirtualChannel
from Packets import Packet


def main():

    # Shared communication channel
    channel = VirtualChannel(
        byte_drop_rate=0.0,
        bit_flip_rate=0.001
    )

    # Sender
    host1 = Host(
        data="Hello, ProtoStack!",
        payload_size=5,
        channel=channel,
        HEADER_SIZE=Packet.HEADER_SIZE,
        CRC_SIZE=Packet.TRAILER_SIZE
    )

    # Receiver
    host2 = Host(
        data="",
        payload_size=5,
        channel=channel,
        HEADER_SIZE=Packet.HEADER_SIZE,
        CRC_SIZE=Packet.TRAILER_SIZE
    )

    sent_packets = host1.transmit()
    received_packets = host2.receive()

    Host.compare(sent_packets, received_packets)


if __name__ == "__main__":
    main()