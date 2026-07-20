from VirtualChannel import channel

class PacketSender:
    @classmethod
    def send_packet_train(cls, packet_train: list) -> int:
        """
        Serializes a list of Packet objects into a continuous raw byte stream
        and pushes them into the global VirtualChannel instance.
        Returns the number of bytes transmitted.
        """
        # 1. Serialize all packet objects into continuous raw bytes
        raw_stream = b"".join(pkt.serialize_packet() for pkt in packet_train)
        
        # 2. Push continuous byte stream into the single channel instance
        bytes_sent = channel.send(raw_stream)

        return bytes_sent