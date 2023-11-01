# Assignment: UDP Simple Chat Room - UDP Client Code Implementation
# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need sys, socket, argparse, select, threading (or _thread) libraries for the client implementation.
#    Feel free to use any libraries as well.
import socket
import sys
import threading

# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.

# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the client side.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
#    - Take into consideration error handling, interrupts,and client shutdown.


def receive_messages(client_socket, username):
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            print(data.decode('utf-8'))
        except OSError as e:
            pass

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    server_address = ('127.0.0.1', 12345)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Create a separate thread for receiving messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client, username))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        message = input()
        if message == "exit":
            break
        message = f"{username}: {message}"  # Include the username in the message
        client.sendto(message.encode('utf-8'), server_address)

if __name__ == "__main__":
    main()
