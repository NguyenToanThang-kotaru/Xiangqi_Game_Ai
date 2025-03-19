import tkinter as tk
from game.game_logic import GameLogic

"""
Suggest legit moves for pieces that players try to move
If player click on a piece, suggest all possible moves for that piece
The code should use board, piece, check_move() functions in game_logic.py
"""

CELL_SIZE = 40

class Suggestion:
    suggestions = []
    canvas = None

    def __init__(self, game_logic, canvas):
        self.game_logic = game_logic
        self.canvas = canvas
        Suggestion.canvas = self.canvas
        self.valid_moves = []
    
    # not optimized enough
    def suggest(self, piece, board_state):
        self.valid_moves.clear()
        for col in range(9):
            for row in range(10):
                if self.game_logic.check_move(piece, (col, row), board_state):
                    self.valid_moves.append((col, row))
        self.draw()

    # mark legit moves for the selected piece
    def draw(self):
        for col, row in self.valid_moves:
            x = (col + 1) * CELL_SIZE
            y = (row + 1) * CELL_SIZE
            radius = 5
            oval_id = Suggestion.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='#FFF000', width=2)
            
            Suggestion.suggestions.append(oval_id)

    @staticmethod
    def clear():
        for oval_id in Suggestion.suggestions:
            Suggestion.canvas.delete(oval_id)
        Suggestion.suggestions.clear()
