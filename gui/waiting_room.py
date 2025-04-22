import tkinter as tk
import config_font
from sound_manager import SoundManager
from appState import AppState

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

    def animate_dots(self):
        if not self.running:
            return
        self.dot_state += "."
        if len(self.dot_state) > 3:
            self.dot_state = ""
        self.loading_label.config(text=self.dot_state)
        self.frame.after(500, self.animate_dots)

    def cancel_waiting(self):
        self.running = False
        self.sound_manager.play_click_sound()
        self.frame.destroy()                   
        self.pvp_window.show_again()           
