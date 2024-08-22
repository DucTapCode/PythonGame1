import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1350, 700))
clock = pygame.time.Clock()

img = pygame.image.load("../player.png")

num_blits = 3

blit_positions = [
    (
        random.randint(0, screen.get_width() - img.get_width()),
        random.randint(0, screen.get_height() - img.get_height()),
    )
    for _ in range(num_blits)
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for pos in blit_positions:
        screen.blit(img, pos)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
