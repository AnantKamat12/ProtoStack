# Packet Format

## Overview

The `Packet` class represents the basic unit of communication used throughout ProtoStack. Every packet transmitted between two virtual devices follows the same binary structure.

```
+------------+---------------+------------+----------------------+
| PacketType | SequenceNumber| PayloadLen |       Payload        |
+------------+---------------+------------+----------------------+
|   1 Byte   |    2 Bytes    |   1 Byte   | Variable Length      |
+------------+---------------+------------+----------------------+
```

The header occupies **4 bytes**, followed by a payload of variable length.

---

# Header Layout

The header is defined using Python's `struct` module:

```python
HEADER_FORMAT = ">BHB"
```

The format string is interpreted as follows:

| Symbol | Meaning                 | Size    |
| ------ | ----------------------- | ------- |
| `>`    | Big-endian byte order   | —       |
| `B`    | Unsigned 8-bit integer  | 1 byte  |
| `H`    | Unsigned 16-bit integer | 2 bytes |
| `B`    | Unsigned 8-bit integer  | 1 byte  |

Therefore,

```
HEADER_SIZE = 1 + 2 + 1 = 4 bytes
```

---

# Packet Structure

```
Byte Offset

0        1        3        4
+--------+--------+--------+-------------------+
| Type   | SeqNum | Length | Payload           |
+--------+--------+--------+-------------------+
 1 byte   2 bytes  1 byte    Variable
```

---

# Example Packet

Suppose we create the following packet:

```python
packet = Packet(
    packet_type=1,
    seq_num=100,
    payload=b"Hello"
)
```

The payload is

```
Hello
```

whose ASCII values are

| Character | Hex |
| --------- | --- |
| H         | 48  |
| e         | 65  |
| l         | 6C  |
| l         | 6C  |
| o         | 6F  |

The payload length is

```
5 bytes
```

---

## Serialization

The packet is serialized into

```
b'\x01\x00d\x05Hello'
```

Hex representation

```
01 00 64 05 48 65 6C 6C 6F
```

---

# Breaking Down Each Byte

## Byte 0 — Packet Type

```
01
```

Decimal

```
1
```

Meaning

```
DATA Packet
```

The packet type identifies the purpose of the packet.

Example mapping

| Value | Meaning |
| ----- | ------- |
| 1     | DATA    |
| 2     | ACK     |
| 3     | NACK    |
| 4     | CONTROL |

---

## Bytes 1–2 — Sequence Number

```
00 64
```

Because the packet uses **Big-Endian** ordering,

```
00 64
```

is interpreted as

```
0x0064
```

which equals

```
100
```

The sequence number uniquely identifies the packet.

It enables protocols to

* detect duplicate packets
* acknowledge received packets
* perform retransmissions
* preserve ordering

---

## Byte 3 — Payload Length

```
05
```

Decimal

```
5
```

The receiver now knows that the next **5 bytes** belong to the payload.

---

## Remaining Bytes — Payload

```
48 65 6C 6C 6F
```

ASCII decoding gives

```
Hello
```

The payload is application data and is interpreted by higher-level protocols.

---

# Complete Packet

```
01 | 00 64 | 05 | 48 65 6C 6C 6F
```

or

```
+------+-----------+---------+----------------------+
|Type  |Sequence # | Length  | Payload              |
+------+-----------+---------+----------------------+
| 01   | 00 64     |   05    | H e l l o            |
+------+-----------+---------+----------------------+
```

---

# Serialization Process

```
Packet Object

packet_type = 1
sequence = 100
length = 5
payload = Hello

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

        ▼

Final Packet

01 00 64 05 48 65 6C 6C 6F
```

---

# Deserialization Process

When a receiver obtains the byte stream

```
01 00 64 05 48 65 6C 6C 6F
```

it performs the following steps:

1. Read the first 4 bytes as the header.
2. Decode the header using `struct.unpack(">BHB")`.
3. Extract:

   * Packet Type = 1
   * Sequence Number = 100
   * Payload Length = 5
4. Read the next 5 bytes as the payload.
5. Construct a new `Packet` object.

The reconstructed object is equivalent to the original packet before transmission.

---

# Why Big-Endian?

ProtoStack uses Big-Endian (network byte order) because it is the conventional byte ordering used by Internet protocols such as IPv4, TCP, and UDP. Using a consistent endianness ensures that multi-byte fields like sequence numbers are interpreted identically across different machines.

---

# Future Extensions

This packet format is intentionally minimal and serves as the foundation for the framework. As ProtoStack evolves, additional header fields may be introduced, such as:

* CRC / Checksum
* Source Address
* Destination Address
* Flags
* Protocol Identifier
* Timestamp
* Priority
* Fragment Information

These additions can be made while preserving the same serialization and deserialization principles.
