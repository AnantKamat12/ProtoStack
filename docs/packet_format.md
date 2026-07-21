# Baseline Packet Format

## Overview

The `Packet` class is ProtoStack's **baseline packet implementation**. It inherits from the abstract `AbsPacket` interface and provides a simple, generic framing format used throughout the initial versions of the framework.

```python
from AbsPacket import AbsPacket

class Packet(AbsPacket):
    ...
```

This packet is **not intended to represent any specific real-world protocol** such as Ethernet, IPv4, TCP, UART, or UFS. Instead, it serves as a reference implementation that demonstrates the fundamental concepts shared by most communication protocols:

- Structured packet headers
- Variable-length payloads
- Binary serialization and deserialization
- Sequence numbering
- Packet type identification
- Payload length encoding
- CRC-based integrity verification

Protocol-specific packet formats introduced later in ProtoStack will inherit from `AbsPacket` and implement their own serialization logic while exposing the same common interface.

---

# Packet Hierarchy

```
                  AbsPacket
                      ▲
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
   Packet      EthernetPacket     IPv4Packet
                                      │
                                      ▼
                                 TCPPacket

      ▼
 UARTFrame

      ▼
 UPIUPacket
```

The current `Packet` implementation acts as the default packet format used by the framework's communication pipeline.

---

# Packet Structure

Every baseline packet consists of a **4-byte header**, followed by a variable-length payload and a CRC32 trailer.

```
+------------+---------------+------------+----------------------+-------------+
| PacketType | SequenceNumber| PayloadLen |       Payload        |    CRC32    |
+------------+---------------+------------+----------------------+-------------+
|   1 Byte   |    2 Bytes    |   1 Byte   | Variable Length      |   4 Bytes   |
+------------+---------------+------------+----------------------+-------------+
```

---

# Header Layout

The header is defined using Python's `struct` module.

```python
HEADER_FORMAT = ">BHB"
```

The format string is interpreted as follows.

| Symbol | Meaning                 | Size    |
| ------- | ----------------------- | ------- |
| `>`     | Big-endian byte order   | —       |
| `B`     | Unsigned 8-bit integer  | 1 byte  |
| `H`     | Unsigned 16-bit integer | 2 bytes |
| `B`     | Unsigned 8-bit integer  | 1 byte  |

Therefore,

```
HEADER_SIZE = 4 bytes
```

---

# Packet Layout

```
Byte Offset

0        1        3        4
+--------+--------+--------+-------------------+-------------+
| Type   | SeqNum | Length | Payload           | CRC32       |
+--------+--------+--------+-------------------+-------------+
 1 byte   2 bytes  1 byte    Variable             4 bytes
```

---

# Example Packet

Suppose we construct the following packet.

```python
packet = Packet(
    packet_type=1,
    seq_num=100,
    payload=b"Hello"
)
```

The payload contains

```
Hello
```

whose ASCII values are

| Character | Hex |
| --------- | --- |
| H | 48 |
| e | 65 |
| l | 6C |
| l | 6C |
| o | 6F |

Payload length

```
5 bytes
```

---

# Serialization

The packet header is generated using

```python
struct.pack(">BHB", packet_type, seq_num, payload_length)
```

which produces

```
01 00 64 05
```

The payload is then appended

```
48 65 6C 6C 6F
```

CRC32 is computed over

```
Header + Payload
```

and appended as the trailer.

The final transmitted frame therefore has the form

```
01 00 64 05
48 65 6C 6C 6F
CRC CRC CRC CRC
```

or

```
+------+-----------+---------+----------------------+-------------+
|Type  |Sequence # | Length  | Payload              | CRC32       |
+------+-----------+---------+----------------------+-------------+
| 01   | 00 64     |   05    | H e l l o            | 4 bytes     |
+------+-----------+---------+----------------------+-------------+
```

---

# Serialization Pipeline

```
Packet Object

packet_type = 1
sequence    = 100
length      = 5
payload      = Hello

        │

        ▼

struct.pack(">BHB")

        │

        ▼

Header

01 00 64 05

        │

Append Payload

48 65 6C 6C 6F

        │

Compute CRC32

        │

Append Trailer

        ▼

Serialized Packet
```

---

# Deserialization Pipeline

When the receiver obtains a serialized packet, it performs the following operations.

1. Read the fixed-size header.
2. Decode the header using `struct.unpack(">BHB")`.
3. Extract the packet metadata.
4. Read the payload using the encoded payload length.
5. Verify the CRC32.
6. Reconstruct the `Packet` object.

The reconstructed object is functionally identical to the packet prior to transmission.

---

# Why Big-Endian?

ProtoStack adopts **Big-Endian (network byte order)** for the baseline packet because it is the convention used by Internet protocols such as IPv4, TCP, and UDP.

Using a consistent byte ordering ensures that multi-byte fields are interpreted identically across different architectures.

---

# Relationship to Future Protocols

The baseline `Packet` is intentionally simple.

Future protocol implementations will inherit from `AbsPacket` and define their own binary layouts while remaining compatible with the common packet interface.

Examples include

- Ethernet frames
- IPv4 packets
- TCP segments
- UART frames
- SPI frames
- I²C frames
- SCSI command packets
- UFS UPIUs

Each protocol may introduce fields such as

- Source and destination addresses
- Port numbers
- Flags
- Checksums
- Transaction identifiers
- Flow-control information
- Fragmentation metadata
- Timing information

without affecting the common abstractions provided by `AbsPacket`.