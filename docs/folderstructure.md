ProtoStack/
│
├── README.md
├── pyproject.toml
├── Dockerfile
├── requirements.txt
│
├── docs/
│ ├── architecture.md
│ ├── protocol_design.md
│ ├── packet_format.md
│ └── diagrams/
│
├── protocol/
│ │
│ ├── core/
│ │ ├── packet.py
│ │ ├── serializer.py
│ │ ├── checksum.py
│ │ ├── event.py
│ │ ├── timer.py
│ │ ├── ring_buffer.py
│ │ ├── logger.py
│ │ └── config.py
│ │
│ ├── fsm/
│ │ ├── state.py
│ │ ├── state_machine.py
│ │ └── transitions.py
│ │
│ ├── link/
│ │ ├── uart.py
│ │ ├── spi.py
│ │ ├── i2c.py
│ │ └── ethernet.py
│ │
│ ├── network/
│ │ ├── ipv4.py
│ │ └── arp.py
│ │
│ ├── transport/
│ │ ├── udp.py
│ │ ├── tcp.py
│ │ └── tcp_fsm.py
│ │
│ ├── storage/
│ │ ├── scsi.py
│ │ ├── upiu.py
│ │ ├── ufs.py
│ │ └── ufs_fsm.py
│ │
│ ├── simulator/
│ │ ├── channel.py
│ │ ├── latency.py
│ │ ├── packet_loss.py
│ │ ├── corruption.py
│ │ └── virtual_device.py
│ │
│ └── cli/
│ └── main.py
│
├── tests/
│
└── examples/
