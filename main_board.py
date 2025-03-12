import pygame
from board import Board
from piece import Piece

pygame.init()
WIDTH, HEIGHT = 800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Xiangqi")

board = Board(screen)
# initialize all the pieces
bn = Piece("assets/black-ma.png", 1, 0)
rn = Piece("assets/red-ma.png", 1, 9)
rr = Piece("assets/red-xe.png", 0, 9)
br = Piece("assets/black-xe.png", 0, 0)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        rr.handle_event(event)
        br.handle_event(event)
        bn.handle_event(event)
        rn.handle_event(event)

    board.draw()
    rr.draw(screen)
    br.draw(screen)
    bn.draw(screen)
    rn.draw(screen)
    pygame.display.flip()

pygame.quit()
