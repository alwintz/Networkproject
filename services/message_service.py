class MessageService:

    @staticmethod
    def send_history_to_client(
        message_history,
        client_socket,
        room_name
    ):

        if room_name not in message_history:
            try:
             client_socket.send(
                "ERROR: Room does not exist".encode()
            )
             
            except:
             print("Failed to send error to client")

            return

        if message_history[room_name]:

            history_text = (
                f"\n--- Message History "
                f"for {room_name} ---\n"
            )

            history_text += "\n".join(
                message_history[room_name]
            )

            history_text += "\n-----------------------\n"

        else:

            history_text = (
                f"\nNo previous messages in "
                f"{room_name}\n"
            )

        try:
           client_socket.send(history_text.encode())
        except:
           print("Failed to send history to client")
        return 

    @staticmethod
    def send_message_to_room(
        rooms,
        user_rooms,
        message_history,
        username,
        sender_socket,
        message
    ):

        if sender_socket not in user_rooms:
         try:
            sender_socket.send("Error: You are not in any room".encode())
         except:
            print("Failed to notify sender about room error")
         return
        
        room = user_rooms[sender_socket]

        if room not in rooms:
         try:
            sender_socket.send(f"Error: Room '{room}' does not exist".encode())
         except:
            print(f"Failed to notify sender about missing room {room}")
         return

        full_message = (
            f"[{room}] {username}: {message}"
        )

         
        if room not in message_history:
         message_history[room] = []
        message_history[room].append(full_message)

        for client_socket in rooms[room]:
          try:
            client_socket.send(full_message.encode())
          except:
            print(f"Failed to send message to {client_socket}")

            
            



    @staticmethod
    def send_private_message(
        sender_username,
        sender_socket,
        recv_username,
        private_history, 
        message,
        clients
        ):

        #figuring out if the receiver in connected/ in clients
        for client in clients:
            if client["username"] == recv_username:
                recv_socket = client["socket"]
                full_message = (
                    f"{sender_username}: {message}"
                     )

                # tuple that will identify each private message
                # sorted makes the key unique regardless of who is sending/ receiving
                # it's recognized that ideally ID's should had been added in auth used  for the key as names can change, 
                private_key = tuple(sorted([sender_username, recv_username]))

                #add the private key with value as an array where future messages will be appended
                if private_key not in private_history:
                    private_history[private_key] = []

                private_history[private_key].append(full_message)
                
                try:
                 recv_socket.send(full_message.encode())
                 return "Sent"
                except:
                 print(f"Failed to send private message to {recv_username}")
                 return "Failed"

        try:
            sender_socket.send(f"User {recv_username} not found".encode())
        except:
            print("Failed to notify sender that user not found")
        return "User not found"
    
    
    @staticmethod
    def send_priv_history_to_client(private_history, client_socket, requester_username, target_username):
        
        private_key = tuple(sorted([requester_username, target_username]))

        if private_key in private_history:
           history_text = (
                f"\n--- Message History "
                f"for {requester_username} and {target_username} ---\n"
            )
            
            # how the message will be sent and printed in the client
           history_text += "\n".join(
                private_history[private_key]
            )
           history_text += "\n-----------------------\n"

           try:
            client_socket.send(history_text.encode())
           except:
            print("Failed to send private history to client")

        else:
           try: 
              client_socket.send(f"No previous messages between you and {target_username}")
           except:
              print(f"Failed to notify that there weren't any messages between {requester_username} and {target_username}")
            
    


            
