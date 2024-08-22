import socket
import threading
import time

# Variables
Host_ip = "0.0.0.0"
Host_port = 1512

# Setup server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((Host_ip, Host_port))
server.listen()

# Data
clients = []
online_players = []
address_list = []
rooms = []
total_data_received = 0  # Biến đếm số lượng dữ liệu nhận được

# Lock để đồng bộ hoá truy cập biến đếm
data_lock = threading.Lock()


# Function to handle individual client
def handle_client(client, address):
    global total_data_received 
    username = None  # Initialize username with a default value
    formatted_address = f"{address[0]}:{address[1]}"
    try:
        while True:
            message = client.recv(1024).decode("utf-8")
            if not message:  # If message is empty, the client has disconnected
                break
            data = client.recv(1024)
            with data_lock:
                total_data_received += len(data)
            if message.startswith("coords"):
                broadcast(message, client)
            elif message.startswith("username"):
                print(message)
                parts = message.split()
                if len(parts) == 2:
                    _, username = parts
                    if username not in online_players:
                        client.send("True".encode("utf-8"))
                        online_players.append(username)
                    else:
                        client.send(
                            "False".encode("utf-8")
                        )  # Optional: inform user if username is taken
            elif message == "room_name":
                room_name = create_room(client)
                if room_name:
                    client.send(f"Room {room_name} created".encode("utf-8"))
                else:
                    client.send("Room creation failed".encode("utf-8"))
    except OSError as e:
        if e.errno == 10054:
            print(f"{formatted_address} đã thoát")
    finally:
        if client in clients:
            clients.remove(client)
        if address in address_list:
            address_list.remove(address)
        if username in online_players:
            online_players.remove(username)
        client.close()
        if username:
            print(f"{username} đã ngắt kết nối.")  # Inform when the user disconnects


def print_data_received():
    global total_data_received
    while True:
        time.sleep(5)
        with data_lock:
            print(f"Tổng số dữ liệu đã nhận: {total_data_received} bytes")


# Function to broadcast messages to all clients except the sender
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error broadcasting message: {str(e)}")
                clients.remove(client)
                client.close()


# Function to receive connections
def receive():
    global client, address
    while True:
        client, address = server.accept()
        formatted_address = f"{address[0]}:{address[1]}"
        print(f"Connection from {str(formatted_address)} accepted")
        clients.append(client)
        address_list.append(address)
        # Start a new thread for each client
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()


# Function to load players from JSON file


# Function to create a room
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


# Main server loop
if __name__ == "__main__":
    print("Server is listening...")
    # Start the data printing thread
    threading.Thread(target=print_data_received, daemon=True).start()
    try:
        receive()
    except Exception as e:
        print("Đã xảy ra một số lỗi")
