from ReceiverTransitionTable import *
from FSM import *
class ReceiverFSM(FSM):

    def __init__(self):
        super().__init__(
            ReceiverState.WAIT_PACKET,
            ReceiverTransitionTable()
        )