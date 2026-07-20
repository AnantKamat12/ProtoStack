import struct
import zlib
#This packet will be common for most of protocals
class Packet:
 
    # 'B' = Type (1 byte), 'H' = Seq Num (2 bytes), 'B' = Length (1 byte)
    HEADER_FORMAT = ">BHB" 
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT) # This will equal 4 bytes
    TRAILER_FORMAT = ">I"
    TRAILER_SIZE = struct.calcsize(TRAILER_FORMAT)#32 bits ,4 bytes
    def __init__(self, packet_type: int, seq_num: int, payload: bytes):
        self.packet_type = packet_type  # Ex:1 for DATA, 2 for ACK
        self.seq_num = seq_num          # Frame sequence tracker. seq_num will go in header_bytes:
        self.payload = payload          # The raw actual messgse bytes(bytes in the packet)
        self.length = len(payload)      # Dynamic size of the payloads
        self.payload_len = len(payload)

    def serialize_packet(self) -> bytes:
        """Converts the packet object into a raw binary stream to send over the 'wire'."""
        # 1. Pack the header variables into their 4-byte structural layout
        header_bytes = struct.pack(
            self.HEADER_FORMAT, 
            self.packet_type, 
            self.seq_num, 
            self.length
        )
        self.header_bytes=header_bytes
        body=header_bytes+self.payload
        self.body=body
        crc_val = zlib.crc32(body)
        trailer_bytes = struct.pack(self.TRAILER_FORMAT, crc_val)
        self.trailer=trailer_bytes

        # 2. Append the payload bytes directly after the header
        return (body+trailer_bytes)
    

    @classmethod
    def deserialize_packet(cls, raw_bytes: bytes):
        """Takes a raw binary stream off the 'wire' and reconstructs the Packet object."""
        if len(raw_bytes) < cls.HEADER_SIZE:
            raise ValueError("Data stream too short to contain a valid header!")

        # 1. Slice out the first 4 bytes and unpack them using our format definition
        header_part = raw_bytes[:cls.HEADER_SIZE]
        body_part = raw_bytes[:-cls.TRAILER_SIZE]#header+payload
        trailer_part=raw_bytes[-cls.TRAILER_SIZE:]
        packet_type, seq_num, length = struct.unpack(cls.HEADER_FORMAT, header_part)
        received_crc = struct.unpack(cls.TRAILER_FORMAT, trailer_part)[0]
        expected_crc = zlib.crc32(body_part)
        if received_crc != expected_crc:
            raise ValueError(f"CRC Mismatch! Corrupted Frame. Expected {hex(expected_crc)}, got {hex(received_crc)}")
        # 2. Extract the remaining bytes belonging to the payload
        payload_part = raw_bytes[cls.HEADER_SIZE : cls.HEADER_SIZE + length]
        #return the new packet object

        return cls(packet_type, seq_num, payload_part)
    def check_crc(self):
        header_part = self.header_bytes
        body_part = self.body
        trailer_part=self.trailer
        received_crc = struct.unpack(self.TRAILER_FORMAT, trailer_part)[0]
        expected_crc = zlib.crc32(body_part)
        if received_crc != expected_crc:
            print(f"The CRC check failed: expected={expected_crc} and received={received_crc}")
        else:
            print("Packet has Passed the CRC Check!")

        

        
if __name__ == "__main__":

    print("\n========== Example 1 : DATA Packet ==========\n")

    packet = Packet(
        packet_type=1,
        seq_num=100,
        payload=b"Hello"
    )
    print(type(packet))

    raw = packet.serialize_packet()
    print(type(raw))#print(help(raw))
    print("serialize_packetd Bytes:")
    print(raw)
    print(raw.hex())

    recovered = Packet.deserialize_packet(raw)
    print(type(recovered))
    packet.check_crc()
    print("\nRecovered Packet")
    print("Type    :", recovered.packet_type)
    print("Seq Num :", recovered.seq_num,"asci value of 'd':",100 , "i.e 0x0064")
    print("Length  :", recovered.length)
    print("Payload :", recovered.payload)



