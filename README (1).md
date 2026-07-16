# Assignment 7 – Secure Multi-Client GUI Chat Application

## Student Information

- **Name:** Madhab Boro
- **Roll No.:** CSB24055

---

# Objective

The objective of this assignment is to develop a secure multi-client GUI-based chat application using Python socket programming. The application implements user authentication, session management, security mechanisms, and real-time communication while analyzing TCP traffic using Wireshark.

---

# Features Implemented

## Authentication
- Username and password-based login
- Passwords stored securely using SHA-256 hashing
- User authentication using `users.json`

## Security Features
- Duplicate login prevention
- Account blocking after multiple failed login attempts
- Input validation
- Message length validation
- Security event logging

## Session Management
- Automatic session timeout due to inactivity
- Manual logout using the Disconnect button
- Online users list
- Session timeout notification

## Chat Features
- Broadcast messaging
- Private messaging using `/msg`
- Display online users using `/list`
- Chat history storage

## Logging and Performance
- Security log generation
- Chat history logging
- Performance statistics generation

---

# Software Requirements

- Ubuntu Linux
- Python 3
- Mininet
- Wireshark
- Tkinter
- VirtualBox

---

# Project Structure

```text
Assignment_7/
│
├── server.py
├── client_gui.py
├── users.json
├── README.md
├── report.pdf
├── security_log.txt
├── chat_history.csv
├── performance_results.csv
└── screenshots/
    ├── login.png
    ├── online_users.png
    ├── broadcast.png
    ├── private_message.png
    ├── duplicate_login.png
    ├── invalid_login.png
    ├── account_blocked.png
    ├── session_timeout.png
    ├── security_log.png
    └── wireshark/
        ├── handshake.png
        ├── login_packet.png
        ├── broadcast_packet.png
        ├── private_packet.png
        ├── timeout_packet.png
        └── connection_close.png
```

---

# Network Topology

```text
                   +-------------+
                   |  Switch s1  |
                   +-------------+
            /        |      |        \
         h1         h2     h3       h4      h5

h1 : Chat Server
h2 : Client 1
h3 : Client 2
h4 : Client 3
h5 : Client 4
```

---

# Execution Steps

## 1. Start Mininet

```bash
sudo mn -c
sudo mn --topo single,5
```

Open terminals for all hosts:

```bash
xterm h1 h2 h3 h4 h5
```

## 2. Start the Server

On **h1**:

```bash
cd ~/Assignment_7
python3 server.py
```

## 3. Start the Clients

On **h2**, **h3**, **h4**, and **h5**:

```bash
cd ~/Assignment_7
python3 client_gui.py
```

## 4. Login

Example credentials:

```text
Username: Madhab
Password: password123
```

## 5. Chat Commands

Broadcast message:

```text
Hello Everyone
```

Private message:

```text
/msg Masum Hello
```

View online users:

```text
/list
```

Logout:

```text
/logout
```

---

# Sample Screenshots

The repository includes screenshots demonstrating:

- Server startup
- Successful login
- Online users list
- Broadcast messaging
- Private messaging
- Duplicate login prevention
- Invalid login attempt
- Account blocking after repeated failed login attempts
- Session timeout
- Security log
- Wireshark TCP handshake
- Wireshark message transmission
- TCP connection termination

---

# Wireshark Analysis

Wireshark was used to monitor and analyze TCP communication between the clients and server. The captured packets include:

- TCP Three-Way Handshake
- Login authentication packets
- Broadcast message packets
- Private message packets
- Online user update packets
- Session timeout packets
- TCP connection termination (FIN/ACK)

---

# Generated Files

The application generates the following files:

- `chat_history.csv`
- `performance_results.csv`
- `security_log.txt`

These files record chat history, performance metrics, and security-related events generated during execution.

---

# Brief Description of the Implementation

The application is developed using Python socket programming and multithreading to support multiple simultaneous client connections. A Tkinter-based graphical user interface provides an intuitive chat experience. User authentication is secured using SHA-256 password hashing, while additional security mechanisms such as duplicate login prevention, account blocking after repeated failed login attempts, input validation, and automatic session timeout improve the overall security of the application.

The server manages client connections, broadcasts messages, supports private messaging, maintains the online user list, stores chat history, records performance statistics, and logs security events. Wireshark was used to verify TCP communication and analyze network traffic during testing.

---

# Conclusion

This project demonstrates the implementation of a secure multi-client GUI chat application using TCP socket programming. It integrates networking, multithreading, GUI development, authentication, session management, and network traffic analysis to provide a reliable and secure client-server communication system.
