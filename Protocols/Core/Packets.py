import struct

class Packet:
    # Format string layout: 
    # '>' '<'<means Big-Endian, Little-Endian 

    # ENDIANNESS EXAMPLE (Using 32-bit Hex Value: 0x12345678)
    # ==============================================================================

    # --- BIG-ENDIAN ---
    #
    # Memory Address  |  Byte Stored  |  Description
    # -------------------------------------------------------------
    # 1000            |  12           |  Most Significant Byte (MSB)
    # 1001            |  34           |  
    # 1002            |  56           |  
    # 1003            |  78           |  Least Significant Byte (LSB)
    # --- LITTLE-ENDIAN ---
    # Memory Address  |  Byte Stored  |  Description
    # -------------------------------------------------------------
    # 1000            |  78           |  Least Significant Byte (LSB)
    # 1001            |  56           |  
    # 1002            |  34           |  
    # 1003            |  12           |  Most Significant Byte (MSB)

    # ==============================================================================

    # 'B' = Type (1 byte), 'H' = Seq Num (2 bytes), 'B' = Length (1 byte)
    HEADER_FORMAT = ">BHB" 
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT) # This will equal 4 bytes

    def __init__(self, packet_type: int, seq_num: int, payload: bytes):
        self.packet_type = packet_type  # e.g., 1 for DATA, 2 for ACK
        self.seq_num = seq_num          # Frame sequence tracker
        self.payload = payload          # The raw actual message bytes
        self.length = len(payload)      # Dynamic size of the payload

    def serialize(self) -> bytes:
        """Converts the packet object into a raw binary stream to send over the 'wire'."""
        # 1. Pack the header variables into their 4-byte structural layout
        header_bytes = struct.pack(
            self.HEADER_FORMAT, 
            self.packet_type, 
            self.seq_num, 
            self.length
        )
        # 2. Append the payload bytes directly after the header
        return header_bytes + self.payload

    @classmethod
    def deserialize(cls, raw_bytes: bytes):
        """Takes a raw binary stream off the 'wire' and reconstructs the Packet object."""
        if len(raw_bytes) < cls.HEADER_SIZE:
            raise ValueError("Data stream too short to contain a valid header!")

        # 1. Slice out the first 4 bytes and unpack them using our format definition
        header_part = raw_bytes[:cls.HEADER_SIZE]
        packet_type, seq_num, length = struct.unpack(cls.HEADER_FORMAT, header_part)

        # 2. Extract the remaining bytes belonging to the payload
        payload_part = raw_bytes[cls.HEADER_SIZE : cls.HEADER_SIZE + length]

        return cls(packet_type, seq_num, payload_part)
if __name__=="__main__":
    Packet=Packet()
