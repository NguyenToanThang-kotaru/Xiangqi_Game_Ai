import tkinter as tk
import config_font
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.Piece import Piece
from board import create_board
from board import create_pieces
from board import CELL_SIZE
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
    # create_pieces(canvas)
    Pieces = create_pieces(canvas)
    # selected_piece=None
    # # for Piece in create_pieces(canvas):
    # #     print(Piece)
    # def on_click(event):
    #     nonlocal selected_piece
    #     x = event.x // CELL_SIZE
    #     y = event.y // CELL_SIZE
    #     if selected_piece:
    #         print(x,y)
    #         selected_piece = None
    #     # if selected_piece!=None:
    #     else:
    #         for Piece in Pieces:
    #             if Piece.x==x and Piece.y==y:
    #                 selected_piece = Piece
    #                 print(selected_piece.x,selected_piece.y)
                    
    # canvas.bind("<Button-1>", on_click)          
    back_button = Button(board, text="Back to Menu", command=lambda: config_font.change_gate(board, main_menu))
    back_button.place(x=10,)
    
    board.mainloop()
        
create_PlayvsAI(tk.Tk(),tk.Toplevel())