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
        sender_id,
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
                recv_id = client["user_id"]

                full_message = (
                    f"{sender_username}: {message}"
                     )

                # tuple that will identify each private message
                # sorted makes the key unique regardless of who is sending/ receiving 
                private_key = tuple(sorted([sender_id, recv_id]))

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
    def send_priv_history_to_client(
        requester_id,
        private_history,
        client_socket,
        requester_username,
        target_username,
        clients):

        for client in clients:
           if client["username"] == target_username:
              target_id = client["user_id"]

              private_key = tuple(sorted([requester_id, target_id]))

              if private_key in private_history:
                history_text = (
                    f"\n--- Message History "
                    f"for {requester_username} and {target_username} ---\n"
                )

                history_text += "\n".join(private_history[private_key])
                history_text += "\n-----------------------\n"

                try:
                    client_socket.send(history_text.encode())
                    return "Sent"
                except:
                    print(f"Failed to send private history to {target_username}")
                    return "Failed"

              else:
                try:
                    client_socket.send(
                        f"No previous messages between you and {target_username}".encode()
                    )
                    return "Sent"
                except:
                    print("Failed to notify empty history")
                    return "Failed"

    
        try:
          client_socket.send(f"User {target_username} not found".encode())
          return "Failed"
        except:
          print("Failed to notify missing user")
          return "Failed"
            
