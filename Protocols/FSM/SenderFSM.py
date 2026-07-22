from SenderTransitionTable import *
from FSM import *
class SenderFSM(FSM):

    def __init__(self):
        super().__init__(
            SenderState.READY,
            SenderTransitionTable()
        )