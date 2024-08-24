import socket
import pygame
import threading
import time

# Khởi tạo biến toàn cục cho trạng thái Pygame
pygame_initialized = False


class Player:
    def __init__(self, img):
        self.x = 5
        self.img = img
        self.jumpped = False
        self.velocity_y = 0
        self.velo = 3
        self.gravity = 0.6
        self.mm_x = [False, False]
        self.mm_y = [False, False]
        self.kaoruka_wid = img.get_width()
        self.kaoruka_hei = img.get_height()
        self.y = height - self.kaoruka_hei
        self.other_x = 5
        self.other_y = 5
        self.direction = False
        self.previous_x = 5
        self.previous_y = 5
        self.other_direction = False
        self.time_delay = 0.04
        self.last_send_time = time.time()
        self.send_threshold = 2
        self.lerp_speed = 0.1
        self.target_x = 5
        self.target_y = height - self.kaoruka_hei
        self.client = None  # Initialize client as None
        self.running = True  # Flag to indicate if Pygame is running
        self.coin_pos = (width - self.kaoruka_wid, height - self.kaoruka_hei)
        self.coin = True
        

    @staticmethod
    def connect_to_server():
        global client
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("116.106.225.168", 1512))
            print("Connected to the server successfully.")
            return client
        except ConnectionRefusedError:
            print("Server hiện đang đóng")
        except OSError as e:
            print(f"Server đang đóng hoặc xảy ra lỗi: {str(e)}")
        return None

    def connect(self):
        self.client = self.connect_to_server()

    def jump(self):
        if not self.jumpped:  # Only allow jumping if not already in the air
            self.velocity_y = -10  # Initial jump velocity
            self.jumpped = True

    def receive_data(self):
        global message
        while self.client:  # Only attempt to receive if the client is connected
            try:
                message = self.client.recv(1024).decode("utf-8")
                if message.startswith("coords"):
                    parts = message.split()
                    if len(parts) == 4:
                        _, received_x, received_y, received_direction = parts
                        self.target_x, self.target_y = int(float(received_x)), int(
                            float(received_y)
                        )
                        self.other_direction = received_direction == "True"
                if message.startswith("coins_pos"):
                    parts = message.split()
                    print(parts)
            except Exception as e:
                print(f"Error receiving data: {str(e)}")
                break

    def movement(self):
        while self.running:
            moved = False
            self.previous_x = self.x

            try:
                # Apply horizontal movement
                if (
                    self.x + (self.mm_x[0] - self.mm_x[1]) * self.velo > 0
                    and self.x + (self.mm_x[0] - self.mm_x[1]) * self.velo
                    < width - self.kaoruka_wid
                ):
                    self.x += (self.mm_x[0] - self.mm_x[1]) * self.velo
                    moved = True

                # Apply gravity and vertical movement
                self.velocity_y += self.gravity
                self.y += self.velocity_y

                if self.y >= height - self.kaoruka_hei:
                    self.y = height - self.kaoruka_hei
                    self.velocity_y = 0
                    self.jumpped = False  # Allow jumping again after landing
                if self.other_x != self.target_x or self.other_y != self.target_y:
                    self.other_x += (self.target_x - self.other_x) * self.lerp_speed
                    self.other_y += (self.target_y - self.other_y) * self.lerp_speed
                if self.client:
                    try:
                        current_time = time.time()
                        if (
                            moved
                            and (abs(self.x - self.previous_x) >= self.send_threshold)
                            and (current_time - self.last_send_time >= self.time_delay)
                        ):
                            self.client.send(
                                f"coords {self.x} {self.y} {self.direction}".encode(
                                    "utf-8"
                                )
                            )
                            self.last_send_time = (
                                current_time  # Update the last send time
                            )
                    except OSError as e:
                        print(f"Error sending data: {str(e)}")
                        self.client.close()
                        self.client = None

                if pygame_initialized:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            pygame.quit()
                            exit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                self.mm_x[1] = True
                                self.direction = False
                            elif event.key == pygame.K_RIGHT:
                                self.mm_x[0] = True
                                self.direction = True
                            elif event.key == pygame.K_UP:
                                self.jump()  # Call jump function
                            elif event.key == pygame.K_DOWN:
                                self.mm_y[0] = True
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_LEFT:
                                self.mm_x[1] = False
                            elif event.key == pygame.K_RIGHT:
                                self.mm_x[0] = False
                            elif event.key == pygame.K_DOWN:
                                self.mm_y[0] = False

                    # Ensure that we are still running before accessing Pygame
                    if pygame_initialized:
                        scr.fill((0, 255, 0))
                        if self.previous_x < self.x:
                            self.direction = True
                        if self.previous_x > self.x:
                            self.direction = False
                        if not self.direction:
                            scr.blit(
                                pygame.transform.flip(self.img, True, False),
                                (self.x, self.y),
                            )
                        else:
                            scr.blit(self.img, (self.x, self.y))

                        if not self.other_direction:
                            scr.blit(
                                pygame.transform.flip(self.img, True, False),
                                (self.other_x, self.other_y),
                            )
                        else:
                            scr.blit(self.img, (self.other_x, self.other_y))
                        if self.coin:
                            player_rect = pygame.Rect(self.x, self.y, self.kaoruka_wid, self.kaoruka_hei)
                            coin_rect = pygame.Rect(self.coin_pos[0], self.coin_pos[1], self.kaoruka_wid, self.kaoruka_hei)
                            scr.blit(self.img, self.coin_pos)
                            if player_rect.colliderect(coin_rect):
                                self.coin = False
                                print("Nhặt xu thành công")
                        pygame.display.flip()
                        clock.tick(FPS)
            except Exception as e:
                print(f"Error in movement thread: {str(e)}")
                self.running = False
                break


# Khởi tạo Pygame và Player
pygame.init()
pygame.display.set_caption("tnhthatbongcon")
scr = pygame.display.set_mode((1350, 700))
width, height = scr.get_size()

FPS = 144
clock = pygame.time.Clock()
img = pygame.image.load("player.png")
main = Player(img)

# Set the global flag to indicate Pygame is initialized
pygame_initialized = True

main.connect()  # Kết nối tới server

# Chỉ khởi tạo các luồng nếu kết nối thành công
if main.client:
    Thread1 = threading.Thread(target=main.receive_data, daemon=True)
    Thread1.start()
    main.movement()
else:
    pygame.quit()
    exit()
