import socket
import pygame
import threading
import time


class Player:
    def __init__(self, img):
        self.x = 5
        self.y = 5
        self.img = img
        self.jumpped = False
        self.velocity_y = 0
        self.velo = 3.5
        self.gravity = 0.5
        self.mm_x = [False, False]
        self.mm_y = [False, False]
        self.kaoruka_wid = img.get_width()
        self.kaoruka_hei = img.get_height()
        self.other_x = 5
        self.other_y = 5
        self.direction = False
        self.previous_x = 5
        self.previous_y = 5
        self.other_direction = False
        self.time_delay = 0.04
        self.last_send_time = time.time()
        self.send_threshold = 6.3
        self.lerp_speed = 0.1
        self.target_x = 5
        self.target_y = 5


def connect_to_server():
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


def jump(main):
    if not main.jumpped:  # Only allow jumping if not already in the air
        main.velocity_y = -10  # Initial jump velocity
        main.jumpped = True


# Kết nối tới server
client = connect_to_server()

# Chỉ khởi tạo Pygame nếu kết nối thành công
if client:
    pygame.init()
    pygame.display.set_caption("tnhthatbongcon")
    scr = pygame.display.set_mode((1350, 700))
    width, height = scr.get_size()

    FPS = 144
    clock = pygame.time.Clock()
    img = pygame.image.load("../player.png")
    main = Player(img)

    def receive_data():
        while client:  # Only attempt to receive if the client is connected
            try:
                message = client.recv(1024).decode("utf-8")
                if message.startswith("coords"):
                    parts = message.split()
                    if len(parts) == 4:
                        _, received_x, received_y, received_direction = parts
                        main.target_x, main.target_y = int(float(received_x)), int(
                            float(received_y)
                        )
                        main.other_direction = received_direction == "True"
            except Exception as e:
                print(f"Error receiving data: {str(e)}")
                break

    threading.Thread(target=receive_data, daemon=True).start()

    while True:
        moved = False
        main.previous_x = main.x

        # Apply horizontal movement
        if (
            main.x + (main.mm_x[0] - main.mm_x[1]) * main.velo > 0
            and main.x + (main.mm_x[0] - main.mm_x[1]) * main.velo
            < width - main.kaoruka_wid
        ):
            main.x += (main.mm_x[0] - main.mm_x[1]) * main.velo
            moved = True

        # Apply gravity and vertical movement
        main.velocity_y += main.gravity
        main.y += main.velocity_y

        if main.y >= height - main.kaoruka_hei:
            main.y = height - main.kaoruka_hei
            main.velocity_y = 0
            main.jumpped = False  # Allow jumping again after landing
        if main.other_x != main.target_x or main.other_y != main.target_y:
            main.other_x += (main.target_x - main.other_x) * main.lerp_speed
            main.other_y += (main.target_y - main.other_y) * main.lerp_speed
        if client:
            try:
                current_time = time.time()
                if (
                    moved
                    and (
                        (
                            (main.x - main.previous_x >= main.send_threshold)
                            | (main.y - main.previous_y >= main.send_threshold)
                            | (main.previous_x - main.x >= main.send_threshold)
                            | (main.previous_y - main.y >= main.send_threshold)
                        )
                    )
                ) and (current_time - main.last_send_time >= main.time_delay):
                    client.send(
                        f"coords {main.x} {main.y} {main.direction}".encode("utf-8")
                    )
                    main.last_send_time = current_time  # Update the last send time
            except OSError:
                print("Server đang đóng hoặc xảy ra lỗi khi gửi dữ liệu.")
                client.close()
                client = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    main.mm_x[1] = True
                    main.direction = False
                elif event.key == pygame.K_RIGHT:
                    main.mm_x[0] = True
                    main.direction = True
                elif event.key == pygame.K_UP:
                    jump(main)  # Call jump function
                elif event.key == pygame.K_DOWN:
                    main.mm_y[0] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    main.mm_x[1] = False
                elif event.key == pygame.K_RIGHT:
                    main.mm_x[0] = False
                elif event.key == pygame.K_DOWN:
                    main.mm_y[0] = False

        scr.fill((0, 255, 0))
        if main.previous_x < main.x:
            main.direction = True
        if main.previous_x > main.x:
            main.direction = False
        if main.direction:
            scr.blit(pygame.transform.flip(main.img, True, False), (main.x, main.y))
        else:
            scr.blit(main.img, (main.x, main.y))

        if main.other_direction:
            scr.blit(
                pygame.transform.flip(main.img, True, False),
                (main.other_x, main.other_y),
            )
        else:
            scr.blit(main.img, (main.other_x, main.other_y))

        pygame.display.flip()
        clock.tick(FPS)

# Kết thúc chương trình nếu không kết nối được
else:
    exit()
