import pygame
import socket
import threading
import tkinter
from Python.Online.PythonGame1.login import WHITE

# Kết nối tới server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("116.106.225.168", 1512))

pygame.init()
pygame.display.set_caption("tnhthatbongcon")
scr = pygame.display.set_mode((1100,550))
width, height = scr.get_size()

FPS = 60
clock = pygame.time.Clock()
kaoruka = pygame.image.load("player.png")
kaoruka_wid = kaoruka.get_width()
kaoruka_hei = kaoruka.get_height()
velo = 7
x = 5
y = 5
mm_x = [False, False]
mm_y = [False, False]
other_x, other_y = 5, 5  # Vị trí của người chơi khác


# Hàm để nhận dữ liệu từ server
def receive_data():
    global other_x, other_y
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message.startswith("coords"):
                parts = message.split()
                if len(parts) == 3:  # Đảm bảo nhận đúng 3 phần
                    _, received_x, received_y = parts
                    other_x, other_y = int(received_x), int(received_y)
        except Exception as e:
            print(f"Error receiving data: {str(e)}")
            break


# Bắt đầu nhận dữ liệu trong một thread riêng
threading.Thread(target=receive_data, daemon=True).start()

while True:
    moved = False

    if (
        x + (mm_x[0] - mm_x[1]) * velo > 0
        and x + (mm_x[0] - mm_x[1]) * velo < width - kaoruka_wid
    ):
        x += (mm_x[0] - mm_x[1]) * velo
        moved = True
    if (
        y + (mm_y[0] - mm_y[1]) * velo > 0
        and y + (mm_y[0] - mm_y[1]) * velo < height - kaoruka_hei
    ):
        y += (mm_y[0] - mm_y[1]) * velo
        moved = True

    # Gửi tọa độ hiện tại tới server nếu có thay đổi
    if moved:
        client.send(f"coords {x} {y}".encode("utf-8"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mm_x[1] = True
            elif event.key == pygame.K_RIGHT:
                mm_x[0] = True
            elif event.key == pygame.K_UP:
                mm_y[1] = True
            elif event.key == pygame.K_DOWN:
                mm_y[0] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                mm_x[1] = False
            elif event.key == pygame.K_RIGHT:
                mm_x[0] = False
            elif event.key == pygame.K_UP:
                mm_y[1] = False
            elif event.key == pygame.K_DOWN:
                mm_y[0] = False

    # Vẽ lại màn hình với các vị trí mới
    scr.fill(WHITE)
    scr.blit(kaoruka, (x, y))  # Vẽ người chơi hiện tại
    scr.blit(kaoruka, (other_x, other_y))  # Vẽ người chơi khác
    pygame.display.flip()
    clock.tick(FPS)
