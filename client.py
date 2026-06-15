import socket

HOST = "127.0.0.1"
PORT = 5000

username = input("Enter username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(username.encode())

while True:
    message = input("Message: ")

    if message.lower() == "exit":
        break

    client.send(message.encode())

client.close()