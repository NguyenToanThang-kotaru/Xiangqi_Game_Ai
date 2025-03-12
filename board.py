import pygame

class Board:
    def __init__(self, screen):
        self.screen = screen
    
    def draw(self):
        CELL_SIZE = 80
        self.screen.fill((255, 228, 181))

        for i in range(10):
            pygame.draw.line(self.screen, (0, 0, 0), (50, 50 + i * CELL_SIZE), (50 + 8 * CELL_SIZE, 50 + i * CELL_SIZE), 2)
        for j in range(9):
            if j == 0 or j == 8:
                pygame.draw.line(self.screen, (0, 0, 0), (50 + j * CELL_SIZE, 50), (50 + j * CELL_SIZE, 50 + 9 * CELL_SIZE), 2)
            else:
                pygame.draw.line(self.screen, (0, 0, 0), (50 + j * CELL_SIZE, 50), (50 + j * CELL_SIZE, 50 + 4 * CELL_SIZE), 2)
                pygame.draw.line(self.screen, (0, 0, 0), (50 + j * CELL_SIZE, 50 + 5 * CELL_SIZE), (50 + j * CELL_SIZE, 50 + 9 * CELL_SIZE), 2)
