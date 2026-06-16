class Menu:

    def show_main_menu(self):
        print("\n===== CHAT MENU =====")
        print("1. Send Message")
        print("2. Change Room")
        print("3. Show Users")
        print("4. Show Rooms")
        print("5. Read Message History")
        print("6. Change Username")
        print("7. Exit")

        return input("Select option: ")

    def show_room_menu(self):
        print("\nAvailable Rooms")
        print("1. Room1")
        print("2. Room2")
        print("0. Back")

        return input("Select room: ")

    def show_history_menu(self):
        print("\nRead Message History")
        print("1. Room1")
        print("2. Room2")
        print("0. Back")

        return input("Select room: ")

    def get_new_username(self):
        return input("Enter new username: ")