# import pygame

# class Piece:
#     CELL_SIZE = 80
#     PIECE_SIZE = CELL_SIZE + 70

#     def grid_to_pixel(self, col, row):
#         x = col * self.CELL_SIZE - self.PIECE_SIZE // 10 - 7
#         y = row * self.CELL_SIZE - self.PIECE_SIZE // 10 - 5
#         return x, y

#     def __init__(self, image_path, x, y):
#         # global PIECE_SIZE
#         self.image = pygame.image.load(image_path)
#         self.image = pygame.transform.scale(self.image, (self.PIECE_SIZE, self.PIECE_SIZE))
#         self.pos = [self.grid_to_pixel(x, y)]
#         self.pos = list(self.grid_to_pixel(x, y))
#         self.selected = False

#     def draw(self, screen):
#         screen.blit(self.image, self.pos)

#     #chatgpt support this
#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             x, y = event.pos
#             if self.pos[0] == x and self.pos[1]== y:
#                 self.selected = True
#         elif event.type == pygame.MOUSEBUTTONUP:
#             self.selected = False
#         elif event.type == pygame.MOUSEMOTION and self.selected:
#             self.pos = list(event.pos)



import pygame

class Piece:
    CELL_SIZE = 70  # Kích thước mỗi ô cờ
    NUM_COL = 9
    NUM_ROW = 10
    board_width = (NUM_COL - 1) * CELL_SIZE
    board_height = (NUM_ROW - 1) * CELL_SIZE

    screen_width, screen_height = 750, 750 #cannot use the function screen.get_size()
    BOARD_START_X = (screen_width - board_width) // 2  # Vị trí bắt đầu bàn cờ
    BOARD_START_Y = (screen_height - board_height) // 2  # Vị trí bắt đầu bàn cờ
    PIECE_SIZE = 90  # Kích thước quân cờ

    def __init__(self, image_path, col, row):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.PIECE_SIZE, self.PIECE_SIZE))
        self.col = col  # Vị trí cột 
        self.row = row  # Vị trí hàng 
        self.selected = False
        self.offset_x = 0  # Khoảng cách giữa chuột và tâm quân cờ khi click
        self.offset_y = 0
        self.update_position()

    def update_position(self):
        # Cập nhật vị trí hiển thị quân cờ theo ô cờ 
        self.x = self.BOARD_START_X + self.col * self.CELL_SIZE - self.PIECE_SIZE // 2
        self.y = self.BOARD_START_Y + self.row * self.CELL_SIZE - self.PIECE_SIZE // 2

    def draw(self, screen):
        # Vẽ quân cờ lên màn hình 
        screen.blit(self.image, (self.x, self.y))

    def handle_event(self, event):
        # Xử lý sự kiện chuột để kéo thả quân cờ 
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if self.x <= mx <= self.x + self.PIECE_SIZE and self.y <= my <= self.y + self.PIECE_SIZE:
                self.selected = True
                self.offset_x = mx - self.x
                self.offset_y = my - self.y

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selected:
                mx, my = event.pos

                # Căn chỉnh vị trí quân cờ về đúng ô gần nhất
                self.col = round((mx - self.BOARD_START_X) / self.CELL_SIZE)
                self.row = round((my - self.BOARD_START_Y) / self.CELL_SIZE)

                # Giới hạn phạm vi di chuyển trong bàn cờ
                self.col = max(0, min(8, self.col))
                self.row = max(0, min(9, self.row))

                # Cập nhật lại vị trí đúng ô
                self.update_position()
                self.selected = False

        elif event.type == pygame.MOUSEMOTION and self.selected:
            # Di chuyển quân cờ theo chuột nhưng vẫn giữ khoảng cách ban đầu
            mx, my = event.pos
            self.x = mx - self.offset_x
            self.y = my - self.offset_y

