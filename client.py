from controller.menu import Menu
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


class ChatClient:

    def __init__(self):
        self.username = input("Enter your username: ")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.client.send(self.username.encode())

        print(f"Connected to server as {self.username}")

    def begin(self):
        print("1. Sign Up")
        print("2. Login")

        def get_credentials ():
                username = input("Username: ")
                password = input("Password: ")
                return username, password
        
        while True:
            
         choice = input("Select the option nr: ")

         #Sign up and redirect to Login
         if choice == "1":
                print("\n===Sign Up===")
                username, password = get_credentials()
                message = f"signup|{username}|{password}"
                try: 
                 self.client.send(message.encode())
                except:
                 print("Failed to send the option (Sign Up)")

                try:
                 response = self.client.recv(1024).decode() 
                 print(response)
                except:
                    print("Server disconnected")
                    return

                if response != "SUCCESS": 
                 continue


                print("\n===Login===")
                username, password = get_credentials()
                message = f"login|{username}|{password}"
                try:
                 self.client.send(message.encode())
                except:
                    print("Failed to send the option (Login)")

                try:
                    response = self.client.recv(1024).decode() 
                    print(response)
                except:
                    print("Server disconnected")
                    return
                
                if response == "SUCCESS":
                 self.username = username
                 print("Logged in")
                 break   
         
         #Login direct
         elif choice == "2":
                print("\n===Login===")
                username, password = get_credentials()
                message = f"login|{username}|{password}"
                try:
                 self.client.send(message.encode())
                except:
                 print("Failed to send the option (Login)")

                try:
                    response = self.client.recv(1024).decode() 
                    print(response)
                except:
                    print("Server disconnected")
                    return
                
                if response == "SUCCESS":
                 self.username = username
                 print("Logged in")
                 break 
                 
         else:
          print("Invalid option. Please select 1 or 2")
        



    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message:
                    print(f"\n{message}")
            except:
                print("Disconnected from server")
                break

    def send_message(self):
        print("\n=== CHAT MODE ===")
        print("Type your message and press Enter.")
        print("Type /menu to return to the main menu.")

        while True:
            message = input("You: ")

            if message.lower() == "/menu":
                return

            if message.strip() == "":
                print("Message cannot be empty")
                continue

            self.client.send(message.encode())

    def change_room(self):
        while True:
            print("\nAvailable Rooms")
            print("1. Room1")
            print("2. Room2")
            print("0. Back")

            room_choice = input("Select room: ")

            if room_choice == "0":
                return
            elif room_choice == "1":
                self.client.send("SWITCH:Room1".encode())
                return
            elif room_choice == "2":
                self.client.send("SWITCH:Room2".encode())
                return
            else:
                print("Invalid room. Please try again.")

    def show_users(self):
        self.client.send("SHOW_USERS".encode())
        input("\nPress Enter to return to menu...")

    def show_rooms(self):
        self.client.send("SHOW_ROOMS".encode())
        input("\nPress Enter to return to menu...")

    def read_history(self):
        print("\nRead Message History")
        print("1. Room1")
        print("2. Room2")
        print("0. Back")

        room_choice = input("Select room: ")

        if room_choice == "0":
            return
        elif room_choice == "1":
            self.client.send("HISTORY:Room1".encode())
        elif room_choice == "2":
            self.client.send("HISTORY:Room2".encode())
        else:
            print("Invalid room")
            return

        input("\nPress Enter to return to menu...")

    def change_username(self):
        new_username = input("Enter new username: ")

        if new_username.strip() == "":
            print("Username cannot be empty")
            return

        self.client.send(f"CHANGE_USERNAME:{new_username}".encode())
        self.username = new_username

    def start(self):
        receive_thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )
        receive_thread.start()

        while True:
            print("\n===== CHAT MENU =====")
            print("1. Send Message")
            print("2. Change Room")
            print("3. Show Users")
            print("4. Show Rooms")
            print("5. Read Message History")
            print("6. Change Username")
            print("7. Exit")

            choice = input("Select option: ")

            if choice == "1":
                self.send_message()
            elif choice == "2":
                self.change_room()
            elif choice == "3":
                self.show_users()
            elif choice == "4":
                self.show_rooms()
            elif choice == "5":
                self.read_history()
            elif choice == "6":
                self.change_username()
            elif choice == "7":
                print("Disconnecting...")
                self.client.close()
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.start()
