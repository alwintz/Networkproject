    
from hashlib import pbkdf2_hmac
import os
class UserService:
    
   registered_users = {}

   @staticmethod
   def signUp(username, password):
     if username in UserService.registered_users:
      return "ERROR: Username already taken"
     
     if not username or not username.strip():
        return "ERROR: Username cannot be empty"
     
     if not password or not password.strip():
        return "ERROR: Password cannot be empty"
     
     if len(password) < 4:
        return "ERROR: Password must be at least 4 characters"
     
     if "|" in password:
        return "ERROR: Password cannot contain '|' character"
    
     salt = os.urandom(32)
     key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
     UserService.registered_users[username] = {'salt':salt, 'key':key}

     print(f"[AUTH] New user registered: {username}")
     return "SUCCESS"
      

   @staticmethod
   def LogIn (username, password): 
     if not username or not username.strip():
        return "ERROR: Username cannot be empty"
     
     if not password or not password.strip():
        return "ERROR: Password cannot be empty"
     
     if username not in UserService.registered_users:
        return "ERROR: Username or password incorrect"
     
     new_salt = UserService.registered_users[username]['salt']
     new_key = pbkdf2_hmac('sha256', password.encode('utf-8'), new_salt, 100_000)

     if new_key != UserService.registered_users[username]['key']:
      return "ERROR: Username or password incorrect"
     
     print(f"[AUTH] User logged in: {username}")
     return 'SUCCESS'
       
    @staticmethod
    def get_username(clients, client_socket):

        for client in clients:
            if client["socket"] == client_socket:
                return client["username"]

        return "Unknown"

    @staticmethod
    def change_username(clients, client_socket, new_username):

        if new_username.strip() == "":
            client_socket.send(
                "ERROR: Username cannot be empty".encode()
            )
            return

        for client in clients:

            if client["socket"] == client_socket:

                old_username = client["username"]

                client["username"] = new_username

                client_socket.send(
                    f"Username changed from "
                    f"{old_username} to {new_username}".encode()
                )

                print(
                    f"Username changed: "
                    f"{old_username} -> {new_username}"
                )

                return

    @staticmethod
    def remove_client(
        clients,
        rooms,
        user_rooms,
        client_socket
    ):

        if client_socket in user_rooms:

            room = user_rooms[client_socket]

            if client_socket in rooms[room]:
                rooms[room].remove(client_socket)

            del user_rooms[client_socket]

        for client in clients:

            if client["socket"] == client_socket:
                clients.remove(client)
                break

        client_socket.close()
