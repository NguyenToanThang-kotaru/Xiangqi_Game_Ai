import tkinter as tk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from assets import *

CELL_SIZE = 40  # Kích thước ô cờ

class Piece:
    def __init__(self, canvas, name, x, y, image):
        self.canvas = canvas
        self.name = name 
        self.x = x
        self.y = y
        self.photo = image  # Giữ ảnh trong class
        self.id = canvas.create_image(self.get_pixel_x(), self.get_pixel_y(), image=self.photo, anchor=tk.CENTER)

    def get_pixel_x(self):
        return (self.x+1) * CELL_SIZE 

    def get_pixel_y(self):
        return (self.y+1) * CELL_SIZE

    def move(self, x, y):
        self.x = x
        self.y = y
        self.canvas.coords(self.id, self.get_pixel_x(), self.get_pixel_y())

    def delete(self):
        self.canvas.delete(self.id)

root = tk.Tk()
canvas = tk.Canvas(root, width=9*CELL_SIZE, height=10*CELL_SIZE)
canvas.pack()

# Load hình quân cờ
xe_red_img = tk.PhotoImage(file="assets/red-xe.png")

# Đặt quân Xe đỏ tại (0,0) (giao điểm đầu tiên bên trái)
xe_red = Piece(canvas, "xe_red", 0, 0, xe_red_img)
ma_red = Piece(canvas, "ma_red", 1, 0, tk.PhotoImage(file="assets/red-ma.png"))

root.mainloop()
