import socket
import threading
from services.user_service import UserService
from services.room_service import RoomService
from services.message_service import MessageService

HOST = "0.0.0.0"
PORT = 5000
MAX_USERS_PER_ROOM = 3

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

rooms = {
    "Room1": [],
    "Room2": []
}

user_rooms = {}

message_history = {
    "Room1": [],
    "Room2": []
}

print(f"Server running on port {PORT}")
print("Waiting for clients...")


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            if message == "SHOW_USERS":
                RoomService.send_users_to_client(
                    rooms,
                    clients,
                    client_socket
                )

            elif message == "SHOW_ROOMS":
                RoomService.send_rooms_to_client(
                    rooms,
                    MAX_USERS_PER_ROOM,
                    client_socket
                )

            elif message.startswith("SWITCH:"):
                room_name = message.split(":", 1)[1]

                success = RoomService.switch_room(
                    rooms,
                    user_rooms,
                    client_socket,
                    room_name,
                    MAX_USERS_PER_ROOM
                )

                if success:
                    MessageService.send_history_to_client(
                        message_history,
                        client_socket,
                        room_name
                    )

            elif message.startswith("HISTORY:"):
                room_name = message.split(":", 1)[1]

                MessageService.send_history_to_client(
                    message_history,
                    client_socket,
                    room_name
                )

            elif message.startswith("CHANGE_USERNAME:"):
                new_username = message.split(":", 1)[1]

                UserService.change_username(
                    clients,
                    client_socket,
                    new_username
                )

            else:
                username = UserService.get_username(
                    clients,
                    client_socket
                )

                MessageService.send_message_to_room(
                    rooms,
                    user_rooms,
                    message_history,
                    username,
                    client_socket,
                    message
                )

        except:
            break

    UserService.remove_client(
        clients,
        rooms,
        user_rooms,
        client_socket
    )


while True:
    client_socket, client_address = server.accept()

    username = client_socket.recv(1024).decode()

    if len(rooms["Room1"]) >= MAX_USERS_PER_ROOM:
        client_socket.send(
            "ERROR: Room1 is full. Try again later.".encode()
        )
        client_socket.close()
        continue

    clients.append({
        "socket": client_socket,
        "username": username,
        "ip": client_address[0],
        "port": client_address[1]
    })

    rooms["Room1"].append(client_socket)
    user_rooms[client_socket] = "Room1"

    print(
        f"{username} connected from "
        f"{client_address[0]}:{client_address[1]}"
    )

    print(f"{username} joined Room1")

    client_socket.send(
        "You joined Room1 by default".encode()
    )

    MessageService.send_history_to_client(
        message_history,
        client_socket,
        "Room1"
    )

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,)
    )

    thread.start()