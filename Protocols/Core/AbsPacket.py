from abc import ABC, abstractmethod


class AbsPacket(ABC):

    @abstractmethod
    def serialize_packet(self) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def deserialize_packet(cls, raw_bytes: bytes):
        pass