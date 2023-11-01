# Assignment: TCP Simple Chat Room - TCP Server Code Implementation

# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need socket, threading, select, time libraries for the client.
#    Feel free to use any libraries as well.
import socket
import threading
# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.
# Server configuration
HOST = '0.0.0.0'
PORT = 12345

# List to store connected clients
clients = []
# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the server side.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
# Function to broadcast messages to all clients except the sender
def broadcast(sender_name, message):
    for client_name, client_socket in clients:
        if client_name != sender_name:
            try:
                client_socket.send(f"{sender_name}: {message}".encode('utf-8'))
            except Exception as e:
                remove_client((client_name, client_socket))
                continue

# Function to remove a client from the list
def remove_client(client_info):
    if client_info in clients:
        client_name, client_socket = client_info
        clients.remove(client_info)
        print(f"{client_name} left the chat")
        client_socket.close()



# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Function to handle client connections
def handle_client(client_socket):
    client_name = client_socket.recv(1024).decode('utf-8')
    clients.append((client_name, client_socket))
    print(f"{client_name} joined the chat!")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                remove_client((client_name, client_socket))
                break

            print(f"{client_name}: {message}")
            broadcast(client_name, message)

        except Exception as e:
            print(f"Error: {e}")
            remove_client((client_name, client_socket))
            break


# Main server loop
while True:
    client_socket, client_addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
