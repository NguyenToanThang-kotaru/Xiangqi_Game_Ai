from model.game_model import GameModel
from view.menu_view import MainMenuView

class MenuController:
    def __init__(self, master, sound_manager):
        self.master = master
        self.view = MainMenuView(master, self)
        self.game_model = GameModel(sound_manager, master)

    def play_vs_ai(self, menu):
        self.game_model.start_vs_ai(menu)

    def play_vs_player(self, menu):
        self.game_model.start_vs_player(self.master, menu)

    def open_option_menu(self, menu):
        self.game_model.open_option_menu(menu)

    def logout(self, menu):
        import utils.config_font
        utils.config_font.change_gate(menu, self.master)

    def close_all(self, main_window):
        import utils.config_font
        utils.config_font.close_all(main_window)

    def display(self):
        self.view.display()
