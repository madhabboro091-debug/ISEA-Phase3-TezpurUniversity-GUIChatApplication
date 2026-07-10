import socket
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

SERVER_IP = "10.0.0.1"

PORT = 5000

client = None


class LoginWindow:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("TCP Chat Login")
        self.root.geometry("400x320")
        self.root.resizable(False, False)

        tk.Label(
            self.root,
            text="GUI Chat Application",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Label(self.root, text="Username").pack()

        self.username = tk.Entry(self.root, width=30)
        self.username.pack(pady=5)

        tk.Label(self.root, text="Password (Optional)").pack()

        self.password = tk.Entry(self.root, show="*", width=30)
        self.password.pack(pady=5)

        self.status = tk.Label(
            self.root,
            text="Not Connected",
            fg="red"
        )

        self.status.pack(pady=5)

        tk.Button(
           self.root,
           text="Connect",
           width=15,
           command=self.connect
       ).pack(pady=10)

        print("Creating Connect button")
        self.root.mainloop()

    def connect(self):
        print("Connect button clicked")
        global client

        username = self.username.get().strip()

        if username == "":
            messagebox.showerror(
                "Error",
                "Username cannot be empty."
            )
            return

        try:

            client = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            client.connect((SERVER_IP, PORT))

            client.send(username.encode())

            self.status.config(
                text="Connected",
                fg="green"
            )

            self.root.destroy()

            ChatWindow(client, username)

        except Exception as e:

            messagebox.showerror(
                "Connection Error",
                str(e)
            )
class ChatWindow:

    def __init__(self, client_socket, username):

        self.client = client_socket
        self.username = username

        self.root = tk.Tk()
        self.root.title(f"TCP Chat - {username}")
        self.root.geometry("850x550")
        self.root.resizable(False, False)

        # ---------------- Top Frame ----------------

        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=5)

        tk.Label(
            top_frame,
            text=f"Logged in as: {username}",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=10)

        self.status = tk.Label(
            top_frame,
            text="Connected",
            fg="green",
            font=("Arial", 11, "bold")
        )

        self.status.pack(side="right", padx=10)

        # ---------------- Middle Frame ----------------

        middle = tk.Frame(self.root)
        middle.pack(fill="both", expand=True)

        # -------- Online Users --------

        left = tk.Frame(middle)

        left.pack(
            side="left",
            fill="y",
            padx=10
        )

        tk.Label(
            left,
            text="Online Users",
            font=("Arial", 11, "bold")
        ).pack()

        self.user_list = tk.Listbox(
            left,
            width=20,
            height=20
        )

        self.user_list.pack()

        # -------- Chat Area --------

        right = tk.Frame(middle)

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.chat_area = ScrolledText(
            right,
            width=70,
            height=25,
            state="disabled"
        )

        self.chat_area.pack(
            padx=5,
            pady=5
        )

        # ---------------- Bottom Frame ----------------

        bottom = tk.Frame(self.root)
        bottom.pack(fill="x", pady=10)

        self.message_entry = tk.Entry(
            bottom,
            width=60
        )

        self.message_entry.pack(
            side="left",
            padx=5
        )

        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        tk.Button(
            bottom,
            text="Send",
            width=10,
            command=self.send_message
        ).pack(side="left", padx=5)

        tk.Button(
            bottom,
            text="Disconnect",
            width=12,
            command=self.disconnect
        ).pack(side="left", padx=5)

        # Start receiving thread

        thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )

        thread.start()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.disconnect
        )

        self.root.mainloop()
    def receive_messages(self):

        while True:

            try:

                message = self.client.recv(1024).decode()

                if not message:
                    break

                # Online users update
                if message.startswith("USERS:"):

                    users = message.replace("USERS:", "").split(",")

                    self.user_list.delete(0, tk.END)

                    for user in users:
                        if user.strip():
                            self.user_list.insert(tk.END, user.strip())

                    continue

                self.chat_area.config(state="normal")

                self.chat_area.insert(
                    tk.END,
                    message + "\n"
                )

                self.chat_area.see(tk.END)

                self.chat_area.config(state="disabled")

            except:
                break


    def send_message(self):

        message = self.message_entry.get().strip()

        if message == "":
            return

        try:

            self.client.send(message.encode())

        except:

            messagebox.showerror(
                "Error",
                "Unable to send message."
            )

        self.message_entry.delete(0, tk.END)


    def disconnect(self):

        try:

            self.client.close()

        except:
            pass

        self.status.config(
            text="Disconnected",
            fg="red"
        )

        self.root.destroy()


# ---------------- Main ----------------

if __name__ == "__main__":

    LoginWindow()
