from VirtualChannel import VirtualChannel
print(__file__)
def run_test():
    # Instantiate channel in test script
    chan = VirtualChannel(byte_drop_rate=0.1)
    
    chan.send(b"This is test channel")
    print("Buffer length:", len(chan.queue))
    
    received = chan.read(100)
    print("Read bytes:", received)

if __name__ == "__main__":
    run_test()