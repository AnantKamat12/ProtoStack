from Events import Event
from ReceiverState import ReceiverState


class ReceiverTransitionTable:

    def __init__(self):

        self.transition_table = {

            ReceiverState.WAIT_PACKET: {
                Event.PACKET_RECEIVED: ReceiverState.RECEIVE_PACKET,
            },

            ReceiverState.RECEIVE_PACKET: {
                Event.CRC_PASS: ReceiverState.SEND_ACK,
                Event.CRC_FAIL: ReceiverState.DISCARD,
            },

            ReceiverState.SEND_ACK: {
                Event.ACK_SENT: ReceiverState.WAIT_PACKET,
            },

            ReceiverState.DISCARD: {
                Event.PACKET_DISCARDED: ReceiverState.WAIT_PACKET,
            }

        }

    def next_state(self, current_state, event):
        return self.transition_table[current_state][event]