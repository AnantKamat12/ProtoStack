from enum import Enum, auto
class SenderState(Enum):
    READY = auto()# Python assigns 1
    SEND_PACKET = auto()# Python assigns 2
    WAIT_FOR_ACK = auto()
    RETRANSMIT = auto()
    FINISHED = auto()
