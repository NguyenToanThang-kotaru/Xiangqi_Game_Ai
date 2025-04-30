import tkinter as tk
import utils.config_font as config_font
from sound_manager import SoundManager
from appState import AppState
from PlayvsPlayer import NetworkManager
class WaitingRoom:
    def __init__(self, parent_window, pvp_window, main_window, sound_manager, room_info=None):
        self.parent = parent_window          
        self.pvp_window = pvp_window
        self.main_window = main_window
        self.sound_manager = sound_manager
        self.room_info = room_info
        self.running = True

        # Tạo đối tượng NetworkManager để kết nối
        self.network_manager = NetworkManager()

        # Tạo giao diện con ngay trong cửa sổ cha
        self.frame = tk.Frame(self.parent, bg="black")
        self.frame.pack(expand=True)

        title = tk.Label(self.frame, text="Waiting Room",
                         font=config_font.get_font(20), fg="pink", bg="black")
        title.pack(pady=30)

        # Hiển thị tên phòng và trạng thái
        if self.room_info:
            room_name = self.room_info.get("room_name", "Unknown")
            time_per_move = self.room_info.get("time_per_move", "Unknown")
            password = self.room_info.get("password", "None")
            self.status_label = tk.Label(
                self.frame,
                text=f"Room: {room_name} | Time: {time_per_move}s | Password: {password}",
                font=config_font.get_font(14),
                fg="white",
                bg="black"
            )
            self.status_label.pack(pady=20)
        else:
            self.status_label = tk.Label(
                self.frame,
                text="Waiting for other player to join...",
                font=config_font.get_font(14),
                fg="white",
                bg="black"
            )
            self.status_label.pack(pady=20)

        self.loading_label = tk.Label(self.frame, text="", font=config_font.get_font(14), fg="gray", bg="black")
        self.loading_label.pack(pady=10)

        cancel_button = tk.Button(
            self.frame, text="Cancel", bg="#FF3399", fg="white",
            font=config_font.get_font(12), pady=8, padx=30, bd=0, relief="flat", cursor="hand2",
            command=self.cancel_waiting
        )
        cancel_button.pack(pady=30)

        self.frame.after(500, self.animate_dots)
        self.dot_state = ""

        # Start network connection
        self.start_network_connection()

    def start_network_connection(self):
        """
        Nếu thông tin phòng đã có, kết nối đến server,
        nếu không, chờ kết nối từ client.
        """
        if self.room_info:  # Nếu có thông tin phòng, bắt đầu kết nối với server
            server_ip = self.room_info.get("server_ip", "127.0.0.1")  # Lấy IP từ thông tin phòng
            if self.network_manager.connect_to_server(server_ip):
                self.status_label.config(text="Connected to Server")
                self.loading_label.config(text="")
                self.start_game(False)  # Client
            else:
                print("Error", "Failed to connect to server.")
        else:  # Nếu không có thông tin phòng, bắt đầu làm server
            if self.network_manager.start_server():
                self.status_label.config(text="Waiting for Player to Join...")
                self.loading_label.config(text="")
                self.start_game(True)  # Server

    def start_game(self, is_server):
        """
        Khi kết nối thành công, chuyển sang màn chơi.
        """
        self.frame.destroy()
        game_window = tk.Toplevel(self.parent)
        # create_PlayvsPlayer(game_window, self.main_window)

    def cancel_waiting(self):
        """
        Khi người chơi muốn hủy bỏ kết nối.
        """
        self.running = False
        self.sound_manager.play_click_sound()
        self.frame.destroy()
        self.pvp_window.show_again()

    def animate_dots(self):
        if not self.running:
            return
        self.dot_state += "."
        if len(self.dot_state) > 3:
            self.dot_state = ""
        self.loading_label.config(text=self.dot_state)
        self.frame.after(500, self.animate_dots)
