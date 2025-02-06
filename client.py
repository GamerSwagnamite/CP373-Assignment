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

# imports
import os
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

        # exit condition
        if message.lower() == "exit":
            break

        # get condition
        elif message.startswith("get "):
            # handshake to confirm that file exists. response is either "200 OK" or "404 Not Found"
            response = client_socket.recv(1024).decode()
            print(f"From Server: {response}")

            # file successfully found
            if response == "200 OK":
                # check if directory exists; otherwise, make the folder
                if os.path.exists("client_files") == False:
                    os.makedirs("client_files")
                
                # open the file in the client_files folder
                filename = message[4:].strip()
                directory = f"client_files/{filename}" 
                fh = open(directory, "wb")

                # write to file until "200 OK" is resent
                data = client_socket.recv(1024)
                while data != b"200 OK":
                    fh.write(data)
                    data = client_socket.recv(1024)
                
                # close file because resource management is important :)
                fh.close()

        # general print statement for other conditions
        else:
            response = client_socket.recv(1024).decode()
            print(f"From Server: {response}")



    client_socket.close()

if __name__ == '__main__':
    start_client()
