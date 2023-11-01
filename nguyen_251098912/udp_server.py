# Assignment: UDP Simple Chat Room - UDP Server Code Implementation

# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need socket, select, time libraries for the client.
#    Feel free to use any libraries as well.
import socket
import threading

# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.
HOST = '127.0.0.1'
PORT = 12345
# Dictionary to store connected clients
clients = {}
# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the server side.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful
# Server configuration
def handle_client(client_socket, client_address, username):
    print(f"{username} has joined!")
    clients[username] = (client_socket, client_address)

    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            if data:
                message = data.decode('utf-8')
                if ':' in message:
                    sender, message = message.split(":", 1)
                    print(f"{sender}: {message}")
                    broadcast_message(f"{sender}: {message}", sender)
        except Exception as e:
            print(e)
            break

    client_socket.close()
    del clients[username]
    print(f"{username} has left.")

def broadcast_message(message, sender):
    for client, (client_socket, client_address) in clients.items():
        if client != sender:
            client_socket.sendto(message.encode('utf-8'), client_address)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"Server is running on {HOST}:{PORT}")

    while True:
        data, addr = server.recvfrom(1024)
        username = data.decode('utf-8').split(":", 1)[0]
        if username not in clients:
            print(f"{username} has joined!")
            clients[username] = (server, addr)
        if ':' in data.decode('utf-8'):
            sender, message = data.decode('utf-8').split(":", 1)
            print(f"{sender}: {message}")
            broadcast_message(f"{sender}: {message}", sender)

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
