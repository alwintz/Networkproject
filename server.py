import socket
import threading
from services.user_service import UserService

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            username = UserService.get_username(
                clients,
                client_socket
            )

            print(f"{username}: {message}")

        except:
            break

    UserService.remove_client(
        clients,
        client_socket
    )

while True:

    client_socket, client_address = server.accept()

    username = client_socket.recv(1024).decode()

    clients.append({
        "socket": client_socket,
        "username": username,
        "ip": client_address[0],
        "port": client_address[1]
    })

    print(f"{username} connected")

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,)
    )

    thread.start()