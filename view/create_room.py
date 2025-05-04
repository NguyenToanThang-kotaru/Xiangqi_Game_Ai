import tkinter as tk
import utils.config_font as config_font
from waiting_room import WaitingRoom
from sound_manager import SoundManager
from appState import AppState
<<<<<<< HEAD:view/create_room.py
from PlayvsPlayer import NetworkManager
=======
import socket
import threading
from game.board import Board
>>>>>>> Huy-Socket:gui/create_room.py

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
        self.room_name = self.room_name_entry.get()
        time_limit = self.time_entry.get()
        password = self.password_entry.get()
<<<<<<< HEAD:view/create_room.py
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
=======
        print(f"Tạo phòng: {self.room_name}, Thời gian: {time_limit}, Mật khẩu: {password}")
        self.frame.pack_forget()
        self.status_label = tk.Label(self.root, text="Waiting for player to join...", fg="white", bg="black", font=config_font.get_font(14))
        self.status_label.pack(pady=20)
        threading.Thread(target=self.start_server, args=(password,), daemon=True).start()

    def start_server(self, password):
        HOST = ''
        PORT = 65432
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(1)
            print("Server is listening...")
            conn, addr = s.accept()
            with conn:  # Also good practice
                print(f"Client connected from {addr}")
                client_password = conn.recv(1024).decode()
                if client_password == '_EMPTY_':
                    client_password = ''
                if client_password == password or password == None:
                    conn.sendall(b'OK')
                    conn.sendall(self.room_name.encode())
                    self.status_label.config(text="Player joined! Starting game...")
                    self.show_board(self.room_name)
                else:
                    conn.sendall(b'WRONG_PASSWORD')
                    self.status_label.config(text="Wrong password! Connection refused.")

    def show_board(self, room_name):
        self.status_label.destroy()
        self.frame.destroy()
        room_label = tk.Label(self.root, text=f"Room: {room_name}", fg="yellow", bg="black", font=config_font.get_font(16))
        room_label.pack(pady=10)
        self.board_canvas = tk.Canvas(self.root, width=400, height=425, bg="#333333")
        self.board_canvas.pack(expand=True)
        Board(self.board_canvas)
        back_btn = tk.Button(self.root, text="Back", bg="#FF3399", fg="white", font=config_font.get_font(12), padx=20, pady=8, command=self.back_to_menu_from_board)
        back_btn.pack(pady=10)

    def back_to_menu_from_board(self):
        try:
            self.server_socket.close()
        except Exception:
            pass
        self.root.destroy()
        self.parent.menu.deiconify()
>>>>>>> Huy-Socket:gui/create_room.py

    def cancel(self):
        self.sound_manager.play_click_sound()
        self.frame.destroy()
        self.parent.show_again()
