import socket
from tkinter import *
import json

# Thiết lập clients
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("116.106.225.168", 1512))

# Function to handle button click
def create_room():
    room_name = room_name_entry.get()
    password = password_entry.get()
    print(f"Room Name: {room_name}, Password: {password}")

    # Gửi tên phòng và mật khẩu đến server
    room_info = {"room_name": room_name, "password": password}
    client.send(json.dumps(room_info).encode('utf-8'))

# Khai báo giao diện
root = Tk()
root.title("Test Tạo Room")
root.geometry("1100x500")

# Label và Entry cho tên phòng
room_name_label = Label(root, text="Tên Phòng")
room_name_label.pack(pady=10)
room_name_entry = Entry(root, width=50)
room_name_entry.pack(pady=10)

# Label và Entry cho mật khẩu
password_label = Label(root, text="Mật Khẩu (nếu có)")
password_label.pack(pady=10)
password_entry = Entry(root, width=50, show="*")
password_entry.pack(pady=10)

# Nút để tạo phòng
create_room_button = Button(root, text="Tạo Phòng", command=create_room)
create_room_button.pack(pady=20)

# Start the Tkinter loop
root.mainloop()
