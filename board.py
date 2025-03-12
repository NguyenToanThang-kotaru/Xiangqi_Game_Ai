import pygame

class Board:
    def __init__(self, screen):
        self.screen = screen
    
    def draw(self):
        CELL_SIZE = 70
        NUM_COL = 9
        NUM_ROW = 10
        board_width = (NUM_COL - 1) * CELL_SIZE
        board_height = (NUM_ROW - 1) * CELL_SIZE

        screen_width, screen_height = self.screen.get_size()

        # Take the position so that the chess board could be in the center of the screen
        board_start_x = (screen_width - board_width) // 2
        board_start_y = (screen_height - board_height) // 2

        self.screen.fill((255, 228, 181))

        # draw vertical lines
        for i in range(NUM_ROW):
            y = board_start_y + i * CELL_SIZE
            pygame.draw.line(self.screen, (0, 0, 0), (board_start_x, y), (board_start_x + board_width, y), 2)

        # draw horizontal lines
        for j in range(NUM_COL):
            x = board_start_x + j * CELL_SIZE
            if j == 0 or j == NUM_COL - 1:
                pygame.draw.line(self.screen, (0, 0, 0), (x, board_start_y), (x, board_start_y + board_height), 2)
            else:
                pygame.draw.line(self.screen, (0, 0, 0), (x, board_start_y), (x, board_start_y + 4 * CELL_SIZE), 2)
                pygame.draw.line(self.screen, (0, 0, 0), (x, board_start_y + 5 * CELL_SIZE), (x, board_start_y + board_height), 2)

        # draw diagonal lines
        pygame.draw.line(self.screen, (0, 0, 0), (board_start_x + 3 * CELL_SIZE, CELL_SIZE - 10), (board_start_x + 5 * CELL_SIZE, board_start_y + 2 * CELL_SIZE), 2)
        pygame.draw.line(self.screen, (0, 0, 0), (board_start_x + 3 * CELL_SIZE, board_start_y + 2 * CELL_SIZE), (board_start_x + 5 * CELL_SIZE, CELL_SIZE - 10), 2)
        pygame.draw.line(self.screen, (0, 0, 0), (board_start_x + 3 * CELL_SIZE, board_start_y + 7 * CELL_SIZE), (board_start_x + 5 * CELL_SIZE, board_start_y + 9 * CELL_SIZE), 2)
        pygame.draw.line(self.screen, (0, 0, 0), (board_start_x + 3 * CELL_SIZE, board_start_y + 9 * CELL_SIZE), (board_start_x + 5 * CELL_SIZE, board_start_y + 7 * CELL_SIZE), 2)


# import pygame

# class Board:
#     CELL_SIZE = 80
#     BOARD_START_X = 50
#     BOARD_START_Y = 50

#     def __init__(self, screen):
#         self.screen = screen

#     def draw(self):
#         self.screen.fill((255, 228, 181))  # Màu nền bàn cờ

#         # Vẽ lưới bàn cờ (9 cột, 10 hàng)
#         for i in range(10):  # Hàng ngang
#             pygame.draw.line(self.screen, (0, 0, 0),
#                              (self.BOARD_START_X, self.BOARD_START_Y + i * self.CELL_SIZE),
#                              (self.BOARD_START_X + 8 * self.CELL_SIZE, self.BOARD_START_Y + i * self.CELL_SIZE), 2)

#         for j in range(9):  # Cột dọc
#             if j == 0 or j == 8:
#                 pygame.draw.line(self.screen, (0, 0, 0),
#                                  (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y),
#                                  (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y + 9 * self.CELL_SIZE), 2)
#             else:
#                 pygame.draw.line(self.screen, (0, 0, 0),
#                                  (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y),
#                                  (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y + 4 * self.CELL_SIZE), 2)
#                 pygame.draw.line(self.screen, (0, 0, 0),
#                                  (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y + 5 * self.CELL_SIZE),
#                                  (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y + 9 * self.CELL_SIZE), 2)

#         # Vẽ sông
#         pygame.draw.line(self.screen, (0, 0, 0),
#                          (self.BOARD_START_X, self.BOARD_START_Y + 4.5 * self.CELL_SIZE),
#                          (self.BOARD_START_X + 8 * self.CELL_SIZE, self.BOARD_START_Y + 4.5 * self.CELL_SIZE), 2)

#         # Vẽ cửa cung
#         cung_x_start = self.BOARD_START_X + 3 * self.CELL_SIZE
#         cung_x_end = self.BOARD_START_X + 5 * self.CELL_SIZE
#         cung_y_top = self.BOARD_START_Y
#         cung_y_bottom = self.BOARD_START_Y + 2 * self.CELL_SIZE

#         pygame.draw.line(self.screen, (0, 0, 0), (cung_x_start, cung_y_top), (cung_x_end, cung_y_bottom), 2)
#         pygame.draw.line(self.screen, (0, 0, 0), (cung_x_end, cung_y_top), (cung_x_start, cung_y_bottom), 2)

#         cung_y_top = self.BOARD_START_Y + 7 * self.CELL_SIZE
#         cung_y_bottom = self.BOARD_START_Y + 9 * self.CELL_SIZE

#         pygame.draw.line(self.screen, (0, 0, 0), (cung_x_start, cung_y_top), (cung_x_end, cung_y_bottom), 2)
#         pygame.draw.line(self.screen, (0, 0, 0), (cung_x_end, cung_y_top), (cung_x_start, cung_y_bottom), 2)
