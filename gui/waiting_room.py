import tkinter as tk
import config_font
from sound_manager import SoundManager
from appState import AppState
import socket
import threading
from game.board import Board_v2

class WaitingRoom:
    def __init__(self, parent_window, pvp_window, main_window, sound_manager):
        self.parent = parent_window          
        self.pvp_window = pvp_window
        self.main_window = main_window
        self.sound_manager = sound_manager
        self.running = True

        # Tạo giao diện con ngay trong cửa sổ cha
        self.frame = tk.Frame(self.parent, bg="black")
        self.frame.pack(expand=True)

        title = tk.Label(self.frame, text="Waiting Room",
                         font=config_font.get_font(20), fg="pink", bg="black")
        title.pack(pady=30)

        # Chỉ tạo label status khi cần
        self.status_label = tk.Label(
            self.frame,
            text="",
            font=config_font.get_font(14),
            fg="white",
            bg="black"
        )
        self.status_label.pack(pady=10)

        self.ip_entry = tk.Entry(self.frame, font=config_font.get_font(12), bg="#333", fg="white")
        self.ip_entry.insert(0, "")
        self.ip_entry.pack(pady=5)
        self.pw_entry = tk.Entry(self.frame, font=config_font.get_font(12), bg="#333", fg="white", show="*")
        self.pw_entry.pack(pady=5)
        join_button = tk.Button(self.frame, text="Join Room", bg="green", fg="white", font=config_font.get_font(12), padx=30, pady=10, bd=0, relief="flat", cursor="hand2", command=self.join_room)
        join_button.pack(pady=10)

        cancel_button = tk.Button(
            self.frame, text="Cancel", bg="#FF3399", fg="white",
            font=config_font.get_font(12), pady=8, padx=30, bd=0, relief="flat", cursor="hand2",
            command=self.cancel_waiting
        )
        cancel_button.pack(pady=30)

    def animate_dots(self):
        pass  # Không cần hiệu ứng loading khi join room

    def cancel_waiting(self):
        self.running = False
        self.sound_manager.play_click_sound()
        self.frame.destroy()                   
        self.pvp_window.show_again()           

    def join_room(self):
        ip = self.ip_entry.get()
        password = self.pw_entry.get()
        self.status_label.config(text="Connecting...")
        threading.Thread(target=self.connect_to_server, args=(ip, password), daemon=True).start()

    def connect_to_server(self, ip, password):
        PORT = 65432
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, PORT))
            s.sendall(password.encode() if password else b'_EMPTY_')
            response = s.recv(1024)
            if response == b'OK':
                room_name = s.recv(1024).decode()
                self.status_label.config(text="Connected! Starting game...")
                self.show_board_v2(room_name)
            else:
                self.status_label.config(text="Wrong password or connection refused.")
    def show_board_v2(self, room_name):
        self.status_label.destroy()
        self.frame.destroy()
        room_label = tk.Label(self.parent, text=f"Room: {room_name}", fg="yellow", bg="black", font=config_font.get_font(16))
        room_label.pack(pady=10)
        self.board_canvas = tk.Canvas(self.parent, width=400, height=425, bg="#333333")
        self.board_canvas.pack(expand=True)
        Board_v2(self.board_canvas)
        back_btn = tk.Button(self.parent, text="Back", bg="#FF3399", fg="white", font=config_font.get_font(12), padx=20, pady=8, command=self.back_to_menu_from_board)
        back_btn.pack(pady=10)

    def back_to_menu_from_board(self):
        try:
            self.client_socket.close()
        except Exception:
            pass
        self.parent.destroy()
        self.main_window.deiconify()
