import pygame

class Board:
    CELL_SIZE = 80
    BOARD_START_X = 50
    BOARD_START_Y = 50

    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        self.screen.fill((255, 228, 181))  

        # Vẽ lưới bàn cờ (9 cột, 10 hàng)
        for i in range(10):  # Hàng ngang
            pygame.draw.line(self.screen, (0, 0, 0),
                             (self.BOARD_START_X, self.BOARD_START_Y + i * self.CELL_SIZE),
                             (self.BOARD_START_X + 8 * self.CELL_SIZE, self.BOARD_START_Y + i * self.CELL_SIZE), 2)

        for j in range(9):  # Cột dọc
            if j == 0 or j == 8:
                pygame.draw.line(self.screen, (0, 0, 0),
                                 (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y),
                                 (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y + 9 * self.CELL_SIZE), 2)
            else:
                pygame.draw.line(self.screen, (0, 0, 0),
                                 (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y),
                                 (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y + 4 * self.CELL_SIZE), 2)
                pygame.draw.line(self.screen, (0, 0, 0),
                                 (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y + 5 * self.CELL_SIZE),
                                 (self.BOARD_START_X + j * self.CELL_SIZE, self.BOARD_START_Y + 9 * self.CELL_SIZE), 2)

        # Vẽ sông
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.BOARD_START_X, self.BOARD_START_Y + 4.5 * self.CELL_SIZE),
                         (self.BOARD_START_X + 8 * self.CELL_SIZE, self.BOARD_START_Y + 4.5 * self.CELL_SIZE), 2)

        # Vẽ cửa cung
        cung_x_start = self.BOARD_START_X + 3 * self.CELL_SIZE
        cung_x_end = self.BOARD_START_X + 5 * self.CELL_SIZE
        cung_y_top = self.BOARD_START_Y
        cung_y_bottom = self.BOARD_START_Y + 2 * self.CELL_SIZE

        pygame.draw.line(self.screen, (0, 0, 0), (cung_x_start, cung_y_top), (cung_x_end, cung_y_bottom), 2)
        pygame.draw.line(self.screen, (0, 0, 0), (cung_x_end, cung_y_top), (cung_x_start, cung_y_bottom), 2)

        cung_y_top = self.BOARD_START_Y + 7 * self.CELL_SIZE
        cung_y_bottom = self.BOARD_START_Y + 9 * self.CELL_SIZE

        pygame.draw.line(self.screen, (0, 0, 0), (cung_x_start, cung_y_top), (cung_x_end, cung_y_bottom), 2)
        pygame.draw.line(self.screen, (0, 0, 0), (cung_x_end, cung_y_top), (cung_x_start, cung_y_bottom), 2)
