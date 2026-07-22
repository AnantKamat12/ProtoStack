from SenderFSM import SenderFSM
from ReceiverFSM import ReceiverFSM
from Events import Event


class TestFSM:

    @staticmethod
    def testsfsm(sfsm):

        print("===== Sender FSM =====")
        print("Event--->State")

        transitions = {}

        transitions["Initial State"] = sfsm.get_state()

        sfsm.handle(Event.SEND)
        transitions["After SEND"] = sfsm.get_state()

        sfsm.handle(Event.PACKET_SENT)
        transitions["After PACKET_SENT"] = sfsm.get_state()

        sfsm.handle(Event.ACK)
        transitions["After ACK"] = sfsm.get_state()

        for event, state in transitions.items():
            print(f"{event} -> {state}")

        return transitions

    @staticmethod
    def testrfsm(rfsm):

        print("\n===== Receiver FSM =====")
        print("Event--->State")

        transitions = {}

        transitions["Initial State"] = rfsm.get_state()

        rfsm.handle(Event.PACKET_RECEIVED)
        transitions["After PACKET_RECEIVED"] = rfsm.get_state()

        rfsm.handle(Event.CRC_PASS)
        transitions["After CRC_PASS"] = rfsm.get_state()

        rfsm.handle(Event.ACK_SENT)
        transitions["After ACK_SENT"] = rfsm.get_state()

        for event, state in transitions.items():
            print(f"{event} -> {state}")

        return transitions


if __name__ == "__main__":

    sfsm = SenderFSM()
    rfsm = ReceiverFSM()

    TestFSM.testsfsm(sfsm)
    TestFSM.testrfsm(rfsm)