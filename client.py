import socket
import threading
import queue 

HOST = "127.0.0.1"
PORT = 5000


class ChatClient:

    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.pending_invite_queue = queue.Queue() # all pending invites will be stored in this queue

    def get_credentials (self):
                username = input("Username: ")
                password = input("Password: ")
                return username, password
        
    def login(self):
         print("\n===Login===")
         username, password = self.get_credentials()
         message = f"login|{username}|{password}"
         try:
          self.client.send(message.encode())
         except Exception as e:
          print(e)
          return None, None

         try:
          response = self.client.recv(1024).decode()
          print(response)
         except Exception as e:
          print(e)
          return None, None
         return response, username


    def begin(self):
        print("1. Sign Up")
        print("2. Login")
        
        while True:    
         choice = input("Select the option nr: ")

         #Sign up and redirect to Login
         if choice == "1":
                print("\n===Sign Up===")
                username, password = self.get_credentials()
                message = f"signup|{username}|{password}"
                try: 
                 self.client.send(message.encode())
                except Exception as e:
                 print(e)
                 return
                try:
                 response = self.client.recv(1024).decode() 
                 print(response)
                except Exception as e:
                    print(e)
                    return

                if response != "SUCCESS": 
                 continue              # if signup not a success skip login and start the while True from beginning
                response, username = self.login()

                if response == "SUCCESS":
                 self.username = username
                 print("Logged in")
                 self.start()       # this way the receive thread only starts after login avoiding  conflict of recv()
                 break   
         
         #Login direct
         elif choice == "2":
           response, username = self.login()
           if response == "SUCCESS":
            self.username = username
            print("Logged in")
            self.start()
            break   
                
         else:
          print("Invalid option. Please select 1 or 2")
        

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message:
                    print(f"\n{message}")
                    if message .startswith("You were invited to join a room: |"):
                       self.pending_invite_queue.put(message) # enqueue all messages that are invites
            except:
                print("Disconnected from server")
                break


    def send_message_room(self):
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
            try:
             self.client.send(message.encode())
            except:
                print("Failed to send the message")
                return


    def change_room(self):
        self.show_rooms(instruction="Press Enter to type the room")
       
        room_choice = input("Choose a room name: ")
        if room_choice.strip() == "":
           print("Room can't be empty")
           return

        if room_choice == "/menu":
            return

        else:        
         try:
          self.client.send(f"SWITCH: |{room_choice}".encode())
          return
         except:
          print("Failed to choose room")
          return


    def show_users(self, instruction = "Press Enter to return to main Menu"):
        try:
         self.client.send("SHOW_USERS".encode())
        except:
            print("Failed to show users")
            return
        input(f"\n{instruction}")


    def show_rooms(self, instruction = "\nPress Enter to return to Main Menu" ):
        try:
         self.client.send("SHOW_ROOMS".encode())
        except:
           print("Failed to show rooms")
           return
        input(f"{instruction}")


    def read_room_history(self):
        print("\nREAD ROOM MESSAGE HISTORY")
        print("Type /menu to main menu")

        self.show_rooms(instruction="Press Enter to type the room")
       
        room_choice = input("Choose a room name: ")
        if room_choice.strip() == "":
           print("Room can't be empty")
           return

        if room_choice == "/menu":
            return
        else:
           try:
            self.client.send(f"HISTORY: |{room_choice}".encode())
            input("Press Enter to return to menu")
           except:
            print("Failed to send the room name") 
            return


    def change_username(self):
        new_username = input("Enter new username: ")

        if new_username.strip() == "":
            print("Username cannot be empty")
            return

        try:
         self.client.send(f"CHANGE_USERNAME:{new_username}".encode())
         self.username = new_username

        except:
                print("Failed to send new username")
                return


    def send_private_message(self):
        print("\n=== PRIVATE CHAT MODE ===")
        print("Type your message and press Enter.")
        print("Type /menu to return to the main menu.")

        self.show_users(instruction="Press Enter to choose the username")
        while True:
           
           recv_username = input("Send to: ")
           if recv_username.strip() == "":
                print("Receiver can't be empty")
                continue
           
           if recv_username.lower() == "/menu":
              return

           
           while True:
            print("Type back to return to change recipients.")
            message = input("You: ")
            if message.lower() == "back":
                break
            
            if message.strip() == "":
                print("Message cannot be empty")
                continue
            
            try:
              self.client.send(f'private: |{recv_username}|{message}'.encode())
            except:
                print("Failed to send private message")
                return


    def read_private_history(self):
       print("\n=== READ PRIVATE CHAT MODE ===")
       print("Type /menu to return to the main menu.")

       self.show_users(instruction="Press Enter to choose the username")
         
       target_username = input("Read from username: ")
       if target_username.strip() == "":
         print("Receiver can't be empty")

       if target_username == "/menu":
          return
       try:
         self.client.send(f'privHistory: |{target_username}'.encode())   
         input("Press Enter to return to Menu")
       except:
         print("Failed to read private message history")
         return

    
    def invite_room(self):
        print("\n=== INVITE TO ROOM MODE ===")
        print("Type /menu to return to the main menu.")

        self.show_users(instruction="Press Enter to choose the username")
       
        username = input("Enter username: ")
        room = input("Enter the room: ")

        if username.strip() == "":
            print("Username cannot be empty")
            return
      
        try:
         self.client.send(f"INVITE: |{username}|{room}".encode())
        except:
           print("Failed to invite to room")
           return


    # thread for receiving messages. The recv () would block our ability to send messages without it
    def start(self):  
        receive_thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )
        receive_thread.start()

        while True:
            # the invites will be shown before each menu iteration 
            while not self.pending_invite_queue.empty():
                  invite_msg = self.pending_invite_queue.get_nowait()
                  print("\n" + invite_msg)
                  
                  while True:
                    choice = input("1 to Accept/ 2 to Deny")
                    if choice in ("1", "2"): 
                      self.client.send (f"invResponse: |{choice}".encode())
                      break
                    print ("Invalid response: Please choose between 1 and 2")

            print("\n===== CHAT MENU =====")
            print("0. Send Private Message")
            print("1. Send Message to Room")
            print("2. Change Room")
            print("3. Show Users")
            print("4. Show Rooms")
            print("5. Read Room Message History")
            print("6. Read Private Message History")
            print("7. Change Username")
            print("8. Invite user to room (if the room doesn't exist a new one is created)")
            print("9. Exit")
            choice = input("Select the option nr: ")

            if choice == "0":
                self.send_private_message()
            elif choice == "1":
                self.send_message_room()
            elif choice == "2":
                self.change_room()
            elif choice == "3":
                self.show_users()
            elif choice == "4":
                self.show_rooms()
            elif choice == "5":
                self.read_room_history()
            elif choice == "6":
                self.read_private_history()
            elif choice == "7":
                self.change_username()
            elif choice == "8":
                self.invite_room()
            elif choice == "9":
                print("Disconnecting...")
                self.client.close()
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.begin()   

