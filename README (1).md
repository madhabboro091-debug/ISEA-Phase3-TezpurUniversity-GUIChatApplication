# GUI-Based Multi-Client Chat Application Using TCP

## Overview

This project implements a GUI-based multi-client chat application using Python and the Tkinter library. The application uses TCP socket programming to enable reliable communication between multiple clients connected to a central server. The graphical interface provides a user-friendly environment for chatting while demonstrating event-driven programming and multithreading.

---

## Objective

The objective of this project is to develop a graphical multi-client chat application that demonstrates:

- GUI programming using Tkinter
- TCP socket communication
- Event-driven programming
- Multithreading
- Client-server architecture
- Real-time messaging between multiple users

---

## Features

- Graphical Login Window
- Graphical Chat Interface
- Multiple Client Support
- Broadcast Messaging
- Private Messaging
- Join Notifications
- Leave Notifications
- Chat History Logging
- Performance Logging
- Background Message Receiving Thread
- User-Friendly Interface

---

## Software Requirements

- Ubuntu Linux
- Python 3
- Tkinter
- Mininet
- Wireshark

---

## Project Structure

```
.
├── server.py
├── client_gui.py
├── chat_history.csv
├── performance_results.csv
├── screenshots/
├── README.md
└── report.pdf
```

---

## Network Topology

```
             Mininet

             h1
          Chat Server
               |
 ---------------------------------
 |        |        |             |
h2       h3       h4            h5

Client A Client B Client C Client D
```

Topology Creation:

```bash
sudo mn --topo single,5
```

---

## How to Run

### Step 1

Start Mininet

```bash
sudo mn --topo single,5
```

### Step 2

Open terminals

```bash
xterm h1 h2 h3 h4 h5
```

### Step 3

Run the server on **h1**

```bash
python3 server.py
```

### Step 4

Run the GUI client on each client host

```bash
python3 client_gui.py
```

### Step 5

Login using different usernames and start chatting.

---

## GUI Components Used

- Tk
- Frame
- Label
- Entry
- Button
- Listbox
- ScrolledText
- Messagebox
- Status Label

---

## Functionalities

- Client Login
- Real-Time Chat
- Broadcast Messages
- Private Messages
- Join Notifications
- Leave Notifications
- Chat History Storage
- Performance Statistics
- Responsive GUI using Background Threads

---

## Testing

The application was tested using Mininet with one server and multiple clients.

The following scenarios were successfully verified:

- Client Connection
- Multiple Client Communication
- Broadcast Messaging
- Private Messaging
- Client Join
- Client Leave
- GUI Responsiveness

---

## Wireshark Verification

Traffic was captured using the following filter:

```text
tcp.port == 5000
```

The following were verified:

- TCP Three-Way Handshake
- Broadcast Message Transmission
- Private Message Transmission
- TCP Connection Termination

---

## Screenshots

The `screenshots/` directory contains:

- Login Window
- Successful Connection
- Main Chat Window
- Broadcast Messaging
- Private Messaging
- User Joining
- User Leaving
- Wireshark Connection
- Wireshark Broadcast
- Wireshark Private Message
- Wireshark Disconnect

---

## Technologies Used

- Python
- Tkinter
- Socket Programming
- Threading
- Mininet
- Wireshark

---

## Conclusion

This project demonstrates the implementation of a GUI-based multi-client chat application using TCP socket programming. The application successfully integrates graphical user interface development with networking concepts, allowing multiple users to communicate efficiently through a responsive and user-friendly chat system.
