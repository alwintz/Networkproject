import socket

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server running on port {PORT}")
print("Waiting for client...")

client_socket, client_address = server.accept()

username = client_socket.recv(1024).decode()

print(f"{username} connected from {client_address}")

client_socket.send(
    f"Welcome {username}".encode()
)

client_socket.close()
server.close()