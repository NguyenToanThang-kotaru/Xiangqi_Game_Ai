from tkinter import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game.Piece import Piece
import config_font
def create_board(main_window):
    CELL_SIZE = 40
    def create_broad(canvas):
        for col in range(9):
            x = (col + 1) * CELL_SIZE
            if col == 0 or col == 8:
                canvas.create_line(x, CELL_SIZE, x, 10*CELL_SIZE, width=2, fill="#FF3399")
            else:
                canvas.create_line(x, CELL_SIZE, x, 5*CELL_SIZE, width=2,fil="#FF3399")
                canvas.create_line(x, 6*CELL_SIZE, x, 10*CELL_SIZE, width=2,fill="#FF3399")
        for row in range(10):
            y = (row + 1) * CELL_SIZE
            canvas.create_line(CELL_SIZE, y, CELL_SIZE * 9, y, width=2,fill="#FF3399")
        canvas.create_line(CELL_SIZE*4, CELL_SIZE, CELL_SIZE*6, CELL_SIZE*3, width=2,fill="#FF3399")
        canvas.create_line(CELL_SIZE*4, CELL_SIZE*3, CELL_SIZE*6, CELL_SIZE, width=2,fill="#FF3399")
        canvas.create_line(CELL_SIZE*4, CELL_SIZE*8, CELL_SIZE*6, CELL_SIZE*10, width=2,fill="#FF3399")
        canvas.create_line(CELL_SIZE*4, CELL_SIZE*10, CELL_SIZE*6, CELL_SIZE*8, width=2,fill="#FF3399")

    def create_pieces(canvas):
        #lưu các ảnh vào biến để sử dụng
        images = {
            "xe_red": PhotoImage(file="assets/red-xe.png"),
            "ma_red": PhotoImage(file="assets/red-ma.png"),
            "tuongj_red": PhotoImage(file="assets/red-tuongj.png"),
            "si_red": PhotoImage(file="assets/red-si.png"),
            "tuong_red": PhotoImage(file="assets/red-tuong.png"),
            "phao_red": PhotoImage(file="assets/red-phao.png"),
            "tot_red": PhotoImage(file="assets/red-tot.png"),

            "xe_black": PhotoImage(file="assets/black-xe.png"),
            "ma_black": PhotoImage(file="assets/black-ma.png"),
            "tuongj_black": PhotoImage(file="assets/black-tuongj.png"),
            "si_black": PhotoImage(file="assets/black-si.png"),
            "tuong_black": PhotoImage(file="assets/black-tuong.png"),
            "phao_black": PhotoImage(file="assets/black-phao.png"),
            "tot_black": PhotoImage(file="assets/black-tot.png")
        }
        
        #đặt các quân cờ vào bàn cờ (canvas)
        
        pieces = [
            # Đỏ
            Piece(canvas, "xe_red", 0, 9, images["xe_red"]),
            Piece(canvas, "ma_red", 1, 9, images["ma_red"]),
            Piece(canvas, "tuongj_red", 2, 9, images["tuongj_red"]),
            Piece(canvas, "si_red", 3, 9, images["si_red"]),
            Piece(canvas, "tuong_red", 4, 9, images["tuong_red"]),
            Piece(canvas, "si_red", 5, 9, images["si_red"]),
            Piece(canvas, "tuongj_red", 6, 9, images["tuongj_red"]),
            Piece(canvas, "ma_red", 7, 9, images["ma_red"]),
            Piece(canvas, "xe_red", 8, 9, images["xe_red"]),
            Piece(canvas, "phao_red", 1, 7, images["phao_red"]),
            Piece(canvas, "phao_red", 7, 7, images["phao_red"]),
            Piece(canvas, "tot_red", 0, 6, images["tot_red"]),
            Piece(canvas, "tot_red", 2, 6, images["tot_red"]),
            Piece(canvas, "tot_red", 4, 6, images["tot_red"]),
            Piece(canvas, "tot_red", 6, 6, images["tot_red"]),
            Piece(canvas, "tot_red", 8, 6, images["tot_red"]),

            # Đen
            Piece(canvas, "xe_black", 0, 0, images["xe_black"]),
            Piece(canvas, "ma_black", 1, 0, images["ma_black"]),
            Piece(canvas, "tuongj_black", 2, 0, images["tuongj_black"]),
            Piece(canvas, "si_black", 3, 0, images["si_black"]),
            Piece(canvas, "tuong_black", 4, 0, images["tuong_black"]),
            Piece(canvas, "si_black", 5, 0, images["si_black"]),
            Piece(canvas, "tuongj_black", 6, 0, images["tuongj_black"]),
            Piece(canvas, "ma_black", 7, 0, images["ma_black"]),
            Piece(canvas, "xe_black", 8, 0, images["xe_black"]),
            Piece(canvas, "phao_black", 1, 2, images["phao_black"]),
            Piece(canvas, "phao_black", 7, 2, images["phao_black"]),
            Piece(canvas, "tot_black", 0, 3, images["tot_black"]),
            Piece(canvas, "tot_black", 2, 3, images["tot_black"]),
            Piece(canvas, "tot_black", 4, 3, images["tot_black"]),
            Piece(canvas, "tot_black", 6, 3, images["tot_black"]),
            Piece(canvas, "tot_black", 8, 3, images["tot_black"]),
        ]

        canvas.images = images  # Giữ tham chiếu ảnh để tránh bị xóa
        return pieces 


    board = Toplevel()
    config_font.center_window(board, 800, 440)
    board.configure(bg="#333333")
    board.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(board,main_window))
    board.title("Xiangqi")
    canvas = Canvas(board, height=425, width=400,highlightthickness=0)
    canvas.configure(bg="#333333")
    canvas.pack()
    
    create_broad(canvas)
    create_pieces(canvas)


    board.mainloop()

    # board.mainloop()
    # board = Toplevel()
    # config_font.center_window(board, 800, 440)
    # board.configure(bg="#333333")
    # board.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(board,main_window))
    # board.title("Xiangqi")
    # canvas = Canvas(board, height=400, width=400,highlightthickness=0)
    # canvas.configure(bg="#333333")
    # canvas.pack()
    # create_broad(canvas)

    # board.mainloop()