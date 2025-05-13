# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from tkinter import Tk, Canvas
# from game.board import Board

# def update_fen(fen, move):
#     """Hàm cập nhật trạng thái FEN dựa trên nước đi"""
#     root = Tk()
#     root.withdraw()  # Ẩn cửa sổ GUI
#     fake_canvas = Canvas(root, width=1, height=1)
    
#     board = Board(fake_canvas)  # Tạo board với canvas giả
#     board.set_fen(fen)  # Đặt trạng thái bàn cờ từ FEN
#     board.apply_move(move)  # Áp dụng nước đi
    
#     return board.to_fen()  # Trả về FEN mới

# # Ví dụ sử dụng

# fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/P1P1P1P1P/9/C1N1B1N1C/R3A3R/2BAK4 b"
# move = "h2h2"
# new_fen = update_fen(fen, move)
# print(new_fen)


class Nguoi:
    def __init__(self, ten, tuoi, gioi_tinh):
        self.ten = ten
        self.tuoi = tuoi
        self.gioi_tinh = gioi_tinh
    def input(self):
        self.ten = input("ten: ")
        self.tuoi = int(input("tuoi: "))
        self.gioi_tinh=input("gioi tinh: ")
    def output(self):
        print("ten: ",self.ten)
        print("tuoi: ",self.tuoi)
        print("gioi tinh:",self.gioi_tinh)
    def vetamgiac(self):
        h = int(input("nhap chieu cao: "))
        for i in range(h):
            print("*"*(i+1))
    def vehinhchunhat(self):
        h = int(input("nhap chieu dai: "))
        r = int(input("nhap chieu rong: "))
        for i in range(h):
            print("*"*(r))
nguoi1 = Nguoi("","","")
nguoi1.vehinhchunhat()