import tkinter as tk
import config_font
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sound_manager import SoundManager

def create_PlayvsPlayer(main_window, main_menu, sound_manager):
    player_window = tk.Toplevel()
    player_window.title("Player vs Player")
    config_font.center_window(player_window, 800, 440)
    player_window.configure(bg="#333333")
    player_window.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(main_window))

    # Tiêu đề
    title = tk.Label(player_window, text="Player vs Player", 
                     font=config_font.get_font(20), fg="pink", bg="#333333")
    title.pack(pady=30)

    # Frame chứa các nút
    button_frame = tk.Frame(player_window, bg="#333333")
    button_frame.pack(pady=20)

    # Nút "Create"
    create_button = tk.Button(
        button_frame, text="Create", bg="green", fg="white",
        font=config_font.get_font(14), pady=12, padx=40, bd=0, relief="flat", cursor="hand2",
        command=lambda: [sound_manager.play_click_sound(), print("Tạo trận đấu giữa 2 người")]
    )
    create_button.pack(pady=10)

    # Nút "Search"
    search_button = tk.Button(
        button_frame, text="Search", bg="yellow", fg="black",
        font=config_font.get_font(14), pady=12, padx=40, bd=0, relief="flat", cursor="hand2",
        command=lambda: [sound_manager.play_click_sound(), print("Tìm kiếm trận đấu")]
    )
    search_button.pack(pady=10)

    # Nút "Back to Menu" — về lại menu sau login (main_menu)
    back_button = tk.Button(
        button_frame, text="Back to Menu", bg="#FF3399", fg="white",
        font=config_font.get_font(12), pady=8, padx=30, bd=0, relief="flat", cursor="hand2",
        command=lambda: [sound_manager.play_click_sound(), config_font.change_gate(player_window, main_menu)]
    )
    back_button.pack(pady=10)
