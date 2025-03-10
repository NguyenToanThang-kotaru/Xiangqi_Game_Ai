# def print_triangle(height):
#     for i in range(1, height + 1):
#         print(" " * (height - i) + "*" * i)

# h = int(input("Nhập chiều cao tam giác: "))
# print_triangle(h)
import pygame

# Khởi tạo Pygame
pygame.init()

# Tạo màn hình
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vẽ đường thẳng trong Pygame")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Vòng lặp chính
running = True
while running:
    screen.fill(WHITE)  # Xóa màn hình với màu trắng

    # Vẽ đường thẳng từ (50, 100) đến (400, 300), độ dày 5px
    pygame.draw.line(screen, RED, (50, 100), (400, 300), 5)

    # Cập nhật màn hình
    pygame.display.flip()

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
