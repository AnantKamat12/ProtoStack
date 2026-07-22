from abc import ABC

class FSM(ABC):

    def __init__(self, initial_state, transition_table):
        self.state = initial_state
        self.transition_table = transition_table

    def handle(self, event):
        self.state = self.transition_table.next_state(
            self.state,
            event
        )
        return self.state

   