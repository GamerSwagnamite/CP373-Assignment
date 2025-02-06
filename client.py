# ----------------------------------------------------------------
# CP372 - Computer Networks
# ----------------------------------------------------------------
# Name: Jordan Asmono and Tyler Rizzi
# ID: 210922810 and 169022274
# Email: asmo2810@mylaurier.ca and rizz2274@mylaurier.ca
# Version: 2025-02-04
# ----------------------------------------------------------------
# Assignment 1 - Socket Programming (client.py)
# ----------------------------------------------------------------

import socket

def start_client():
    print(f"CP372 - Computer Networks, Winter 2025\nSocket Programming Assignment - client.py\nJordan Asmono and Tyler Rizzi\n")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Connect to the server

    # handshake to verify that a client has successfully connected to the server
    handshake = client_socket.recv(1024).decode()
    print(f"{handshake}")

    # print("Connected to server! Type 'exit' to disconnect.")

    while True:
        message = input("Enter message ('status', 'list', 'get <filename>', 'exit'): ")
        client_socket.send(message.encode())

        response = client_socket.recv(1024).decode()
        print(f"From Server: {response}")

        if message.lower() == "exit":
            break

    client_socket.close()

if __name__ == '__main__':
    start_client()
