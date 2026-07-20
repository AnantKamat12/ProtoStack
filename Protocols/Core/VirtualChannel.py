import random
from collections import deque

class VirtualChannel:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, capacity: int = 2048, byte_drop_rate: float = 0.0):
        # Prevent re-initializing the singleton on subsequent calls
        if self._initialized:
            return
        
        self.capacity = capacity
        self.byte_drop_rate = byte_drop_rate
        self.queue = deque()  # FIFO holding raw bytes
        self._initialized = True

    def send(self, data: bytes) -> int:
        """Pushes raw continuous bytes onto the wire FIFO buffer."""
        if len(self.queue) + len(data) > self.capacity:
            raise BufferError("[Channel] ⚠️ Overflow! FIFO buffer full.")

        bytes_sent = 0
        for byte in data:
            if random.random() >= self.byte_drop_rate:
                self.queue.append(byte)
                bytes_sent += 1
            else:
                print(f"[Channel] ⚠️ Dropped byte 0x{byte:02X} on wire")
        return bytes_sent

    def read(self, num_bytes: int) -> bytes:
        """Pulls up to `num_bytes` from the FIFO buffer."""
        read_data = bytearray()
        while self.queue and len(read_data) < num_bytes:
            read_data.append(self.queue.popleft())
        return bytes(read_data)

    def has_data(self) -> bool:
        return len(self.queue) > 0

    def clear(self):
        """Empties the FIFO buffer between test runs."""
        self.queue.clear()


# Single global instance will be created when file is imported
channel = VirtualChannel()