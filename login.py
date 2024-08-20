import pygame
import sys
import json
import random
import server.client

# Biến
message = "Đăng nhập thành công"
from_user = "DucTapCode"
# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước cửa sổ
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Đăng nhập/Đăng ký")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Thiết lập font chữ
font = pygame.font.Font(None, 32)

# Các biến input
username = ""
active_username = False
message = ""

# Lấy kích thước màn hình
screen_width, screen_height = screen.get_size()

# Các button
login_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 40)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def random_id():
    return int(random.randint(100000, 999999))


def signin(un):
    global message
    try:
        with open("data/player.json", "r+") as file:
            data = json.load(file)
            existing_ids = {
                user["id"] for user in data
            }  # Tạo tập hợp các ID đã tồn tại
            id = random_id()

            # Kiểm tra ID cho đến khi không trùng lặp
            while id in existing_ids:
                id = random_id()

            for user in data:
                if un == user["username"]:
                    message = "Tên người dùng đã tồn tại."
                    return False

            # Thêm người dùng mới vào danh sách
            data.append({"username": un, "id": id})

            # Quay về đầu tệp và ghi lại dữ liệu
            file.seek(0)
            json.dump(data, file, indent=4)

            return True

    except FileNotFoundError:
        # Nếu tệp không tồn tại, tạo tệp mới với người dùng đầu tiên
        with open("data/player.json", "w") as file:
            data = [{"username": un, "id": random_id()}]
            json.dump(data, file, indent=4)
            return True
    except json.JSONDecodeError:
        # Nếu tệp JSON bị lỗi, tạo tệp mới
        with open("data/player.json", "w") as file:
            data = [{"username": un, "id": random_id()}]
            json.dump(data, file, indent=4)
            return True


def handle_event(event, active_username):
    global username, password, message
    if event.type == pygame.MOUSEBUTTONDOWN:
        if login_button.collidepoint(event.pos):
            if signin(username):
                pygame.quit()
                sys.exit()
        active_username = username_box.collidepoint(event.pos)
        message = ""  # Xóa thông báo khi người dùng bắt đầu tương tác lại
    if event.type == pygame.KEYDOWN:
        if active_username:
            if event.key == pygame.K_BACKSPACE:
                username = username[:-1]
            elif pygame.key.get_mods() & (
                pygame.KMOD_ALT |
                pygame.KMOD_CTRL |
                pygame.KMOD_SHIFT |
                pygame.KMOD_META |
                pygame.KMOD_CAPS |
                pygame.KMOD_NUM |
                pygame.KMOD_MODE |
                pygame.KMOD_GUI
            ):
                # Không thêm gì vào username nếu phím chức năng được nhấn
                pass
            else:
                username += event.unicode
    return active_username



while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        active_username = handle_event(event, active_username)

    # Vẽ ô input cho username
    username_box = pygame.Rect(
        screen_width // 2 - 100, screen_height // 2 - 100, 200, 40
    )
    pygame.draw.rect(screen, GRAY, username_box, 5 if active_username else 1)
    draw_text(username, font, BLACK, screen, screen_width // 2, screen_height // 2 - 80)
    # Vẽ nút login
    pygame.draw.rect(screen, GRAY, login_button)
    draw_text(
        "Next",
        font,
        BLACK,
        screen,
        screen_width // 2,
        screen_height // 2 + 70,
    )

    pygame.display.flip()
    server.client.game_exit()
