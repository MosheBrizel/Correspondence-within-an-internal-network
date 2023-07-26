# Importing required modules
from tkinter import *
from tkinter import messagebox
import datetime
import socket
import threading
import time
import tkinter
import json

# Getting the current time
current_time = datetime.datetime.now()

# Creating the main application window
window = Tk()
window.title("message")
window.configure(bg="#F5F5DC")

# Class to handle the server functionalities
class Frame_server:
    def __init__(self):
        # Initializing variables and settings for the server
        self.list_off = [True]
        self.list_thread = []

        self.address_server = socket.gethostbyname(socket.gethostname())
        self.nameserver = socket.gethostname()
        self.port = 5050
        self.dict_client = {}
        self.dict_names = {"all": "all"}
        self.format_code = 'utf-8'
        self.disconnect = "!Disconnect"
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser.bind((self.address_server, self.port))

        # tkinter settings for GUI
        self.color = "#F5F5DC"
        self.frame_ser = tkinter.Frame(window, bg=self.color)
        self.label_address = Label(self.frame_ser, text=f"the address of the server is {self.address_server}",
                                   font=("Helvetica", 30), bg=self.color)
        self.label_show_clint = Label(self.frame_ser, text=f"all client that connect", font=("Helvetica", 30),
                                      bg=self.color)
        self.frame_names_connect = Frame(self.frame_ser, bg=self.color)
        self.label_clint = Label(self.frame_names_connect, text=f" ", font=("Helvetica", 20),
                                 bg=self.color)

    # Function to send messages to clients
    def send_msg(self, msg, conn, addr_or_type):
        msg_type = f'{addr_or_type}'
        message_type = msg_type.encode(self.format_code)
        msg_length = str(len(message_type)).encode(self.format_code)
        msg_length += b' ' * (64 - len(msg_length))
        conn.send(msg_length)
        conn.send(message_type)

        msg = f'{msg}'
        message = msg.encode(self.format_code)
        msg_length = str(len(message)).encode(self.format_code)
        msg_length += b' ' * (64 - len(msg_length))
        conn.send(msg_length)
        conn.send(message)

    # Function to update the users' list for all connected clients
    def update_users(self):
        json_str = json.dumps(self.dict_names)
        for client in self.dict_client:
            thread_send = threading.Thread(target=self.send_msg, args=(json_str, self.dict_client[client], "update"))
            thread_send.start()
            self.list_thread.append(thread_send)

    # Function to format long messages with word wrapping
    def doun_line(self, text):
        new_str = ""
        word = ""
        counter = 0
        for i in range(len(text)):
            counter += 1
            if text[i] == " ":
                word += text[i]
                if counter > 30:
                    new_str += "\n"
                    counter = 0
                else:
                    new_str += word
                    word = ""
            else:
                word += text[i]
        new_str += word
        return new_str

    # Function to handle receiving and sending messages with a specific client
    def get_client_message(self, conn, addr):
        addr_ip = f"{addr[0]}%{addr[1]}"
        print(f"{addr} Is now connected")
        while self.list_off[0]:
            msg_length = conn.recv(64).decode(self.format_code)

            if msg_length:
                msg_length = int(msg_length)
                msg_addr = conn.recv(msg_length).decode(self.format_code)

                msg_length = conn.recv(64).decode(self.format_code)
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.format_code)
                if msg_addr == "all":  # need to send for all the clients.
                    msg = f"{self.dict_names[addr_ip]} {datetime.datetime.now().strftime('%H:%M')}\n{self.doun_line(msg)}\n"
                    for cli in self.dict_client:
                        print(cli)

                        if addr_ip != cli:
                            self.send_msg(msg, self.dict_client[cli], "all")
                elif msg_addr == self.disconnect:
                    # Handling disconnection of a client
                    conn.close()
                    del self.dict_client[addr_ip]
                    del self.dict_names[addr_ip]
                    self.label_clint["text"] = ""
                    self.show_connect()
                    self.update_users()
                    return
                elif msg_addr == "name":
                    # Setting the name for a client
                    self.dict_names[addr_ip] = (str(msg))
                    self.label_clint["text"] = ""
                    self.show_connect()
                    self.update_users()
                else:
                    # Sending private messages to a specific client
                    self.send_msg(msg, self.dict_client[msg_addr], addr_ip)

        # Closing the connection with a client when the loop exits
        conn.close()
        del self.dict_client[addr]
        del self.dict_names[addr_ip]
        self.label_clint["text"] = ""
        self.show_connect()
        self.update_users()
        return

    # Function to start the server and handle client connections
    def start_server(self):
        self.ser.listen()
        print("listening")
        while self.list_off[0]:
            try:
                conn, addr = self.ser.accept()
                addr_ip = f"{addr[0]}%{addr[1]}"
                self.dict_client[addr_ip] = conn
                thread = threading.Thread(target=self.get_client_message, args=(conn, addr))
                self.list_thread.append(thread)
                thread.start()
                print(f"the num in thread is {threading.active_count() - 1}")
            except:
                print("out listening")

    # Function to display connected clients on the GUI
    def show_connect(self):
        self.frame_names_connect.pack()
        for client in self.dict_names:
            self.label_clint["text"] += f"{self.dict_names[client]}\n"
            self.label_clint.pack(padx=5, pady=5)

    # Function to start the server and display GUI elements
    def start(self):
        thread_server = threading.Thread(target=self.start_server)
        thread_server.start()

        self.list_thread.append(thread_server)

        self.label_address.pack(padx=20, pady=20)
        self.label_show_clint.pack(padx=20, pady=20)
        self.frame_ser.pack(padx=20, pady=20)
        self.show_connect()


# Creating and starting the server instance
star = Frame_server()
star.start()
window.mainloop()

# Stopping the server when the GUI window is closed
star.list_off[0] = False
star.ser.close()
