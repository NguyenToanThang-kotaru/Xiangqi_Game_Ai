import tkinter as tk
import config_font
from waiting_room import WaitingRoom
from create_room import CreateRoomForm
from sound_manager import SoundManager
from appState import AppState

class PlayerVsPlayer:
    def __init__(self, menu_window, main_window):
        self.menu = menu_window
        self.main_window = main_window
        self.root = tk.Toplevel()
        self.sound_manager = SoundManager()

        # Đồng bộ trạng thái âm thanh
        if not AppState.sound_on:
            self.sound_manager.mute()

        config_font.center_window(self.root, 800, 440)
        self.root.title("Player vs Player")
        self.root.configure(bg="black")
        self.root.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(main_window))

        # Ẩn menu chính khi mở
        self.menu.withdraw()

        # Frame chính
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(expand=True)

        title = tk.Label(self.frame, text="Player vs Player",
                         font=config_font.get_font(20), fg="pink", bg="black")
        title.pack(pady=30)

        # Frame chứa nút
        button_frame = tk.Frame(self.frame, bg="black")
        button_frame.pack(pady=20)

        # Nút Create
        create_button = tk.Button(
            button_frame, text="Create", bg="green", fg="white",
            font=config_font.get_font(14), pady=12, padx=40, bd=0, relief="flat", cursor="hand2",
            command=lambda: [self.sound_manager.play_click_sound(), self.open_create_room()]
        )
        create_button.pack(pady=10)

        # Nút Search
        search_button = tk.Button(
            button_frame, text="Search", bg="yellow", fg="black",
            font=config_font.get_font(14), pady=12, padx=40, bd=0, relief="flat", cursor="hand2",
            command=lambda: [self.sound_manager.play_click_sound(), self.open_waiting_room()]
        )
        search_button.pack(pady=10)

        # Nút quay lại
        back_button = tk.Button(
            button_frame, text="Back to Menu", bg="#FF3399", fg="white",
            font=config_font.get_font(12), pady=8, padx=30, bd=0, relief="flat", cursor="hand2",
            command=self.back_to_menu
        )
        back_button.pack(pady=10)

    def open_waiting_room(self):
        self.frame.pack_forget()
        WaitingRoom(self.root, self, self.main_window, self.sound_manager)

    def back_to_menu(self):
        self.sound_manager.play_click_sound()
        self.menu.deiconify()
        self.root.destroy()

    def show_again(self):
        self.frame.pack(expand=True)
        self.root.deiconify()

    def open_create_room(self):
        self.sound_manager.play_click_sound()
        self.frame.pack_forget()
        CreateRoomForm(self.root, self, self.sound_manager)



if __name__ == "__main__":
    root = tk.Tk()
    PlayerVsPlayer(root, root)
    root.mainloop()