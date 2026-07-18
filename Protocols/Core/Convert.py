import struct as st
#class implementing coversions
class Convert():
    def __init__(self):
        pass
    @classmethod
    def LE(cls,value):
        val=st.pack('<i',value)
        #do val.hex() otherwise it will return a string b'C\x00\x00\x00'
        return val.hex()
    @classmethod
    def BE(cls,value):
        val=st.pack('>i',value)
        return val.hex()
    @classmethod
    def BE2LE(cls,value):
        num=st.unpack('>i',value)[0]
        print(num)
        val=st.pack('<i',num)
        return val.hex()
    @classmethod
    def LE2BE(cls,value):
        num=st.unpack('<i',value)[0]
        val=st.pack('>i',num)
        return val.hex()

if __name__=='__main__':
    val=Convert.LE(0Xa)
    print(val)
    val=Convert.BE(0Xa)
    print(val)
    val=Convert.BE2LE(b'\x12\x34\x56\x78')
    print(val)
    val=Convert.LE2BE(b'\x78\x56\x34\x12')
    print(val)


    

