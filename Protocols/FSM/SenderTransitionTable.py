from SenderState import SenderState
from Events import Event
class SenderTransitionTable:

    def __init__(self):

        self.transitions = {

            SenderState.READY: {
                Event.SEND: SenderState.SEND_PACKET,
                Event.NO_MORE_DATA: SenderState.FINISHED,
            },

            SenderState.SEND_PACKET: {
                Event.PACKET_SENT: SenderState.WAIT_FOR_ACK,
            },

            SenderState.WAIT_FOR_ACK: {
                Event.ACK: SenderState.READY,
                Event.TIMEOUT: SenderState.RETRANSMIT,
            },

            SenderState.RETRANSMIT: {
                Event.PACKET_SENT: SenderState.WAIT_FOR_ACK,
            },

            SenderState.FINISHED: {
            }
        }

    def next_state(self, current_state, event):
        return self.transitions[current_state][event]