from collections import deque
import random


class VirtualChannel:

    def __init__(self, capacity=2048, byte_drop_rate=0.0,bit_flip_rate:float=0):
        self._capacity = capacity
        self._byte_drop_rate = byte_drop_rate
        self._bit_flip_rate=bit_flip_rate
        self._queue = deque()

    def configure(self, capacity=None, byte_drop_rate=None):
        if capacity is not None:
            self._capacity = capacity

        if byte_drop_rate is not None:
            self._byte_drop_rate = byte_drop_rate

    def send(self, data: bytes):

        if len(self._queue) + len(data) > self._capacity:
            raise BufferError("Virtual Channel Overflow")

        for byte in data:

            if random.random() >= self._byte_drop_rate:

                if random.random() < self._bit_flip_rate:

                    bit = random.randint(0, 7)
                    byte ^= (1 << bit)

                self._queue.append(byte)

                

    def read(self, n: int):

        out = bytearray()

        while self._queue and len(out) < n:
            out.append(self._queue.popleft())#we will pop by FIFO ,the buffer can hold upto self._capacity bytes

        return bytes(out)

    def available(self):
        return len(self._queue)

    def clear(self):
        self._queue.clear()