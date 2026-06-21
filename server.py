import socket
import threading
from services.user_service import UserService
from services.room_service import RoomService
from services.message_service import MessageService

# ============================================================
# SERVER CONFIGURATION
# ============================================================
# HOST = 0.0.0.0 means listen on all network interfaces
# PORT identifies the chat service
# MAX_USERS_PER_ROOM limits the number of users per room

HOST = "0.0.0.0"
PORT = 5000
MAX_USERS_PER_ROOM = 10


# ============================================================
# CREATE TCP SERVER SOCKET
# ============================================================
# AF_INET     -> IPv4 addressing
# SOCK_STREAM -> TCP protocol
#
# TCP provides:
# - Reliable delivery
# - Ordered packets
# - Error detection
# - Connection-oriented communication

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Turn on re-use of port
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                  
# Bind server to IP address and port
server.bind((HOST, PORT))

# Start listening for client connections
server.listen()


# ============================================================
# DATA STRUCTURES
# ============================================================
# clients         -> connected users
# rooms           -> room membership
# user_rooms      -> current room of each client
# message_history -> stores messages for each room
# private_history -> stores private messages

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

private_history = {}

print(f"Server running on port {PORT}")
print("Waiting for clients...")

# ============================================================
# CLIENT HANDLER THREAD
# ============================================================
# Receives clients and adds it to room 1 by default after authentication is a success
# Processes all commands received from a client.
#
# Supported commands:
# SHOW_USERS
# SHOW_ROOMS
# SWITCH: |<room_name>
# HISTORY: |<room_name>
# CHANGE_USERNAME:<new_username>
# private|<username>|<message>
# privHistory: |<username>

#<Any other message> - broadcast to current room

#authenticate and return the username
def authenticate(client_socket):
    auth_message = client_socket.recv(1024).decode()

    if not auth_message:
        return None
    action, username, password = auth_message.split("|")

    if action == "signup":
        response = UserService.signUp(username, password)
        client_socket.send(response.encode())

        return None   

    elif action == "login":
        response = UserService.LogIn(username, password)
        client_socket.send(response.encode())

        if response == "SUCCESS":
            return username   

        return None 
    
def handle_client(client_socket, client_address):
    username = None

    while username is None:
        username = authenticate(client_socket)

       
   # adding each client connection after auth is a success
    clients.append({                 
        "socket": client_socket,
        "username": username,
        "ip": client_address[0],
        "port": client_address[1],
        "user_id": UserService.registered_users[username]['id']
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

            elif message.startswith("SWITCH: |"):
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

            elif message.startswith("HISTORY: |"):
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

            elif message.startswith("private: |"):
              sender_username = UserService.get_username (clients, client_socket)

              parts = message.split("|")
              recv_username = parts[1]
              msg = parts[2]

              try:
               MessageService.send_private_message(sender_username, client_socket, recv_username, private_history,
                                                    msg, clients)
              except Exception as e:
               print(f"PRIV_MSG ERROR: {e}")
            
            elif message.startswith("privHistory: |"):
              parts = message.split("|")
              target_username = parts[1]

              try:
                MessageService.send_priv_history_to_client(
                    private_history,
                    client_socket,
                    target_username,
                    clients
                )
              except Exception as e:
               print(f"PRIV_HISTORY ERROR: {e}")

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

    # when the while True loop stops remove the client from clients and close connection
    UserService.remove_client(
        clients,
        rooms,
        user_rooms,
        client_socket
    )



# ============================================================
# MAIN SERVER LOOP
# ============================================================
# Waits for incoming client connections.
#
# For each new client:
# 1. Accept connection
# 2. Start a dedicated thread for each connection
#
# Threading allows the server to handle multiple clients simultaneosly without having
# to worry about the accept() blocking

while True:
  try:
    client_socket, client_address = server.accept()
    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address),   # to pass the arguments to the handle client each time thread starts
        daemon=True # when the main loop is stopped the thread will also be stopped
    )
    thread.start()
  except Exception as e:
    print(f"Client not accepted: {e}")
