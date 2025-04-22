import tkinter as tk
import config_font
from waiting_room import WaitingRoom
from sound_manager import SoundManager
from appState import AppState


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
        room_name = self.room_name_entry.get()
        time_limit = self.time_entry.get()
        password = self.password_entry.get()
        print(f"Tạo phòng: {room_name}, Thời gian: {time_limit}, Mật khẩu: {password}")
        self.back_to_waiting_room()

    def cancel(self):
        self.sound_manager.play_click_sound()
        self.frame.destroy()
        self.parent.show_again()

   
