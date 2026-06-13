import socket

HOST = "127.0.0.1"
PORT = 5000

username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(username.encode())

print(f"Connected to server as {username}")

message = client.recv(1024).decode()
print(message)

client.close()