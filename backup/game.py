import socket
import pygame
import threading
import time
import os

# Khởi tạo biến toàn cục cho trạng thái Pygame
pygame_initialized = False

class Player:
    def __init__(self, img, coin_img):
        self.x = 5
        self.y = 0  # Sẽ được đặt giá trị chính xác sau
        self.img = img
        self.jumpped = False
        self.velocity_y = 0
        self.velo = 3
        self.gravity = 0.8
        self.mm_x = [False, False]
        self.mm_y = [False, False]
        self.kaoruka_wid = img.get_width()
        self.kaoruka_hei = img.get_height()
        self.coin_wid = coin_img.get_width()
        self.coin_hei = coin_img.get_height()
        self.y = height - self.kaoruka_hei
        self.target_x = 5
        self.target_y = height - self.kaoruka_hei
        self.other_x = 5
        self.other_y = 5
        self.direction = False
        self.previous_x = 5
        self.previous_y = 5
        self.other_direction = False
        self.time_delay = 0.04
        self.last_send_time = time.time()
        self.lerp_speed = 0.2
        self.client = None
        self.running = True
        self.coin_pos = (width - self.coin_wid, height - self.coin_hei)
        self.coin = True
        self.coin_sent = False
        self.coin_collected = False
        self.coin_img = coin_img
        self.frame_index = 0
        self.egg_ani = self.load_egg_animation()
        self.frame_time = 0.1  # Thời gian giữa các khung hình của hoạt ảnh
        self.last_frame_time = time.time()

    @staticmethod
    def connect_to_server():
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("duckk.ddns.net", 1512))
            print("Bạn vừa tham gia server")
            return client
        except (ConnectionRefusedError, OSError) as e:
            print(f"Lỗi kết nối tới server: {str(e)}")
        return None

    def connect(self):
        self.client = self.connect_to_server()

    def jump(self):
        if not self.jumpped:
            self.velocity_y = -10
            self.jumpped = True

    def send_coin_collected(self):
        try:
            self.client.send("coin_collected".encode("utf-8"))
            self.coin_sent = True
        except OSError as e:
            print(f"Lỗi khi gửi dữ liệu: {str(e)}")
            if e.errno == 10053:
                print("Bạn đã ngắt kết nối")

    def coin_data(self):
        while self.client and self.running:
            if not self.coin and not self.coin_sent:
                self.send_coin_collected()

    def receive_data(self):
        while self.client and self.running:
            try:
                message = self.client.recv(1024).decode("utf-8")
                if message.startswith("coords"):
                    self.handle_coords_message(message)
                elif message == "coin_collected":
                    self.handle_coin_collected()
                else:
                    print(message)
            except OSError as e:
                if e.errno == 10053:
                    print("Bạn đã ngắt kết nối")
                else:
                    print(f"Lỗi khi nhận dữ liệu: {str(e)}")
                break

    def handle_coords_message(self, message):
        _, received_x, received_y, received_direction = message.split()
        self.target_x = int(float(received_x))
        self.target_y = int(float(received_y))
        self.other_direction = received_direction == "True"

    def handle_coin_collected(self):
        self.coin = False
        self.coin_sent = True
        self.coin_collected = True

    def handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                if self.client:
                    self.client.close()
                exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.KEYUP:
                self.handle_keyup(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_LEFT:
            self.mm_x[1] = True
            self.direction = False
        elif event.key == pygame.K_RIGHT:
            self.mm_x[0] = True
            self.direction = True
        elif event.key == pygame.K_UP:
            self.jump()
        elif event.key == pygame.K_DOWN:
            self.mm_y[0] = True

    def handle_keyup(self, event):
        if event.key == pygame.K_LEFT:
            self.mm_x[1] = False
        elif event.key == pygame.K_RIGHT:
            self.mm_x[0] = False
        elif event.key == pygame.K_DOWN:
            self.mm_y[0] = False

    def update_movement(self):
        moved = False
        self.previous_x = self.x
        player_rect = pygame.Rect(self.x, self.y, self.kaoruka_wid, self.kaoruka_hei)
        coin_rect = pygame.Rect(self.coin_pos[0], self.coin_pos[1], self.kaoruka_wid, self.kaoruka_hei)

        # Horizontal movement
        self.x += (self.mm_x[0] - self.mm_x[1]) * self.velo
        self.x = max(0, min(self.x, width - self.kaoruka_wid))
        moved = self.previous_x != self.x

        # Gravity and vertical movement
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        self.y = min(self.y, height - self.kaoruka_hei)
        if self.y >= height - self.kaoruka_hei:
            self.velocity_y = 0
            self.jumpped = False

        # Other player position update
        self.other_x += (self.target_x - self.other_x) * self.lerp_speed
        self.other_y += (self.target_y - self.other_y) * self.lerp_speed

        # Send position update if moved
        if moved and time.time() - self.last_send_time >= self.time_delay:
            self.send_position_update()

        # Coin collision detection
        if not self.coin_collected and self.coin and player_rect.colliderect(coin_rect):
            self.coin = False
            print("Nhặt xu thành công")

    def send_position_update(self):
        try:
            self.client.send(f"coords {self.x} {self.y} {self.direction}".encode("utf-8"))
            self.last_send_time = time.time()
        except OSError as e:
            print(f"Lỗi khi gửi dữ liệu: {str(e)}")
            self.client.close()
            self.client = None

    def load_egg_animation(self):
        egg_images = []
        for i in range(1, 9):
            egg_images.append(pygame.image.load(f"animations/egg/egg{i}.png"))
        return egg_images

    def update_frame(self):
        # Cập nhật khung hình hoạt ảnh sau một khoảng thời gian nhất định
        if time.time() - self.last_frame_time >= self.frame_time:
            self.frame_index = (self.frame_index + 1) % len(self.egg_ani)
            self.last_frame_time = time.time()

    def draw(self):
        scr.fill((0, 255, 0))
        self.update_direction()
        self.draw_player(self.img, self.x, self.y, self.direction)
        self.draw_player(self.img, self.other_x, self.other_y, self.other_direction)

        # Vẽ đồng xu với hoạt ảnh
        if not self.coin_collected and self.coin:
            self.update_frame()  # Cập nhật khung hình hoạt ảnh
            scr.blit(self.egg_ani[self.frame_index], self.coin_pos)

        pygame.display.flip()

    def update_direction(self):
        if self.previous_x < self.x:
            self.direction = True
        elif self.previous_x > self.x:
            self.direction = False

    def draw_player(self, image, x, y, direction):
        if direction:
            scr.blit(image, (x, y))
        else:
            scr.blit(pygame.transform.flip(image, True, False), (x, y))

    def movement(self):
        while self.running:
            self.update_movement()
            if pygame_initialized:
                self.handle_pygame_events()
                self.draw()
            clock.tick(FPS)


# Khởi tạo Pygame và Player
pygame.init()
os.system("cls")
pygame.display.set_caption("tnhthatbongcon")
scr = pygame.display.set_mode((1350, 700))
width, height = scr.get_size()
FPS = 144
clock = pygame.time.Clock()
img = pygame.image.load("player.png")
coin_img = pygame.image.load("animations/egg/egg1.png")
main = Player(img, coin_img)

# Set the global flag to indicate Pygame is initialized
pygame_initialized = True

main.connect()  # Kết nối tới server

# Chỉ khởi tạo các luồng nếu kết nối thành công
if main.client:
    threading.Thread(target=main.receive_data, daemon=True).start()
    threading.Thread(target=main.coin_data, daemon=True).start()
    main.movement()
else:
    pygame.quit()
    exit()
