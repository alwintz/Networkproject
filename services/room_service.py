class RoomService:

    @staticmethod
    def send_rooms_to_client(
        rooms,
        max_users_per_room,
        client_socket
    ):

        result = "\nAvailable Rooms:\n"

        for room_name, sockets in rooms.items():

            result += (
                f"{room_name} "
                f"({len(sockets)}/{max_users_per_room})\n"
            )

        client_socket.send(result.encode())

    @staticmethod
    def send_users_to_client(
        rooms,
        clients,
        client_socket
    ):

        result = "\nUsers by Room:\n"

        for room_name, sockets in rooms.items():

            result += f"\n{room_name}:\n"

            if not sockets:
                result += " - No users\n"

            for sock in sockets:

                for client in clients:

                    if client["socket"] == sock:

                        result += (
                            f" - {client['username']} "
                            f"({client['ip']}:{client['port']})\n"
                        )

        client_socket.send(result.encode())

    @staticmethod
    def switch_room(
        rooms,
        user_rooms,
        client_socket,
        new_room,
        max_users_per_room
    ):

        if new_room not in rooms:

            client_socket.send(
                "ERROR: Room does not exist".encode()
            )

            return False

        if len(rooms[new_room]) >= max_users_per_room:

            client_socket.send(
                "ERROR: Room is full".encode()
            )

            return False

        current_room = user_rooms[client_socket]

        if current_room == new_room:

            client_socket.send(
                f"You are already in {new_room}".encode()
            )

            return False

        rooms[current_room].remove(client_socket)

        rooms[new_room].append(client_socket)

        user_rooms[client_socket] = new_room

        client_socket.send(
            f"You joined {new_room}".encode()
        )

        return True