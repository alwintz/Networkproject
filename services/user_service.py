class UserService:

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