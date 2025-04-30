import tkinter as tk
import utils.config_font as config_font
from waiting_room import WaitingRoom
from sound_manager import SoundManager
from appState import AppState
from PlayvsPlayer import NetworkManager

import threading

class CreateRoomForm:
    def __init__(self, root, parent, sound_manager):
        self.root = root
        self.parent = parent
        self.sound_manager = sound_manager
        self.network_manager = NetworkManager()  # Khởi tạo network manager
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(expand=True)

        title = tk.Label(self.frame, text="Create Room",
                         font=config_font.get_font(18), fg="pink", bg="black")
        title.pack(pady=20)

        self.room_name_entry = self._create_labeled_entry("Room Name")
        self.time_entry = self._create_labeled_entry("Time per move (seconds)")
        self.password_entry = self._create_labeled_entry("Password (optional)", show="*")

        button_frame = tk.Frame(self.frame, bg="black")
        button_frame.pack(pady=20)

        create_btn = tk.Button(button_frame, text="Create", bg="green", fg="white",
                               font=config_font.get_font(12), padx=30, pady=10, bd=0, relief="flat", cursor="hand2",
                               command=self.create_room)
        create_btn.pack(side="left", padx=10)

        cancel_btn = tk.Button(button_frame, text="Cancel", bg="#FF3399", fg="white",
                               font=config_font.get_font(12), padx=30, pady=10, bd=0, relief="flat", cursor="hand2",
                               command=self.cancel)
        cancel_btn.pack(side="left", padx=10)

    def _create_labeled_entry(self, label_text, show=None):
        label = tk.Label(self.frame, text=label_text,
                         font=config_font.get_font(12), fg="white", bg="black")
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
        self.room_info = {
            "type": "room_info",
            "room_name": room_name,
            "time_per_move": time_limit,
            "password": password
        }
        
        if self.network_manager.start_server():
            print("Server started, waiting for client...")
            
            # Tạo một thread mới để tiếp tục chờ kết nối
            threading.Thread(target=self.wait_for_client, daemon=True).start()
            
            # Tiếp tục mở giao diện Waiting Room và truyền thông tin phòng
            self.open_waiting_room()

        else:
            print("Không thể khởi tạo server")

    def wait_for_client(self):
        # Đây là nơi bạn kiểm tra xem có khách hàng nào kết nối không
        self.network_manager.wait_for_client_connection()
        # Sau khi người chơi kết nối, có thể cập nhật giao diện hoặc chuyển đến trò chơi
        print("Client has joined the room!")
        self.network_manager.send_data(self.room_info)
        print("Room info sent to client!")
        self.start_game()

    def open_waiting_room(self):
        self.waiting_room = WaitingRoom(self.root, self, self.parent, self.sound_manager, self.room_info)
        self.frame.pack_forget()  # Ẩn giao diện Create Room
        self.waiting_room.frame.pack(expand=True)

    def start_game(self):
        # Chuyển sang giao diện chơi game
        print("Start game!")
        # Bạn có thể gọi hàm hoặc thay đổi giao diện tại đây để bắt đầu trò chơi.

    def cancel(self):
        self.sound_manager.play_click_sound()
        self.frame.destroy()
        self.parent.show_again()
