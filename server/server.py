import socket
import threading
import time

class Server:
    def __init__(self, host_ip="0.0.0.0", host_port=1512):
        self.host_ip = host_ip
        self.host_port = host_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host_ip, self.host_port))
        self.server.listen()
        print("Server đang lắng nghe...")

        self.clients = []
        self.online_players = []
        self.address_list = []
        self.rooms = []
        self.total_data_received = 0
        self.data_lock = threading.Lock()

    def broadcast(self, message, sender=None, additional_message=None):
        full_message = message
        if additional_message:
            full_message += f"\n{additional_message}"
        for client in self.clients:
            if client != sender:
                try:
                    client.send(full_message.encode("utf-8"))
                except Exception as e:
                    print(f"Error broadcasting message: {str(e)}")
                    self.clients.remove(client)
                    client.close()

    def handle_client(self, client, address):
        username = None
        formatted_address = f"{address[0]}:{address[1]}"
        try:
            while True:
                message = client.recv(1024).decode("utf-8")
                if not message:
                    break

                with self.data_lock:
                    self.total_data_received += len(message)

                if message == "coin_collected":
                    self.broadcast(message)
                elif message.startswith("coords"):
                    self.broadcast(message, client)
                elif message.startswith("username"):
                    username = message.split()[1]
                    if username not in self.online_players:
                        client.send("True".encode("utf-8"))
                        self.online_players.append(username)
                    else:
                        client.send("False".encode("utf-8"))
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
            self.cleanup(client, address, username)
            self.broadcast(f"{username} đã thoát", additional_message=f"Số người còn lại {len(self.clients)}")

    def cleanup(self, client, address, username):
        if client in self.clients:
            self.clients.remove(client)
        if address in self.address_list:
            self.address_list.remove(address)
        if username in self.online_players:
            self.online_players.remove(username)
        client.close()

    def print_data_received(self):
        while True:
            time.sleep(5)
            with self.data_lock:
                print(f"Tổng số dữ liệu đã nhận: {self.total_data_received} bytes")

    def receive(self):
        while True:
            client, address = self.server.accept()
            formatted_address = f"{address[0]}:{address[1]}"
            print(f"Kết nối từ {str(formatted_address)} đã được chấp nhận")
            self.clients.append(client)
            self.address_list.append(address)

            threading.Thread(target=self.handle_client, args=(client, address)).start()

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

    def start(self):
        try:
            self.receive()
        except Exception as e:
            print("Đã xảy ra một số lỗi")

if __name__ == "__main__":
    server = Server()
    threading.Thread(target=server.print_data_received, daemon=True).start()
    server.start()
