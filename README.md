# Correspondence-within-an-internal-network
This code implements a basic chat application using Tkinter for GUI. The server supports multiple clients concurrently using threads. Clients can connect to the server by providing their name and the server's IP. Messages can be sent to all clients or specific clients. Note: further enhancements and error handling might be necessary.
# Chat Application 

This is a simple chat application built with Python and Tkinter. It allows multiple clients to connect to a central server and chat in both group and private messages.

## Features

- Client can connect to server by IP address
- Clients are identified by unique name
- Group chat visible to all connected clients
- Private 1-on-1 chatting between clients 
- Server shows currently connected clients
- Messages handled by separate client and server threads
- Client can scroll through message history

## Usage 

### Server

Run `server.py` to start the server:

`python server tk.py`

Server will display its IP address for clients to connect to. 

### Client

Run `client_tk.py` and enter:

- Server IP address
- Desired user name

Start chatting in group or private messages.

## Code Structure

**Server**

- `server.py` - Main server script
- `server_gui.py` - Tkinter GUI code for server 
- `server_utils.py` - Helper functions for messaging, clients list etc.

**Client**

- `client.py` - Main client script
- `client_gui.py` - Tkinter GUI code for client
- `client_utils.py` - Helper functions for messaging, threading etc.  

Key classes:

- `Server` - Main server class with sockets, threads etc. 
- `Client` - Main client class for connecting and chatting
