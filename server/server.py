import socket
import threading
import json

Host_ip = "0.0.0.0"
Host_port = 1512

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((Host_ip, Host_port))
server.listen()

clients = []
online_players = []
rooms = []


def handle_client(client):
    try:
        while True:
            message = client.recv(1024).decode("utf-8")
            if message.startswith("coords"):
                broadcast(message, client)
            elif message == "room_name":
                room_name = create_room(client)
                if room_name:
                    client.send(f"Room {room_name} created".encode("utf-8"))
                else:
                    client.send("Room creation failed".encode("utf-8"))
    except ConnectionResetError:
        print(f"Client {client.getpeername()} disconnected abruptly.")
    except OSError as e:
        print(f"OSError: {str(e)}")
    finally:
        if client in clients:
            clients.remove(client)
        client.close()
        print(f"Connection {client.getpeername()} closed")


def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error broadcasting message: {str(e)}")


def receive():
    global client
    while True:
        client, address = server.accept()
        print(f"Connection from {str(address)} accepted")
        clients.append(client)
        # Start a new thread for each client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


def load_players():
    with open("..\data\player.json", "r") as file:
        data = json.load(file)
        for user in data:
            online_players.append(user["username"])


def create_room(client):
    try:
        client.send("Enter room name:".encode("utf-8"))
        room_name = client.recv(1024).decode("utf-8").strip()
        if room_name:
            rooms.append({"room_name": room_name})
            return room_name
    except Exception as e:
        print(f"Room creation failed: {str(e)}")
    return None


if __name__ == "__main__":
    print("Server is listening...")
    load_players()
    try:
        receive()
    except Exception as e:
        print(f"Error: {str(e)}")
