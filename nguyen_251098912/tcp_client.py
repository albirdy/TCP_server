# Assignment: TCP Simple Chat Room - TCP Client Code Implementation
# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need sys, socket, argparse, select, threading (or _thread) libraries for the client implementation.
#    Feel free to use any libraries as well.
import socket
import sys
import threading
# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.
# Client configuration
HOST = 'localhost'  # Server's IP address
PORT = 12345
# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the client side.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
#    - Take into consideration error handling, interrupts,and client shutdown.
# Function to receive and print messages from the server
def receive_messages():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

# Start a thread to continuously receive and print messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Check if the user provided a name as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python client.py <your_name>")
    sys.exit(1)

# Extract the user's name from the command-line argument
user_name = sys.argv[1]

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Send the user's name to the server
client_socket.send(user_name.encode('utf-8'))

while True:
    message = input("Enter a message: ")
    client_socket.send(message.encode('utf-8'))
