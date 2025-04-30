import tkinter as tk
from utils import config_font

class MainMenuView:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.menu = None
    def display(self):
        self.menu = tk.Toplevel(self.master)
        self.menu.title("Xiangqi")
        self.menu.geometry("800x440")
        self.menu.configure(bg="#333333")
        frameMenu = tk.Frame(self.menu, bg="#333333")
        config_font.center_window(self.menu, 800, 440)
        self.menu.protocol("WM_DELETE_WINDOW", lambda: self.controller.close_all(self.master))

        menu_label = tk.Label(frameMenu, text="Main Menu", bg="#333333", fg="#FF3399", pady=50, font=config_font.get_font(20))
        menu_label.pack()

        vs_ai_button = tk.Button(frameMenu, text="PLAY VS AI", bg="#333333", fg="white", font=config_font.get_font(16), pady=5,
                                 highlightthickness=0, padx=30, bd=0, relief="flat", cursor="hand2",
                                 command=lambda: [self.controller.play_vs_ai(self.menu)])
        vs_ai_button.pack()

        vs_player_button = tk.Button(frameMenu, text="PLAYER VS PLAYER", bg="#333333", fg="white", font=config_font.get_font(16), pady=5,
                                     highlightthickness=0, padx=30, bd=0, relief="flat", cursor="hand2",
                                     command=lambda: [self.controller.play_vs_player(self.menu)])
        vs_player_button.pack()

        option_button = tk.Button(frameMenu, text="OPTION", bg="#333333", fg="white", font=config_font.get_font(16), pady=5,
                                  highlightthickness=0, padx=30, bd=0, relief="flat", cursor="hand2",
                                  command=lambda: [self.controller.open_option_menu(self.menu)])
        option_button.pack()

        logout_button = tk.Button(frameMenu, text="LOGOUT", bg="#333333", fg="white", font=config_font.get_font(16), pady=5,
                                  highlightthickness=0, padx=30, bd=0, relief="flat", cursor="hand2",
                                  command=lambda: [self.controller.logout(self.menu)])
        logout_button.pack()

        frameMenu.pack()
        self.menu.mainloop()
