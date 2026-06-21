    
from hashlib import pbkdf2_hmac
import os

class UserService:
    
    registered_users = {}
    next_id = 1

    @staticmethod
    def signUp(username, password):
     # the id will be added as value to minimize changes as it was added later
     user_id = UserService.next_id    
     UserService.next_id += 1

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
    
     salt = os.urandom(32)  # to generate different outputs from same inputs
     key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000) #hashing the password
     UserService.registered_users[username] = {'id': user_id, 'salt':salt, 'key':key}

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
     
     new_salt = UserService.registered_users[username]['salt'] # retrieving the salt of the user
     new_key = pbkdf2_hmac('sha256', password.encode('utf-8'), new_salt, 100_000) #hashing to then compare

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

     if not new_username or not new_username.strip():
        return "ERROR: Username cannot be empty"
    
     if "|" in new_username:
        return "ERROR: Username cannot contain '|' character"
        
        
     for client in clients:
        if client["socket"] == client_socket:
            old_username = client["username"]
            
            
            if new_username in UserService.registered_users and new_username != old_username:
                return "ERROR: Username already taken"
            
            UserService.registered_users[new_username] = UserService.registered_users.pop(old_username)
            
            client["username"] = new_username

            
            print(f"Username changed: {old_username} -> {new_username}")
            return "SUCCESS"
    
     return "ERROR: Client not found"

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
