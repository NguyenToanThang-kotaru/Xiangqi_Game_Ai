import pygame

class Piece:
    CELL_SIZE = 80
    PIECE_SIZE = CELL_SIZE + 70

    def grid_to_pixel(self, col, row):
        x = col * self.CELL_SIZE - self.PIECE_SIZE // 10 - 7
        y = row * self.CELL_SIZE - self.PIECE_SIZE // 10 - 5
        return x, y

    def __init__(self, image_path, x, y):
        # global PIECE_SIZE
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.PIECE_SIZE, self.PIECE_SIZE))
        self.pos = [self.grid_to_pixel(x, y)]
        self.pos = list(self.grid_to_pixel(x, y))
        self.selected = False

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    #chatgpt support this
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.pos[0] == x and self.pos[1]== y:
                self.selected = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.selected = False
        elif event.type == pygame.MOUSEMOTION and self.selected:
            self.pos = list(event.pos)