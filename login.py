# Imports
from tkinter import *
import socket
# Thiết lập clients
try:
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("116.106.225.168", 1512))
except Exception as e:
    print(e)
finally:
    client.close()
# Thiết lập giao diện
root = Tk()
root.geometry("500x500")
root.title("Username")
root.resizable(False,False) # Không cho thay đổi kích thước cửa sổ
root.attributes('-topmost', True) # Đưa cửa sổ lên trên cùng
root.mainloop() 