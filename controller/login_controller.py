from model.login_model import LoginModel
from view.login_view import LoginView
from controller.menu_controller import MenuController
from view.register import openRegister
from view.sound_manager import SoundManager
from appState import AppState

class LoginController:
    def __init__(self, root):
        self.root = root
        self.model = LoginModel()
        self.view = LoginView(root)
        self.sound_manager = SoundManager()
        self.sound_on = True

        self.view.login_button.config(command=self.handle_login)
        self.view.register_button.config(command=self.handle_register)

        # Âm thanh
        self.sound_button = self.create_sound_button()
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def handle_login(self):
        self.sound_manager.play_click_sound()
        username = self.view.get_username()
        password = self.view.get_password()
        self.model.set_credentials(username, password)
        success = self.model.authenticate()

        if success:
            self.view.hide_error()
            self.view.reset_entries()
            self.root.withdraw()
            menu_controller = MenuController(self.root, self.sound_manager)
            menu_controller.display()
        else:
            self.view.show_error()

    def handle_register(self):
        self.sound_manager.play_click_sound()
        self.root.withdraw()
        openRegister(self.root)

    def create_sound_button(self):
        import tkinter as tk
        btn = tk.Button(self.root, text="🔊 Sound On", bg="#FF3399", fg="white",
                        font=("Arial", 10), bd=0, relief="flat", cursor="hand2",
                        command=self.toggle_sound)
        btn.pack(side="bottom", anchor="w", padx=20, pady=20)
        return btn

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        AppState.sound_on = self.sound_on
        if self.sound_on:
            self.sound_button.config(text="🔊 Sound On")
            self.sound_manager.unmute()
        else:
            self.sound_button.config(text="🔇 Sound Off")
            self.sound_manager.mute()
            self.sound_manager.set_music_volume(0)
        self.sound_manager.play_click_sound()

    def quit_app(self):
        import utils.config_font
        utils.config_font.close_all(self.root)
