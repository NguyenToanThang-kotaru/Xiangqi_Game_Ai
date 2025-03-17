# Giao diện khi ấn vào option 
# Xuất hiện menu để điều chỉnh âm thanh

import tkinter as tk
import config_font  # Import để dùng chung font chữ

class OptionMenu:
    def __init__(self, menu):
        self.menu = menu  # Lưu lại cửa sổ menu chính để quay lại khi cần
        self.root = tk.Toplevel()
        self.root.title("Game Settings")
        self.root.geometry("800x440")
        self.root.configure(bg="black")

        # Tiêu đề
        title = tk.Label(self.root, text="Options Menu", 
                         font=config_font.get_font(20), fg="pink", bg="black")
        title.pack(pady=15)

        # Âm lượng nhạc nền
        self.music_volume = 50  # Mặc định 50%
        self.music_label = tk.Label(self.root, text=f"Music Volume: {self.music_volume}%", 
                                    font=config_font.get_font(14), fg="white", bg="black")
        self.music_label.pack(pady=5)

        music_frame = tk.Frame(self.root, bg="black")
        music_frame.pack()
        btn_music_down = tk.Button(music_frame, text="-", font=config_font.get_font(12), 
                                   command=lambda: self.change_volume("music", -10),
                                   width=5, fg="white", bg="gray")
        btn_music_down.pack(side="left", padx=5)
        btn_music_up = tk.Button(music_frame, text="+", font=config_font.get_font(12), 
                                 command=lambda: self.change_volume("music", 10),
                                 width=5, fg="white", bg="gray")
        btn_music_up.pack(side="right", padx=5)

        # Âm lượng hiệu ứng âm thanh
        self.sfx_volume = 50  # Mặc định 50%
        self.sfx_label = tk.Label(self.root, text=f"Sound Effect Volume: {self.sfx_volume}%", 
                                  font=config_font.get_font(14), fg="white", bg="black")
        self.sfx_label.pack(pady=10)

        sfx_frame = tk.Frame(self.root, bg="black")
        sfx_frame.pack()
        btn_sfx_down = tk.Button(sfx_frame, text="-", font=config_font.get_font(12), 
                                 command=lambda: self.change_volume("sfx", -10),
                                 width=5, fg="white", bg="gray")
        btn_sfx_down.pack(side="left", padx=5)
        btn_sfx_up = tk.Button(sfx_frame, text="+", font=config_font.get_font(12), 
                               command=lambda: self.change_volume("sfx", 10),
                               width=5, fg="white", bg="gray")
        btn_sfx_up.pack(side="right", padx=5)

        # Nút quay lại menu chính (MÀU HỒNG)
        exit_button = tk.Button(self.root, text="Back to Menu", 
                                command=self.back_to_menu, font=config_font.get_font(12),
                                fg="white", bg="#FF3399", width=15)
        exit_button.pack(pady=20)

        # Ẩn menu chính khi mở OptionMenu
        self.menu.withdraw()
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_menu)

    def change_volume(self, setting, amount):
        """Thay đổi âm lượng nhạc nền hoặc hiệu ứng âm thanh"""
        if setting == "music":
            self.music_volume = max(0, min(100, self.music_volume + amount))
            self.music_label.config(text=f"Music Volume: {self.music_volume}%")
        elif setting == "sfx":
            self.sfx_volume = max(0, min(100, self.sfx_volume + amount))
            self.sfx_label.config(text=f"Sound Effect Volume: {self.sfx_volume}%")

    def back_to_menu(self):
        """Hiển thị lại menu chính khi quay về"""
        self.menu.deiconify()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    OptionMenu(root)
    root.mainloop()




