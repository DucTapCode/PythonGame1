import pygame
import tkinter as tk

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình Pygame ở chế độ fullscreen
screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)

# Tạo cửa sổ Tkinter
root = tk.Tk()

# Đặt tiêu đề và kích thước cửa sổ Tkinter
root.title("Cửa sổ Tkinter trước fullscreen của Pygame")
root.geometry("300x200")

# Đưa cửa sổ Tkinter lên trước (trên top)
root.attributes('-topmost', True)

# Chạy vòng lặp Pygame và hiển thị Tkinter
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Vẽ màu nền Pygame
    screen.fill((0, 0, 0))
    
    # Cập nhật hiển thị Pygame
    pygame.display.flip()

    # Cập nhật cửa sổ Tkinter
    root.update()

# Thoát Pygame và đóng cửa sổ Tkinter
pygame.quit()
root.destroy()
