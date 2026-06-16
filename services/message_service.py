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

            client_socket.send(
                full_message.encode()
            )