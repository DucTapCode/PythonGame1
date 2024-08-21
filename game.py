import pygame
import socket
import threading


class Player:
    def __init__(self, img):
        self.x = 5
        self.y = 5
        self.img = img
        self.velocity_y = 0
        self.velo = 10
        self.gravity = 0.5
        self.mm_x = [False, False]
        self.mm_y = [False, False]
        self.kaoruka_wid = img.get_width()
        self.kaoruka_hei = img.get_height()
        self.mm_x = [False, False]
        self.mm_y = [False, False]
        self.other_x = 5
        self.other_y = 5
        self.direction = False
        self.previous_x = 5
        self.other_direction = False


# Kết nối tới server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("116.106.225.168", 1512))

pygame.init()
pygame.display.set_caption("tnhthatbongcon")
scr = pygame.display.set_mode((1100, 550))
width, height = scr.get_size()

FPS = 60
clock = pygame.time.Clock()
img = pygame.image.load("player.png")
main = Player(img)


def receive_data():
    global other_x, other_y
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message.startswith("coords"):
                parts = message.split()
                if len(parts) == 4:
                    _, received_x, received_y, received_direction = parts
                    main.other_x, main.other_y = int(received_x), int(received_y)
                    main.other_direction = received_direction == "True"
        except Exception as e:
            print(f"Error receiving data: {str(e)}")
            break


threading.Thread(target=receive_data, daemon=True).start()

while True:
    moved = False
    main.previous_x = main.x
    if (
        main.x + (main.mm_x[0] - main.mm_x[1]) * main.velo > 0
        and main.x + (main.mm_x[0] - main.mm_x[1]) * main.velo < 1100
    ):
        main.x += (main.mm_x[0] - main.mm_x[1]) * main.velo
        moved = True
    if (
        main.y + (main.mm_y[0] - main.mm_y[1]) * main.velo > 0
        and main.y + (main.mm_y[0] - main.mm_y[1]) * main.velo < 550
    ):
        main.y += (main.mm_y[0] - main.mm_y[1]) * main.velo
        moved = True

    if moved:
        client.send(f"coords {main.x} {main.y} {main.direction}".encode("utf-8"))

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
                main.mm_y[1] = True
            elif event.key == pygame.K_DOWN:
                main.mm_y[0] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                main.mm_x[1] = False
            elif event.key == pygame.K_RIGHT:
                main.mm_x[0] = False
            elif event.key == pygame.K_UP:
                main.mm_y[1] = False
            elif event.key == pygame.K_DOWN:
                main.mm_y[0] = False

    scr.fill((0, 255, 0))
    if(main.previous_x<main.x):
        main.direction=True
    if(main.previous_x>main.x):
        main.direction=False
    if main.direction:
        scr.blit(pygame.transform.flip(main.img, True, False), (main.x, main.y))
    else:
        scr.blit(main.img, (main.x, main.y))

    if main.other_direction:
        scr.blit(
            pygame.transform.flip(main.img, True, False), (main.other_x, main.other_y)
        )
    else:
        scr.blit(main.img, (main.other_x, main.other_y))

    pygame.display.flip()
    clock.tick(FPS)
