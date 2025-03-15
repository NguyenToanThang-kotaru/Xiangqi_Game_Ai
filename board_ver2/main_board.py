"""
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
"""


import pygame
import os
from board import Board
from piece import Piece

os.environ["SDL_VIDEO_CENTERED"] = "1" # center the window on the device's screen

pygame.init()
WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Xiangqi")

board = Board(screen)

# Danh sách quân cờ 
pieces = [
    # Tướng
    Piece("assets/black-tuong.png", 4, 0),
    Piece("assets/red-tuong.png", 4, 9),

    # Sĩ
    Piece("assets/black-si.png", 3, 0), 
    Piece("assets/black-si.png", 5, 0),
    Piece("assets/red-si.png", 3, 9), 
    Piece("assets/red-si.png", 5, 9),

    # Tượng
    Piece("assets/black-tuongj.png", 2, 0), 
    Piece("assets/black-tuongj.png", 6, 0),
    Piece("assets/red-tuongj.png", 2, 9), 
    Piece("assets/red-tuongj.png", 6, 9),

    # Xe
    Piece("assets/black-xe.png", 0, 0), 
    Piece("assets/black-xe.png", 8, 0),
    Piece("assets/red-xe.png", 0, 9), 
    Piece("assets/red-xe.png", 8, 9),

    # Pháo
    Piece("assets/black-phao.png", 1, 2), 
    Piece("assets/black-phao.png", 7, 2),
    Piece("assets/red-phao.png", 1, 7), 
    Piece("assets/red-phao.png", 7, 7),

    # Mã
    Piece("assets/black-ma.png", 1, 0), 
    Piece("assets/black-ma.png", 7, 0),
    Piece("assets/red-ma.png", 1, 9), 
    Piece("assets/red-ma.png", 7, 9),

    # Tốt
    Piece("assets/black-tot.png", 0, 3), 
    Piece("assets/black-tot.png", 2, 3),
    Piece("assets/black-tot.png", 4, 3), 
    Piece("assets/black-tot.png", 6, 3),
    Piece("assets/black-tot.png", 8, 3),
    Piece("assets/red-tot.png", 0, 6), 
    Piece("assets/red-tot.png", 2, 6),
    Piece("assets/red-tot.png", 4, 6), 
    Piece("assets/red-tot.png", 6, 6),
    Piece("assets/red-tot.png", 8, 6)
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for piece in pieces:
            piece.handle_event(event, pieces)

    board.draw()
    for piece in pieces:
        piece.draw(screen)
    
    pygame.display.flip()

pygame.quit()