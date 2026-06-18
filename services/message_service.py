class MessageService:

    @staticmethod
    def send_history_to_client(
        message_history,
        client_socket,
        room_name
    ):

        if room_name not in message_history:

            client_socket.send(
                "ERROR: Room does not exist".encode()
            )

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

        client_socket.send(history_text.encode())

    @staticmethod
    def send_message_to_room(
        rooms,
        user_rooms,
        message_history,
        username,
        sender_socket,
        message
    ):

        room = user_rooms[sender_socket]

        full_message = (
            f"[{room}] {username}: {message}"
        )

        message_history[room].append(full_message)

        for client_socket in rooms[room]:




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


            client_socket.send(
                full_message.encode()
            )
