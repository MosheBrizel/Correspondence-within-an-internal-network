from tkinter import *
import datetime
import tkinter
import socket
import threading
import time
import json
import datetime

current_time = datetime.datetime.now()

window = Tk()
window.title("message")
window.configure(bg="#F5F5DC")


class First_window:
    def __init__(self):
        # Initializing variables and settings for the client
        self.format_code = 'utf-8'
        self.disconnect = "!Disconnect"
        self.dict_result_thread = {"conn": False}
        self.color = "#F5F5DC"
        self.port = 5050
        self.first_frame = tkinter.Frame(window, bg=self.color)
        self.cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Widgets for the initial connection window
        self.label_waiting = tkinter.Label(self.first_frame, width=30, bg=self.color, font=("Helvetica", 30),
                                           text="connect")
        self.label_ip = tkinter.Label(self.first_frame, width=30, bg=self.color, font=("Helvetica", 30),
                                      text="Enter the ip of the server")
        self.entry_ip = tkinter.Entry(self.first_frame, width=30, font=("Helvetica", 30), justify='center')
        self.entry_ip = tkinter.Entry(self.first_frame, width=30, font=("Helvetica", 30), justify='center')
        self.label_name = tkinter.Label(self.first_frame, width=30, bg=self.color, font=("Helvetica", 30),
                                        text="Enter your name")
        self.entry_name = tkinter.Entry(self.first_frame, width=30, font=("Helvetica", 30), justify='center')
        self.button_start = Button(self.first_frame, fg='black', text="connect", font=("Helvetica", 20), width=28)

    def start(self):
        self.first_frame.pack(padx=20, pady=20)
        self.label_ip.pack()
        self.entry_ip.insert(0, "192.168.")
        self.entry_ip.pack()
        self.label_name.pack()
        self.entry_name.pack()
        self.button_start.configure(command=lambda: self.connect())
        self.button_start.pack(padx=20, pady=20)

    def frame_waiting(self):
        # Function to show the waiting animation in the connect button
        self.button_start["state"] = "disabled"
        self.button_start["disabledforeground"] = "black"

        while self.thread_conn.is_alive() and self.dict_result_thread["conn"] is False:
            self.button_start["text"] = "connect"
            time.sleep(0.5)
            self.button_start["text"] = "connect."
            time.sleep(0.5)
            self.button_start["text"] = "connect.."
            if self.dict_result_thread["conn"]:
                self.button_start["text"] = "connect"
                self.button_start["state"] = "normal"
                if self.dict_result_thread["conn"]:
                    self.first_frame.destroy()
                return
            time.sleep(0.5)
            self.button_start["text"] = "connect..."
            time.sleep(0.5)
        self.button_start["text"] = "connect"
        self.button_start["state"] = "normal"
        if self.dict_result_thread["conn"]:
            self.first_frame.destroy()
        return

    def connect(self):
        # Function to initiate the connection with the server
        ip = self.entry_ip.get()
        self.thread_conn = threading.Thread(target=self.thread_connect, args=(ip,))
        self.thread_conn.start()
        self.thread_waiting = threading.Thread(target=self.frame_waiting)
        self.thread_waiting.start()

    def send_msg(self, addr, msg):
        # Function to send a message to the server
        message_addr = addr.encode(self.format_code)
        msg_length = str(len(message_addr)).encode(self.format_code)
        msg_length += b' ' * (64 - len(msg_length))
        try:
            self.cli.send(msg_length)
            self.cli.send(message_addr)
        except:
            print("error send")
        message = msg.encode(self.format_code)
        msg_length = str(len(message)).encode(self.format_code)
        msg_length += b' ' * (64 - len(msg_length))
        try:
            self.cli.send(msg_length)
            self.cli.send(message)
        except:
            print("error send")

    def thread_connect(self, ip):
        # Function to handle the connection process and notify the result
        try:
            self.cli.connect((ip, self.port))
            time.sleep(4)
            self.dict_result_thread["conn"] = True
            if self.dict_result_thread["conn"] is True:
                self.name = self.entry_name.get()
                self.send_msg("name", self.name)
                second = Second_frame()
                second.start_frame_button()
                second.start()
            return
        except:
            self.label_ip["text"] = "Enter the right ip of the server"
            self.dict_result_thread["conn"] = False
            return


