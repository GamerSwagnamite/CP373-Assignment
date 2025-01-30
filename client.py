import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Connect to the server

    print("Connected to server! Type 'exit' to disconnect.")

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
