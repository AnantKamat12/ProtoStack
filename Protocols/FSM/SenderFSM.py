from SenderTransitionTable import *
from FSM import *
class ReceiverFSM(FSM):

    def __init__(self):
        super().__init__(
            SenderState.READY,
            SenderTransitionTable()
        )