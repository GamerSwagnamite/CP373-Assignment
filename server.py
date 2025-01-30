import socket
import os
from datetime import datetime
import threading

MAX_CLIENTS = 3  # Limit server to 3 clients
clients = {}  # Dictionary to store active clients

def handle_client(client_socket, client_name, addr):
    global clients
    clients[client_name] = {"start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    print(f"{client_name} connected from {addr}")

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            if data.lower() == "exit":
                print(f"{client_name} disconnected.")
                clients[client_name]["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break

            elif data.lower() == "status":
                # Send active clients
                status = "\n".join(
                    [f"{name}: {info['start_time']} -> {info.get('end_time', 'Active')}" for name, info in clients.items()]
                    )
                client_socket.send(status.encode())

            elif data.lower() == "list":
                # Send list of files
                files = os.listdir("server_files") if os.path.exists("server_files") else []
                file_list = "\n".join(files) if files else "No files available"
                client_socket.send(file_list.encode())

            #elif data.startswith("get "):
                # Handle file transfer

            else:
                # Append "ACK" to message and send it back
                client_socket.send(f"{data} ACK".encode())

        except Exception as e:
            print(f"Error with client {addr}: {e}")
            break

    del clients[client_name]  # Remove from active clients list
    client_socket.close()  # Close connection


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(MAX_CLIENTS)

    print("Server is listening...")

    while True:
        if len(clients) < MAX_CLIENTS:
            client_socket, addr = server_socket.accept()  # Accept client connection
            client_name = f"Client{len(clients) + 1}"
            thread = threading.Thread(target=handle_client, args=(client_socket, client_name, addr))
            thread.start()  # Start a new thread for each client

if __name__ == '__main__':
    start_server()
