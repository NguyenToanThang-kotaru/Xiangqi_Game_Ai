import tkinter as tk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.game_logic import GameLogic
from assets import *

CELL_SIZE = 40  # Kích thước ô cờ

class Piece:
    piece_values = {
        "xe": 10,  # Xe (车)
        "phao": 7,  # Pháo (炮)
        "ma": 6,  # Mã (马)
        "tuong": 4,  # Tượng (相/象)
        "si": 3,  # Sĩ (士/仕)
        "tot": 1   # Tốt (兵/卒)
    }

    def __init__(self, canvas, name, x, y, image):
        self.canvas = canvas
        self.name = name 
        self.x = x
        self.y = y
        self.photo = image  # Giữ ảnh trong class
        self.id = canvas.create_image(self.get_pixel_x(), self.get_pixel_y(), image=self.photo, anchor=tk.CENTER)
        self.color = "red" if "red" in name else "black"
        self.value = self.get_piece_value()
    def get_pixel_x(self):
        return (self.x+1) * CELL_SIZE 

    def get_pixel_y(self):
        return (self.y+1) * CELL_SIZE

    def get_piece_value(self):
        """Trả về giá trị của quân cờ"""
        for key in self.piece_values.keys():
            if key in self.name:
                return self.piece_values[key]
        return 0  # Mặc định cho tướng (không tính điểm)

    
    def move(self, x, y):
        self.x = x
        self.y = y
        self.canvas.coords(self.id, self.get_pixel_x(), self.get_pixel_y())

    def delete(self):
        self.canvas.delete(self.id)

    def __str__(self):
        return f"{self.name} tại ({self.x}, {self.y}) - Giá trị: {self.value}"
    

    
    def get_valid_moves(self, board_state):
        """Trả về danh sách các nước đi hợp lệ cho quân cờ này"""
        game_logic = GameLogic()  # Khởi tạo logic game
        valid_moves = []

        # Duyệt tất cả các ô trên bàn cờ
        for y in range(10):
            for x in range(9):
                if game_logic.check_move(self, (x, y), board_state):
                    if game_logic.is_king_safe(self, (x, y), board_state)==None:
                        valid_moves.append((x, y))

        return valid_moves
    