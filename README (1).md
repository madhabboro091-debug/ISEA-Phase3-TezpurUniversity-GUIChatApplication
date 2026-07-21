# GUI Chat Application

A multi-client GUI-based chat application built using Python and TCP sockets. The application provides secure user authentication, real-time messaging, performance evaluation, and network traffic analysis while demonstrating scalability and reliability improvements.

---

## Overview

This project implements a client-server chat system with a graphical user interface. It supports multiple concurrent clients, secure user authentication, broadcast and private messaging, configurable server settings, and performance monitoring. The application is designed to evaluate how the system behaves under different client loads while maintaining reliable communication.

---

## Features

- GUI-based chat client using Tkinter
- Multi-client TCP server
- Secure user authentication using SHA-256 password hashing
- Broadcast messaging
- Private messaging
- Online users list
- Chat history logging
- Security event logging
- Session timeout for inactive users
- Configurable server parameters using `config.json`
- Performance evaluation and CSV logging
- Delay and throughput graph generation
- Network traffic analysis using Wireshark

---

## Technologies Used

- Python 3
- TCP Sockets
- Tkinter
- Mininet
- Wireshark
- Pandas
- Matplotlib

---

## Project Structure

```
.
├── server.py
├── client_gui.py
├── config.json
├── users.json
├── chat_history.csv
├── performance_results.csv
├── graph_generator.py
├── graphs/
│   ├── delay_graph.png
│   └── throughput_graph.png
├── screenshots/
├── README.md
└── report.pdf
```

---

## Prerequisites

Install the required Python packages:

```bash
sudo apt install python3-pandas python3-matplotlib
```

Ensure the following software is available:

- Python 3.x
- Mininet
- Wireshark

---

## Network Topology

The application was tested using Mininet with a single-switch topology.

```bash
sudo mn --topo single,11
```

Host allocation:

- **h1** – Server
- **h2–h11** – Clients

Open terminals for all hosts:

```bash
xterm h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11
```

---

## Running the Application

### Start the Server

On **h1**:

```bash
python3 server.py
```

### Start the Clients

On each client host:

```bash
python3 client_gui.py
```

Authenticate using the credentials defined in `users.json`.

---

## Functionalities

The application supports the following operations:

- User authentication
- Broadcast messaging
- Private messaging
- Viewing online users
- User logout
- Session timeout
- Chat history logging
- Performance monitoring

---

## Performance Evaluation

The application was evaluated using the following metrics:

- Average message delay
- Message throughput
- Concurrent client scalability

Experiments were conducted with:

- 5 concurrent clients
- 8 concurrent clients
- 10 concurrent clients

Performance results are stored in:

```
performance_results.csv
```

Graphs can be generated using:

```bash
python3 graph_generator.py
```

Generated output:

- `graphs/delay_graph.png`
- `graphs/throughput_graph.png`

---

## Wireshark Analysis

Network communication was captured and analyzed using Wireshark to observe:

- TCP three-way handshake
- Client authentication
- Broadcast messaging
- Private messaging
- Client disconnection

---

## Improvements

The project introduces several software quality improvements while preserving the existing communication protocol:

- External configuration using `config.json`
- Improved exception handling
- Automatic cleanup of disconnected clients
- Session timeout management
- Performance logging
- Scalability testing with multiple concurrent clients
- Delay and throughput visualization

---

## Future Enhancements

Possible future improvements include:

- End-to-end message encryption
- File sharing
- Group chat support
- Voice and video communication
- Database-backed user management
- Message delivery acknowledgements
- Docker-based deployment

---

## License

This project is intended for educational and learning purposes.
