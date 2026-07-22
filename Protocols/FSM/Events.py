from enum import Enum, auto

class Event(Enum):

    # Sender events
    SEND = auto()
    PACKET_SENT = auto()
    ACK = auto()
    TIMEOUT = auto()
    NO_MORE_DATA = auto()

    # Receiver events
    PACKET_RECEIVED = auto()
    CRC_PASS = auto()
    CRC_FAIL = auto()
    ACK_SENT = auto()
    PACKET_DISCARDED = auto()