import tkinter as tk
import config_font  # Import để dùng chung font chữ

class OptionMenu:
    def __init__(self, menu, main_window):
        self.menu = menu  # Lưu lại cửa sổ menu chính để quay lại khi cần
        self.root = tk.Toplevel()
        config_font.center_window(self.root, 800, 440)
        self.root.title("Game Settings")
        self.root.configure(bg="black")
        self.root.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(main_window))
        
        title = tk.Label(self.root, text="Options Menu", 
                         font=config_font.get_font(20), fg="pink", bg="black")
        title.pack(pady=15)
        
        title = tk.Label(self.root, text="Level", 
                         font=config_font.get_font(14), fg="white", bg="black")
        title.pack(pady=5)

        # Chọn độ khó
        difficulty_frame = tk.Frame(self.root, bg="black")
        difficulty_frame.pack(pady=10)
        
        tk.Button(difficulty_frame, text="Easy", font=config_font.get_font(12), 
                  fg="white", bg="green", width=10).pack(side="left", padx=5)
        tk.Button(difficulty_frame, text="Medium", font=config_font.get_font(12), 
                  fg="white", bg="orange", width=10).pack(side="left", padx=5)
        tk.Button(difficulty_frame, text="Hard", font=config_font.get_font(12), 
                  fg="white", bg="red", width=10).pack(side="left", padx=5)

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
        
        self.music_canvas = tk.Canvas(music_frame, width=200, height=20, bg="black", highlightthickness=0)
        self.music_canvas.pack(side="left", padx=5)
        self.draw_progress_bar(self.music_canvas, self.music_volume)
        
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
        
        self.sfx_canvas = tk.Canvas(sfx_frame, width=200, height=20, bg="black", highlightthickness=0)
        self.sfx_canvas.pack(side="left", padx=5)
        self.draw_progress_bar(self.sfx_canvas, self.sfx_volume)
        
        btn_sfx_up = tk.Button(sfx_frame, text="+", font=config_font.get_font(12), 
                               command=lambda: self.change_volume("sfx", 10),
                               width=5, fg="white", bg="gray")
        btn_sfx_up.pack(side="right", padx=5)

        # Nút quay lại menu chính
        exit_button = tk.Button(self.root, text="Back to Menu", 
                                command=self.back_to_menu, font=config_font.get_font(12),
                                fg="white", bg="#FF3399", width=15)
        exit_button.pack(pady=20)

        # Ẩn menu chính khi mở OptionMenu
        self.menu.withdraw()

    def draw_progress_bar(self, canvas, value):
        """Vẽ thanh progress kiểu retro với ô vuông"""
        canvas.delete("all")
        canvas.create_rectangle(2, 2, 198, 18, outline="white", width=2)  # Viền ngoài
        
        fill_width = int(196 * (value / 100))
        block_width = 12  # Độ rộng của mỗi ô
        gap = 4  # Khoảng cách giữa các ô
        num_blocks = fill_width // (block_width + gap)
        
        for i in range(num_blocks):
            x1 = 4 + i * (block_width + gap)
            x2 = x1 + block_width
            canvas.create_rectangle(x1, 4, x2, 16, fill="white", outline="white")
    
    def change_volume(self, setting, amount):
        """Thay đổi âm lượng nhạc nền hoặc hiệu ứng âm thanh"""
        if setting == "music":
            self.music_volume = max(0, min(100, self.music_volume + amount))
            self.music_label.config(text=f"Music Volume: {self.music_volume}%")
            self.draw_progress_bar(self.music_canvas, self.music_volume)
        elif setting == "sfx":
            self.sfx_volume = max(0, min(100, self.sfx_volume + amount))
            self.sfx_label.config(text=f"Sound Effect Volume: {self.sfx_volume}%")
            self.draw_progress_bar(self.sfx_canvas, self.sfx_volume)

    def back_to_menu(self):
        """Hiển thị lại menu chính khi quay về"""
        self.menu.deiconify()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    OptionMenu(root, root)
    root.mainloop()
