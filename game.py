import pygame
import socket
import threading
# Kết nối tới server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('116.106.225.168', 1512))
pygame.init()

pygame.display.set_caption("tnhthatbongcon")
scr = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 60
clock = pygame.time.Clock()
kaoruka = pygame.image.load("8834c0656673ed3f08cb42ecbbe30701-removebg-preview (1).png")
velo = 1.75
x = 5
y = 5
mm_x = [False, False]
mm_y = [False, False]

while True:

    if x + (mm_x[0] - mm_x[1]) * velo > 0 and x + (mm_x[0] - mm_x[1]) * velo < 1270:
        x += (mm_x[0] - mm_x[1]) * velo
    if y + (mm_y[0] - mm_y[1]) * velo > 0 and y + (mm_y[0] - mm_y[1]) * velo < 630:
        y += (mm_y[0] - mm_y[1]) * velo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mm_x[1] = True
            elif event.key == pygame.K_RIGHT:
                print(x)
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

    scr.fill((0.0, 255, 0))
    scr.blit(kaoruka, (x, y))
    pygame.display.flip()
    clock.tick(FPS)
