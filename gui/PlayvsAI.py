import tkinter as tk
import config_font
from board import create_board
from board import create_pieces
from tkinter import *

def create_PlayvsAI(main_window,main_menu):
    board = tk.Toplevel()
    config_font.center_window(board, 800, 440)
    board.configure(bg="#333333")
    board.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(main_window))
    board.title("Xiangqi")
    canvas = Canvas(board, height=425, width=400,highlightthickness=0)
    canvas.configure(bg="#333333")
    canvas.pack()
    create_board(canvas)
    create_pieces(canvas)
    
    back_button = Button(board, text="Back to Menu", command=lambda: config_font.change_gate(board, main_menu))
    back_button.place(x=10,)
    
    board.mainloop()
    
    