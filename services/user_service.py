class UserService:

    @staticmethod
    def get_username(clients, client_socket):
        for client in clients:
            if client["socket"] == client_socket:
                return client["username"]

        return "Unknown"

    @staticmethod
    def remove_client(clients, client_socket):
        for client in clients:
            if client["socket"] == client_socket:
                print(f"{client['username']} disconnected")
                clients.remove(client)
                break

        client_socket.close()