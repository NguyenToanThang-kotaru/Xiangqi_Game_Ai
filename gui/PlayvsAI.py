import tkinter as tk
import config_font
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.board import Board
from game.game_logic import GameLogic
from sound_manager import SoundManager


def create_PlayvsAI(main_window, main_menu, sound_manager):
    game_logic = GameLogic() 
    board_window = tk.Toplevel()
    config_font.center_window(board_window, 800, 440)   
    board_window.configure(bg="#333333")
    board_window.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(main_window))
    board_window.title("Xiangqi")

    canvas = tk.Canvas(board_window, height=425, width=400, highlightthickness=0)
    canvas.configure(bg="#333333")
    canvas.pack()
    mode = "Play vs AI"
    board = Board(canvas,None,mode)  # Tạo bàn cờ
    # board.print_board()   

    back_button = tk.Button(board_window, text="Back to Menu", command=lambda: [sound_manager.play_click_sound(),config_font.change_gate(board_window, main_menu)])
    back_button.place(x=10)

    try:
        board_window.mainloop()
    except Exception as e:
        print("Mainloop exception:", e)
        import traceback; traceback.print_exc()
    finally:
        print("Mainloop exited!")
    

# create_PlayvsAI(tk.Tk(),tk.Toplevel());