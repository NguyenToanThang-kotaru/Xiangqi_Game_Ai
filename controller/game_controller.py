import tkinter as tk
from view.board_view import BoardView
from game.board import Board
from game.game_logic import GameLogic
from view.sound_manager import SoundManager
import utils.config_font


class GameController:
    def __init__(self, main_window, main_menu, sound_manager):
        self.main_window = main_window
        self.main_menu = main_menu
        self.sound_manager = sound_manager
        self.game_logic = GameLogic()
        
    def create_play_vs_ai(self):
        board_window = tk.Toplevel()
        utils.config_font.center_window(board_window, 800, 440)   
        board_window.configure(bg="#333333")
        board_window.protocol("WM_DELETE_WINDOW", lambda: utils.config_font.close_all(self.main_window))
        board_window.title("Xiangqi")

        # View initialization
        board_view = BoardView(board_window)
        
        # Model initialization
        board = Board(board_view.canvas, "AI")  # Tạo bàn cờ

        # Controller logic: Back button
        board_view.create_back_button(lambda: [self.sound_manager.play_click_sound(), utils.config_font.change_gate(board_window, self.main_menu)])

        board_window.mainloop()
