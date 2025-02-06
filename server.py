# ----------------------------------------------------------------
# CP372 - Computer Networks
# ----------------------------------------------------------------
# Name: Jordan Asmono and Tyler Rizzi
# ID: 210922810 and 169022274
# Email: asmo2810@mylaurier.ca and rizz2274@mylaurier.ca
# Version: 2025-02-04
# ----------------------------------------------------------------
# Assignment 1 - Socket Programming (server.py)
# ----------------------------------------------------------------

# imports
import socket
import os
from datetime import datetime
import threading

# global constants
MAX_CLIENTS = 3     # Limit server to 3 clients
client_cache = {}   # Cache of all clients that have connected to the server
active_clients = {} # Dictionary to store active clients


# handle client function
# infinite while loop run on its own thread when a client connects to the server
# 
# param client_socket - 
# param client_name - the name of the client being handled, formatted as Client<xx>
# param addr - the IP address and port the client is accessing
def handle_client(client_socket, client_name, addr):
    global active_clients, client_cache

    # save client data to our active list and our cache
    active_clients[client_name] = {"start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    client_cache[client_name] = active_clients[client_name]
    print(f"{client_name} connected from {addr}")

    # handling procedures. will run until exit occurs
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # exit condition
            # save the client's exit date + time to the cache
            if data.lower() == "exit":
                print(f"{client_name} disconnected.")
                client_cache[client_name]["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break

            # status condition
            # send over a list of client information stored in the cache
            elif data.lower() == "status":
                # Send active clients
                status = "\n".join(
                    [f"{name}: {info['start_time']} -> {info.get('end_time', 'Active')}" for name, info in client_cache.items()]
                    )
                client_socket.send(status.encode())

            # list condition
            # list all files in the server's repository
            elif data.lower() == "list":
                # Send list of files
                files = os.listdir("server_files") if os.path.exists("server_files") else []
                file_list = "\n".join(files) if files else "No files available"
                client_socket.send(file_list.encode())

            # get condition
            # transfer a file stored in the repository to the client
            elif data.startswith("get "):
                # handshake to confirm that file exists
                filename = data[4:].strip()
                directory = f"server_files/{filename}"
                if os.path.exists(directory) == False:
                    response = "404 Not Found"              # failure condition
                    client_socket.send(response.encode())
                else:
                    response = "200 OK"                     # success condition
                    client_socket.send(response.encode())

                    # send file to client
                    fh = open(directory, "r")
                    lines = fh.readlines()
                    for line in lines:
                        client_socket.send(str(line).encode())
                    client_socket.send(response.encode())

                    # close file because we love resource management
                    fh.close()
                                  

            else:
                # Append "ACK" to message and send it back
                client_socket.send(f"{data} ACK".encode())

        except Exception as e:
            print(f"Error with client {addr}: {e}")
            break

    del active_clients[client_name]  # Remove from active clients list
    client_socket.close()  # Close connection

# start server function
# essentially our main function. sets up the server and separates each client onto a separate thread
def start_server():
    print(f"CP372 - Computer Networks, Winter 2025\nSocket Programming Assignment - server.py\nJordan Asmono and Tyler Rizzi\n")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(MAX_CLIENTS)

    print("Server is listening...")
    while True:
        if len(active_clients) < MAX_CLIENTS:

            # Accept client connection
            client_socket, addr = server_socket.accept()  
            client_name = f"Client{len(client_cache) + 1}"

            # complete the handshake for the client
            handshake = f"Connected to the server as {client_name}. Type 'exit' to disconnect."
            client_socket.send(handshake.encode())

            # Start a new thread for the client
            thread = threading.Thread(target=handle_client, args=(client_socket, client_name, addr))
            thread.start()  

if __name__ == '__main__':
    start_server()
