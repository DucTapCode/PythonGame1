import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Khởi tạo màn hình (giả sử kích thước màn hình là 800x600)
screen = pygame.display.set_mode((800, 600))

# Tải hình ảnh
try:
    image = pygame.image.load('../player.png')
except pygame.error as e:
    print(f"Không thể tải hình ảnh: {str(e)}")
    pygame.quit()
    exit()

num_blits = 3

# Lặp lại việc blit hình ảnh lên nhiều vị trí ngẫu nhiên
blit_positions = [
    (
        random.randint(0, screen.get_width() - image.get_width()),
        screen.get_height() - image.get_height(),
    )
    for _ in range(num_blits)
]

# Blit hình ảnh lên các vị trí ngẫu nhiên
for pos in blit_positions:
    screen.blit(image, pos)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Cập nhật màn hình để hiển thị các blits
    pygame.display.flip()

# Thoát Pygame
pygame.quit()
