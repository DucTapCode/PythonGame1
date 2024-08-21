# Imports
import tkinter as tk
import socket
# Thiết lập clients
try:
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("116.106.225.168", 1512))
except Exception as e:
    print(e)
# Hàm gửi dữ liệu qua server
def send_data():
    name = entry.get()
    client.send(f"username {name}".encode("utf-8"))
    message = client.recv(1024).decode('utf-8')
    if message:
        print(f"Bạn hiện đăng nhập với tư cách {name}")
        root.destroy()
    else:
        print("Đăng nhập thất bại")
# Thiết lập giao diện
root = tk.Tk()
root.geometry("300x200")
root.title("Username")
root.resizable(False,False) # Không cho thay đổi kích thước cửa sổ
root.attributes('-topmost', True) # Đưa cửa sổ lên trên cùng
# Tạo label
label = tk.Label(root,text="Tên của bạn")
label.config(font=("", 15))
label.pack(pady=20,padx=10)
# Tạo entry
entry = tk.Entry(root,width=250)
entry.pack(pady=10,padx=10)
# Tạo nút
button = tk.Button(root, text="Next",width=15,height=10,command=send_data)
button.pack(padx=10,pady=10)
root.mainloop() 