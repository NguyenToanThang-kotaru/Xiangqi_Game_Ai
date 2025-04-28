import tkinter as tk
import config_font
import sys
import os
from network_manager import NetworkManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.board import Board
from game.game_logic import GameLogic
from sound_manager import SoundManager

class NetworkGame:
    def __init__(self, main_window, main_menu, sound_manager, is_server=False, room_info=None, network=None):
        self.main_window = main_window
        self.main_menu = main_menu
        self.sound_manager = sound_manager
        self.is_server = is_server
        self.game_logic = GameLogic()
        self.room_info = room_info or {}
        
        # Tạo cửa sổ game
        self.board_window = tk.Toplevel()
        config_font.center_window(self.board_window, 800, 440)   
        self.board_window.configure(bg="#333333")
        self.board_window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.board_window.title(f"Xiangqi - {self.room_info.get('name', 'Network Game')}")

        # Tạo canvas cho bàn cờ
        self.canvas = tk.Canvas(self.board_window, height=425, width=400, highlightthickness=0)
        self.canvas.configure(bg="#333333")
        self.canvas.pack()

        # Tạo bàn cờ
        self.board = Board(self.canvas, "NETWORK")
        
        # Sử dụng network manager từ WaitingRoom hoặc tạo mới
        if network:
            self.network = network
            self.network.set_callback(self.handle_network_message)
        else:
            self.network = NetworkManager(is_server=is_server, host=room_info.get('server_ip', 'localhost'))
            self.network.set_callback(self.handle_network_message)
            
            if is_server:
                if not self.network.start_server():
                    self.show_error("Failed to start server")
                    self.board_window.destroy()
                    return
            else:
                if not self.network.connect_to_server():
                    self.show_error("Failed to connect to server")
                    self.board_window.destroy()
                    return

        # Set màu quân cờ
        self.board.set_player_color("RED" if is_server else "BLACK")

        # Hiển thị thông tin phòng
        room_info_frame = tk.Frame(self.board_window, bg="#333333")
        room_info_frame.pack(pady=10)

        room_name_label = tk.Label(
            room_info_frame,
            text=f"Room: {self.room_info.get('name', 'Unknown')}",
            font=config_font.get_font(12),
            fg="white",
            bg="#333333"
        )
        room_name_label.pack(side="left", padx=10)

        player_color_label = tk.Label(
            room_info_frame,
            text=f"Your color: {'RED' if is_server else 'BLACK'}",
            font=config_font.get_font(12),
            fg="white",
            bg="#333333"
        )
        player_color_label.pack(side="left", padx=10)

        # Nút quay lại
        self.back_button = tk.Button(
            self.board_window, 
            text="Back to Menu", 
            command=self.back_to_menu,
            bg="#FF3399",
            fg="white",
            font=config_font.get_font(12)
        )
        self.back_button.place(x=10, y=10)

        # Kết nối sự kiện click chuột
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if (self.is_server and self.game_logic.current_player == "RED") or \
           (not self.is_server and self.game_logic.current_player == "BLACK"):
            x, y = event.x, event.y
            piece = self.board.get_piece_at_position(x, y)
            
            if piece:
                if piece.color == self.game_logic.current_player:
                    self.board.select_piece(piece)
                else:
                    # Thực hiện nước đi
                    if self.board.selected_piece:
                        if self.game_logic.is_valid_move(self.board.selected_piece, piece):
                            # Gửi nước đi qua mạng
                            move_data = {
                                'type': 'move',
                                'from_pos': self.board.selected_piece.position,
                                'to_pos': piece.position
                            }
                            self.network.send_message(move_data)
                            
                            # Cập nhật bàn cờ
                            self.board.move_piece(self.board.selected_piece, piece.position)
                            self.game_logic.switch_player()
                            self.board.selected_piece = None

    def handle_network_message(self, message):
        if message['type'] == 'move':
            from_pos = message['from_pos']
            to_pos = message['to_pos']
            
            # Tìm quân cờ tại vị trí bắt đầu
            piece = self.board.get_piece_at_position(from_pos[0], from_pos[1])
            if piece:
                # Di chuyển quân cờ
                self.board.move_piece(piece, to_pos)
                self.game_logic.switch_player()

    def back_to_menu(self):
        self.sound_manager.play_click_sound()
        self.network.close()
        self.main_menu.deiconify()
        self.board_window.destroy()

    def on_window_close(self):
        self.network.close()
        self.main_menu.deiconify()
        self.board_window.destroy()

    def show_error(self, message):
        error_label = tk.Label(
            self.board_window,
            text=message,
            fg="red",
            bg="#333333",
            font=config_font.get_font(12)
        )
        error_label.pack(pady=20) 