class Second_frame:
    def __init__(self):
        # Initializing variables and settings for the chat window
        self.color = "#F5F5DC"
        self.ip_addr = ""
        self.name_user = ""
        self.format_code = 'utf-8'
        self.disconnect = "!Disconnect"
        self.tk = tkinter
        self.connect = True
        self.list_send_to = []
        self.send_to = "all"
        self.dict_buttons_users = {}
        self.dict_chat = {}
        self.dict_names_users = {}
        self.frame_window = tkinter.Frame(window, bg="#F5F5DC")
        self.frame_window.pack(padx=20, pady=20)
        self.frame_right = tkinter.Frame(self.frame_window, bg="#F5F5DC")
        self.first = First_window()
        self.cli = first.cli

    def start_frame_button(self):
        # Function to create and pack the buttons for users in the chat window
        self.frame_users = tkinter.Frame(self.frame_window, bg="#F5F5DC")
        self.frame_users.pack(side="left")
        for user_ip in self.dict_names_users:
            self.button = Button(self.frame_users, text=self.dict_names_users[user_ip], width=20, height=1, padx=10,
                                 font=("Helvetica", 15))  # done button
            self.button.configure(command=lambda ip=user_ip: self.change_send(ip))
            self.button.pack()
            self.dict_buttons_users[user_ip] = self.button

    def change_send(self, user_ip):
        # Function to change the target user to send messages
        self.send_to = user_ip
        self.label_send_name["text"] = f"send a message to: {self.dict_names_users[self.send_to]}"
        self.text_chat["text"] = self.dict_chat[self.send_to]
        self.dict_buttons_users[user_ip]["font"] = ("Helvetica", 15)

    def show_chat(self):
        # Function to display the chat window with scrollable text area
        self.frame_right.pack(side="right")
        self.box_frame = Frame(self.frame_right)  # the tasks frame
        self.box_frame.pack()
        canvas = Canvas(self.box_frame)  # canvas for scroll bar
        scrollbar = Scrollbar(self.box_frame, orient="vertical", command=canvas.yview)  # scroll bar
        scrollable_frame = Frame(canvas, width=65, height=65)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add widgets to the scrollable frame
        self.text_chat = Label(scrollable_frame, text="", font=("Helvetica", 15))
        self.text_chat.pack()

        # Pack the canvas and scrollbar widgets
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.entry1 = tkinter.Entry(self.frame_right, width=40, justify='left', font=("Helvetica", 15))
        self.entry1.pack()
        self.button_send = Button(self.entry1, text="send", font=("Helvetica", 10))
        self.button_send.configure(command=lambda: self.send_message())
        self.button_send.place(relx=1.0, rely=0.5, anchor='e')

    def start(self):
        # Function to start the chat window
        self.label_name = Label(self.frame_window, text=f"you are connected with the name: {first.name}",
                                font=("Helvetica", 15), bg=self.color)
        self.label_name.pack()
        self.label_send_name = Label(self.frame_window, text=f"send a message to: {self.send_to}",
                                     font=("Helvetica", 15), bg=self.color)
        self.label_send_name.pack()
        self.thread_massage = threading.Thread(target=self.get_massage_server)
        self.thread_massage.start()
        self.show_chat()

    def send_message(self):
        # Function to send a message to the selected user
        msg_send = self.entry1.get()
        self.dict_chat[self.send_to] += f'you {datetime.datetime.now().strftime("%H:%M")}\n' \
                                        f'{self.doun_line(msg_send)}\n'
        self.entry1.delete(0, END)
        self.text_chat["text"] = self.dict_chat[self.send_to]
        self.send_msg(self.send_to, msg_send)

    def doun_line(self, text):
        # Function to format the message text to fit within the text area
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

    def send_msg(self, addr, msg):
        # Function to send a message to the server
        message_addr = addr.encode(self.format_code)
        msg_length = str(len(message_addr)).encode(self.format_code)
        msg_length += b' ' * (64 - len(msg_length))
        try:
            self.cli.send(msg_length)
            self.cli.send(message_addr)
        except:
            print("error send")
        message = msg.encode(self.format_code)
        msg_length = str(len(message)).encode(self.format_code)
        msg_length += b' ' * (64 - len(msg_length))
        try:
            self.cli.send(msg_length)
            self.cli.send(message)
        except:
            print("error send")

    def get_massage_server(self):
        # Function to receive messages from the server
        while True:
            if not self.connect:
                break
            msg_length = self.cli.recv(64).decode(self.format_code)
            if msg_length == '':
                break
            if msg_length:
                msg_length = int(msg_length)
                msg_type = self.cli.recv(msg_length).decode(self.format_code)
                msg_length = self.cli.recv(64).decode(self.format_code)
                msg_length = int(msg_length)
                msg = self.cli.recv(msg_length).decode(self.format_code)

                if msg_type == "all":
                    self.dict_chat["all"] += f"{msg}"
                    if msg_type == self.send_to:
                        self.text_chat["text"] = self.dict_chat[msg_type]
                    else:
                        self.dict_buttons_users[msg_type]["font"] = ("Helvetica", 15, "bold")

                elif msg_type == "update":
                    self.dict_names_users = json.loads(msg)
                    for user in self.dict_names_users:
                        if user not in self.dict_chat:
                            self.dict_chat[user] = ""
                    if self.frame_users:
                        self.frame_users.destroy()
                    self.start_frame_button()

                else:
                    self.dict_chat[msg_type] += f"{self.dict_names_users[msg_type]} " \
                                                f"{datetime.datetime.now().strftime('%H:%M')}\n" \
                                                f"{self.doun_line(msg)}\n"
                    if msg_type == self.send_to:
                        self.text_chat["text"] = self.dict_chat[msg_type]
                    else:
                        self.dict_buttons_users[msg_type]["font"] = ("Helvetica", 15, "bold")
        return


first = First_window()
first.start()
second = Second_frame()

window.mainloop()

# After the main GUI window is closed, send a disconnection message and stop the second thread
first.send_msg(first.disconnect, first.disconnect)
second.connect = False
