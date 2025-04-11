import tkinter as tk
import config_font
import threading
import time

class WaitingRoom:
    def __init__(self, menu_window, main_window, sound_manager):
        self.menu = menu_window
        self.main_window = main_window
        self.sound_manager = sound_manager
        self.running = True

        # Tạo cửa sổ mới như option_menu
        self.root = tk.Toplevel()
        self.root.title("Waiting Room")
        self.root.configure(bg="#333333")
        config_font.center_window(self.root, 800, 440)
        self.root.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(main_window))

        # Ẩn cửa sổ trước đó
        self.menu.withdraw()

        self.waiting_frame = tk.Frame(self.root, bg="black")
        self.waiting_frame.pack(expand=True)

        # Tiêu đề
        title = tk.Label(self.waiting_frame, text="Waiting Room",
                         font=config_font.get_font(20), fg="pink", bg="black")
        title.pack(pady=30)

        # Label trạng thái
        self.status_label = tk.Label(
            self.waiting_frame,
            text="Waiting for other player to join...",
            font=config_font.get_font(14),
            fg="white",
            bg="black"
        )
        self.status_label.pack(pady=20)

        # Hiệu ứng chấm động
        self.loading_label = tk.Label(self.waiting_frame, text="", font=config_font.get_font(14), fg="gray", bg="black")
        self.loading_label.pack(pady=10)

        # Nút Cancel
        cancel_button = tk.Button(
            self.waiting_frame, text="Cancel", bg="#FF3399", fg="white",
            font=config_font.get_font(12), pady=8, padx=30, bd=0, relief="flat", cursor="hand2",
            command=self.cancel_waiting
        )
        cancel_button.pack(pady=30)

        # Hiệu ứng loading
        self.animate_thread = threading.Thread(target=self.animate_dots, daemon=True)
        self.animate_thread.start()

    def animate_dots(self):
        dots = ""
        while self.running:
            dots += "."
            if len(dots) > 3:
                dots = ""
            self.loading_label.config(text=dots)
            time.sleep(0.5)

    def cancel_waiting(self):
        self.running = False
        self.sound_manager.play_click_sound()
        self.root.destroy()
        self.menu.deiconify()
