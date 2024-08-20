import pygame
import socket
import threading

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('116.106.225.168', 1512))

pygame.init()
pygame.display.set_caption("tnhthatbongcon")
scr = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 60
clock = pygame.time.Clock()
kaoruka = pygame.image.load("8834c0656673ed3f08cb42ecbbe30701-removebg-preview (1).png")
velo = 7
x = 5
y = 5
mm_x = [False, False]
mm_y = [False, False]
other_x, other_y = 5, 5  # Position of the other player

# Function to receive data from the server
def receive_data():
    global other_x, other_y
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message.startswith("coords"):
                _, received_x, received_y = message.split()
                other_x, other_y = int(received_x), int(received_y)
        except Exception as e:
            print(f"Error receiving data: {str(e)}")
            break

# Start the receive data thread
threading.Thread(target=receive_data, daemon=True).start()

while True:
    if x + (mm_x[0] - mm_x[1]) * velo > 0 and x + (mm_x[0] - mm_x[1]) * velo < 1270:
        x += (mm_x[0] - mm_x[1]) * velo
    if y + (mm_y[0] - mm_y[1]) * velo > 0 and y + (mm_y[0] - mm_y[1]) * velo < 630:
        y += (mm_y[0] - mm_y[1]) * velo

    # Send the current coordinates to the server
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

    scr.fill((0, 255, 0))
    scr.blit(kaoruka, (x, y))  # Draw the current player
    scr.blit(kaoruka, (other_x, other_y))  # Draw the other player
    pygame.display.flip()
    clock.tick(FPS)
