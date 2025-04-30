import tkinter as tk
import socket
import threading
import config_font
import json
from waiting_room import WaitingRoom
from online_game import OnlineGame
from sound_manager import SoundManager
from appState import AppState


class CreateRoomForm:
    def __init__(self, root, parent, sound_manager):
        self.root = root
        self.parent = parent
        self.sound_manager = sound_manager

        self.server_socket = None
        self.client_socket = None

        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(expand=True)

        title = tk.Label(self.frame, text="Tạo Phòng",
                         font=config_font.get_font(18), fg="pink", bg="black")
        title.pack(pady=20)

        self.room_name_entry = self._create_labeled_entry("Tên Phòng")
        self.time_entry = self._create_labeled_entry("Thời gian mỗi nước (giây)")
        self.password_entry = self._create_labeled_entry("Mật khẩu (tùy chọn)", show="*")

        button_frame = tk.Frame(self.frame, bg="black")
        button_frame.pack(pady=20)

        create_btn = tk.Button(button_frame, text="Tạo", bg="green", fg="white",
                               font=config_font.get_font(12), padx=30, pady=10, bd=0, relief="flat", cursor="hand2",
                               command=self.create_room)
        create_btn.pack(side="left", padx=10)

        cancel_btn = tk.Button(button_frame, text="Hủy", bg="#FF3399", fg="white",
                               font=config_font.get_font(12), padx=30, pady=10, bd=0, relief="flat", cursor="hand2",
                               command=self.cancel)
        cancel_btn.pack(side="left", padx=10)

    def _create_labeled_entry(self, label_text, show=None):
        label = tk.Label(self.frame, text=label_text, font=config_font.get_font(12), fg="white", bg="black")
        label.pack(pady=(10, 0))
        entry = tk.Entry(self.frame, font=config_font.get_font(12), bg="#333", fg="white",
                         show=show, insertbackground="white")
        entry.pack(pady=5, ipadx=10, ipady=5)
        return entry

    def create_room(self):
        self.sound_manager.play_click_sound()
        room_name = self.room_name_entry.get()
        time_limit = self.time_entry.get()
        password = self.password_entry.get()
        print(f"Tạo phòng: {room_name}, Thời gian: {time_limit}, Mật khẩu: {password}")
        self.frame.destroy()
        self.start_server()
        self.show_waiting_room()

    def show_waiting_room(self):
        self.waiting_room = WaitingRoom(
            parent_window=self.root,
            pvp_window=self,
            main_window=self.parent,
            sound_manager=self.sound_manager
        )

    def start_server(self):
        def server_thread():
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('0.0.0.0', 12345))
            self.server_socket.listen(1)
            print("[SERVER] Waiting for client to connect...")

            self.client_socket, addr = self.server_socket.accept()
            print(f"[SERVER] Client connected from {addr}")
            
            try:
                # Nhận dữ liệu đăng nhập từ client
                data = self.client_socket.recv(4096).decode()
                if not data:
                    return
                    
                login_data = json.loads(data)
                if login_data["type"] == "JOIN":
                    # Gửi thông báo kết nối thành công dưới dạng JSON
                    response = {
                        "type": "CONNECT",
                        "status": "SUCCESS",
                        "message": "Kết nối thành công"
                    }
                    self.client_socket.send(json.dumps(response).encode())
                    
                    # Tạo cửa sổ game mới
                    game_window = tk.Toplevel(self.root)
                    game_window.title("Cờ Tướng Online")
                    game_window.geometry("400x500")
                    config_font.center_window(game_window, 400, 500)
                    
                    # Khởi tạo game online (is_host=True vì đây là người tạo phòng)
                    OnlineGame(game_window, self.client_socket, True, self.parent, self.sound_manager)
                    
                    # Đóng phòng chờ
                    if hasattr(self, 'waiting_room'):
                        self.waiting_room.frame.destroy()
            except json.JSONDecodeError as e:
                print(f"Lỗi giải mã JSON: {e}")
            except Exception as e:
                print(f"Lỗi xử lý kết nối: {e}")

        threading.Thread(target=server_thread, daemon=True).start()

    def cancel(self):
        self.sound_manager.play_click_sound()
        self.frame.destroy()
        self.parent.show_again()

    def show_again(self):
        self.__init__(self.root, self.parent, self.sound_manager)

