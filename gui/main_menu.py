import tkinter as tk
import config_font
import PlayvsAI
from option_menu import OptionMenu # Import OptionMenu từ file option_menu.py
from sound_manager import SoundManager

sound_manager = SoundManager()

def display_vsAI(menu, main_window):
    menu.withdraw()
    PlayvsAI.create_PlayvsAI(main_window,menu,sound_manager)

def display_option_menu(menu,main_window): # Hàm mở menu cài đặt
    OptionMenu(menu,main_window)
    
def openMenu(main_window):

    # pixel_font = font.Font(family="Press Start 2P", size=20)
    menu = tk.Toplevel()
    menu.title("Xiangqi")
    menu.geometry("800x440")
    menu.configure(bg="#333333")
    frameMenu=tk.Frame(menu,bg="#333333")
    config_font.center_window(menu, 800, 440)
    menu.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(main_window))
    # menu.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all_windows(login.window))

    class Option(tk.Button):
        def __init__(self,parent,text,command=None):
            super().__init__(
                            parent, bg="#333333",
                            text=text,fg="white",
                            font=config_font.get_font(16),pady=5,highlightthickness=0,padx=30,
                            bd=0,relief="flat",cursor="hand2",
                            command=lambda: [sound_manager.play_click_sound(), command()] if command else sound_manager.play_click_sound()
                            )
            self.pack() 

    
    frameMenu.pack()
    menu_label = tk.Label(
        frameMenu,text="Main Menu",bg="#333333",fg="#FF3399",pady=50,font=config_font.get_font(20))
    menu_label.pack()
    vs_ai_button = Option(frameMenu,"PLAY VS AI", lambda: display_vsAI(menu, main_window))
    #vs_ai_button.config(command=lambda: display_vsAI(menu, main_window))
    vs_player_button = Option(frameMenu,"PLAYER VS PLAYER")
    option_button = Option(frameMenu,"OPTION", lambda: display_option_menu(menu, main_window))
    #option_button.config(command=lambda: display_option_menu(menu,main_window)) # Gọi menu cài đặt
    logout_button = Option(frameMenu,"LOGOUT", lambda: config_font.change_gate(menu, main_window))
    #logout_button.config(command=lambda: config_font.change_gate(menu,main_window))
    menu.mainloop()
