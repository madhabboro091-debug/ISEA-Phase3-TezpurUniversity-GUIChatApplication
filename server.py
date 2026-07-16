import json
import hashlib
import re
import socket
import threading
import csv
import time
from datetime import datetime, timedelta

HOST = "10.0.0.1"
PORT = 5000

clients = []
usernames = {}
client_ips = {}
client_ports = {}
login_times = {}
status = {}
last_activity = {}
logged_in_users = set()

failed_attempts = {}

blocked_until = {}

SESSION_TIMEOUT = 300

USER_FILE = "users.json"

SECURITY_LOG = "security_log.txt"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

users_db = load_users()
def verify_user(username, password):
    print("Checking user:", username)

    if username not in users_db:
        print("User not found")
        return False

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    print("Stored hash    :", users_db[username])
    print("Computed hash  :", password_hash)

    return users_db[username] == password_hash

def write_security_log(event):
    with open(SECURITY_LOG, "a") as f:
        f.write(f"{datetime.now()} - {event}\n")

message_count = 0
broadcast_count = 0
private_count = 0
start_time = None
end_time = None

HISTORY_FILE = "chat_history.csv"
RESULT_FILE = "performance_results.csv"

with open(HISTORY_FILE,"w",newline="") as f:
	csv.writer(f).writerow(["time","sender","receiver","type","message"])

with open(RESULT_FILE,"w",newline="") as f:
	csv.writer(f).writerow(["online_clients","total_messages","broadcast_messages","private_messages","average_delay_ms","throughput_msg_per_sec"])

def save_history(sender,receiver,msg_type,message):
    with open(HISTORY_FILE,"a",newline="") as f:
        csv.writer(f).writerow([datetime.now().strftime("%H:%M:%S"),sender,receiver,msg_type,message])

def send_history(client):
    try:
        with open(HISTORY_FILE) as f:
            rows=f.readlines()[1:]
        client.send(b"--- Last 5 Messages ---\n")
        for r in rows[-5:]:
            client.send(r.strip().encode()+b"\n")
        client.send(b"------------------------\n")
    except:
        pass
def broadcast(message):
    print("Broadcasting:", repr(message))
    print("Clients:", len(clients))

    for c in clients:
        try:
            c.send((message + "\n").encode())
            print("Sent to:", usernames.get(c, "Unknown"))
        except Exception as e:
            print("Broadcast error:", e)
def update_online_users():

    users = ",".join(usernames.values())
    print("Updating users:", users)

    for client in clients:
        try:
            client.send(f"USERS:{users}\n".encode())
            print("Sent USERS to", usernames.get(client))
        except Exception as e:
            print("User update error:", e)
def send_online_users(client):
    names=""
    for c in clients:
        names = usernames[c] if names=="" else names+","+usernames[c]
    client.send(names.encode())

def send_private(sender_client,receiver,message):
    global private_count,message_count
    sender=usernames[sender_client]
    message_count += 1
    if message_count==50:
        write_results()
    for c in clients:
        if usernames[c]==receiver:
            c.send(f"[PRIVATE] {sender}: {message}".encode())
            sender_client.send(f"[To {receiver}] {message}".encode())
            private_count += 1
            save_history(sender,receiver,"Private",message)
            return
    sender_client.send(b"User not found.")

def write_results():
    global message_count, broadcast_count, private_count, start_time,end_time
    if start_time is None or end_time is None or message_count==0:
        return
    total=max(end_time-start_time,0.001)
    avg=(total/message_count)*1000
    throughput=message_count/total
    with open(RESULT_FILE,"a",newline="") as f:
        csv.writer(f).writerow([len(clients),message_count,broadcast_count,private_count,round(avg,2),round(throughput,2)])
        print("Performance Saved")

    # Reset for next experiment
    message_count = 0
    broadcast_count = 0
    private_count = 0
    start_time = None
    end_time = None

def handle_client(client,addr):
    global start_time,end_time,message_count,broadcast_count

    credentials = client.recv(1024).decode()
    print("Received:", credentials)
    try:
        username, password = credentials.split(":", 1)
        if username in blocked_until:
            if datetime.now() < blocked_until[username]:
                client.send(b"ACCOUNT_BLOCKED")
                client.close()
                return
            else:
                del blocked_until[username]
                failed_attempts[username] = 0

        print("Username:", username)
        print("Password:", password)
    except ValueError:
        write_security_log(f"{username} LOGIN FAILED")
        client.send(b"LOGIN_FAILED")
       
        client.close()
        return
    if not verify_user(username, password):

        failed_attempts[username] = failed_attempts.get(username, 0) + 1

        print(username, "failed", failed_attempts[username], "times")

        if failed_attempts[username] >= 5:

            blocked_until[username] = datetime.now() + timedelta(seconds=60)

            failed_attempts[username] = 0
            write_security_log(f"{username} ACCOUNT BLOCKED")
            client.send(b"ACCOUNT_BLOCKED")

        else:

            client.send(b"LOGIN_FAILED")

        client.close()
        return 

    if username in logged_in_users:
        client.send(b"ALREADY_LOGGED_IN")
        client.close()
        return

    logged_in_users.add(username)
   
    client.send(b"LOGIN_SUCCESS")
    write_security_log(f"{username} LOGIN SUCCESS")
    failed_attempts[username] = 0

    clients.append(client)
    usernames[client]=username
    client_ips[client]=addr[0]
    client_ports[client]=addr[1]
    login_times[client]=datetime.now().strftime("%H:%M:%S")
    last_activity[client] = time.time() 
    status[client]="Online"

    print(f"{username} connected from {addr[0]}:{addr[1]}")
    send_history(client)
    broadcast(f"[SERVER] {username} joined the chat.")
    update_online_users()
    client.settimeout(1)
    
    while True:
        try:

            data = client.recv(1024).decode()
 
            if not data:
                break

            last_activity[client] = time.time()

        except socket.timeout:

            if time.time() - last_activity[client] > 300:   # Use 300 later
                write_security_log(f"{username} SESSION TIMEOUT")
                client.send(b"SESSION_TIMEOUT\n")
                break

            continue

        except:
            break
          
        if data == "/logout":
            write_security_log(f"{username} LOGOUT")
            client.send(b"LOGOUT_SUCCESS")
            break
   
        if len(data) > 500:
            client.send(b"Message rejected: Too long.\n")
            continue

        if start_time is None:
            start_time=time.time()
           
        end_time=time.time()

        if data=="/list":
            send_online_users(client)

        elif data.startswith("/msg "):
            p=data.split(" ",2)
            if len(p)==3:
                send_private(client,p[1],p[2])

        else:
             message_count += 1
             broadcast_count += 1
             text=f"[{username}] {data}"
             print(text)
             broadcast(text)
             save_history(username,"ALL","Broadcast",data)
          
             if message_count == 50:
                    write_results()


    broadcast(f"[SERVER] {username} left the chat.")

    if client in clients:
        clients.remove(client)

    usernames.pop(client,None)
    client_ips.pop(client,None)
    client_ports.pop(client,None)
    login_times.pop(client,None)
    last_activity.pop(client, None)
    status.pop(client,None)
    update_online_users()
    logged_in_users.discard(username)
    write_security_log(f"{username} LOGOUT") 
    client.close()
    
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

print("Server Started...")
print("Waiting for clients...")

while True:
    client,addr=server.accept()
    threading.Thread(target=handle_client,args=(client,addr),daemon=True).start()
