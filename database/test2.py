import pygame
from test import Game  # Import class Game từ file game.py

# Kích thước cửa sổ game
BOARD_WIDTH = 9
BOARD_HEIGHT = 10
SQSIZE = 60  # Kích thước ô vuông
WIDTH = 1000
HEIGHT = 1000

# Khởi tạo Pygame
pygame.init()

# Tạo cửa sổ game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Tướng với Pygame")

# Khởi tạo game
game = Game()

# Vòng lặp game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Thoát game khi nhấn nút X

    # Hiển thị bàn cờ
    game.show_bg(screen)

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát game
pygame.quit()
