# protocol/core/segmenter.py
from typing import List
from Packets import Packet  


class Segmenter:
    """
    Segmentation and Reassembly (SAR) Engine.
    
    Splits large byte arrays into a train of fixed-payload Packet objects
    (Segmentation) and stitches received Packets back into a raw byte stream
    (Reassembly).
    """

    @staticmethod
    def segment(raw_data: bytes, payload_size: int, packet_type: int = 1) -> List[Packet]:
        """
        Slices raw application data into a sequence (train) of Packet objects.
        """
        if payload_size <= 0:
            raise ValueError("payload_size must be greater than 0!")

        packet_train: List[Packet] = []
        seq_num = 0

        for offset in range(0, len(raw_data), payload_size):
            payload_chunk = raw_data[offset : offset + payload_size]

            pkt = Packet(
                packet_type=packet_type,
                seq_num=seq_num,
                payload=payload_chunk
            )
            packet_train.append(pkt)
            seq_num += 1

        return packet_train

    @staticmethod
    def reassemble(packet_train: List[Packet]) -> bytes:
        """
        Stitches an in-order or out-of-order train of Packets back into 
        the original raw application data stream.
        """
        # Sort packets by sequence number in case of out-of-order arrival
        sorted_packets = sorted(packet_train, key=lambda p: p.seq_num)

        # Concatenate all payloads
        return b"".join(pkt.payload for pkt in sorted_packets)