class PacketSender:

    @staticmethod
    def send_packet_train(packet_train, channel):

        raw_stream = b"".join(
            packet.serialize_packet()
            for packet in packet_train
        )

        channel.send(raw_stream)

        return len(raw_stream)