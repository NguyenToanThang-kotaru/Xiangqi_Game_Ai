import tkinter as tk
import config_font
from waiting_room import WaitingRoom
from sound_manager import SoundManager
from appState import AppState
import socket
import threading
from game.board import Board


class CreateRoomForm:
    def __init__(self, root, parent, sound_manager):
        self.root = root
        self.parent = parent
        self.sound_manager = sound_manager

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
        label = tk.Label(self.frame, text=label_text, font=config_font.get_font(12), fg="white", bg="black")
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
        print(f"Tạo phòng: {self.room_name}, Thời gian: {time_limit}, Mật khẩu: {password}")
        self.frame.pack_forget()
        self.status_label = tk.Label(self.root, text="Waiting for player to join...", fg="white", bg="black", font=config_font.get_font(14))
        self.status_label.pack(pady=20)
        threading.Thread(target=self.start_server, args=(password,), daemon=True).start()

    def start_server(self, password):
        HOST = ''
        PORT = 65432
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)
        print("Server is listening...")
        conn, addr = self.server_socket.accept()
        print(f"Client connected from {addr}")
        # Nhận mật khẩu từ client
        client_password = conn.recv(1024).decode()
        if client_password == password:
            conn.sendall(b'OK')
            # Gửi room_name cho client
            conn.sendall(self.room_name.encode())
            self.status_label.config(text="Player joined! Starting game...")
            self.show_board(self.room_name)
        else:
            conn.sendall(b'WRONG_PASSWORD')
            self.status_label.config(text="Wrong password! Connection refused.")
        conn.close()
        self.server_socket.close()

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

    def cancel(self):
        self.sound_manager.play_click_sound()
        self.frame.destroy()
        self.parent.show_again()

   
