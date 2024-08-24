import socket
import threading
import time
import random


class Server:
    def __init__(self, host_ip="0.0.0.0", host_port=1512):
        # Variables
        self.host_ip = host_ip
        self.host_port = host_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host_ip, self.host_port))
        self.server.listen()
        print("Server đang lắng nghe...")

        # Data
        self.clients = []
        self.online_players = []
        self.address_list = []
        self.rooms = []
        self.total_data_received = 0  # Variable to track total data received
        self.data_lock = threading.Lock()  # Lock for synchronizing access to data

    # Function to handle individual client
    def handle_client(self, client, address):
        username = None  # Initialize username with a default value
        formatted_address = f"{address[0]}:{address[1]}"
        try:
            while True:
                message = client.recv(1024).decode("utf-8")
                if not message:  # If message is empty, the client has disconnected
                    break
                data = client.recv(1024)
                with self.data_lock:
                    self.total_data_received += len(data)
                if message.startswith("coins"):
                    print(message)
                    parts = message.split()
                    if len(parts) == 5:
                        _, width, player_wid, height, player_hei = parts
                        Thread3.start()
                if message.startswith("coords"):
                    self.broadcast(message, client)
                elif message.startswith("username"):
                    print(message)
                    parts = message.split()
                    if len(parts) == 2:
                        _, username = parts
                        if username not in self.online_players:
                            client.send("True".encode("utf-8"))
                            self.online_players.append(username)
                        else:
                            client.send(
                                "False".encode("utf-8")
                            )  # Inform user if username is taken
                elif message == "room_name":
                    room_name = self.create_room(client)
                    if room_name:
                        client.send(f"Room {room_name} created".encode("utf-8"))
                    else:
                        client.send("Room creation failed".encode("utf-8"))
        except OSError as e:
            if e.errno == 10054:
                print(f"{formatted_address} đã thoát")
        finally:
            if client in self.clients:
                self.clients.remove(client)
            if address in self.address_list:
                self.address_list.remove(address)
            if username in self.online_players:
                self.online_players.remove(username)
            client.close()
            if username:
                print(
                    f"{username} đã ngắt kết nối."
                )  # Inform when the user disconnects

    def print_data_received(self):
        while True:
            time.sleep(5)
            with self.data_lock:
                print(f"Tổng số dữ liệu đã nhận: {self.total_data_received} bytes")

    # Function to broadcast messages to all clients except the sender
    def broadcast(self, message, sender):
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message.encode("utf-8"))
                except Exception as e:
                    print(f"Error broadcasting message: {str(e)}")
                    self.clients.remove(client)
                    client.close()

    # Function to receive connections
    def receive(self):
        while True:
            client, address = self.server.accept()
            formatted_address = f"{address[0]}:{address[1]}"
            print(f"Kết nối từ {str(formatted_address)} đã được chấp nhận")
            self.clients.append(client)
            self.address_list.append(address)
            # Start a new thread for each client
            Thread1 = threading.Thread(
                target=self.handle_client, args=(client, address)
            )
            Thread1.start()

    # Function to create a room
    def create_room(self, client):
        try:
            client.send("Enter room name:".encode("utf-8"))
            room_name = client.recv(1024).decode("utf-8").strip()
            if room_name:
                self.rooms.append({"room_name": room_name})
                return room_name
        except Exception as e:
            print(f"Room creation failed: {str(e)}")
        return None

    # Main method to start the server
    def start(self):
        try:
            self.receive()
        except Exception as e:
            print("Đã xảy ra một số lỗi")


# Main server loop
if __name__ == "__main__":
    server = Server()
    Thread2 = threading.Thread(target=server.print_data_received, daemon=True)
    Thread2.start()

    server.start()
