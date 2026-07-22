from enum import Enum, auto
class ReceiverState(Enum):
    WAIT_PACKET = auto()
    RECEIVE_PACKET = auto()
    SEND_ACK = auto()
    DISCARD = auto()