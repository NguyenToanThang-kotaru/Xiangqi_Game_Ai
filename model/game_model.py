class GameModel:
    def __init__(self, sound_manager, main_window):
        self.main_window = main_window
        self.sound_manager = sound_manager

    def start_vs_ai(self, menu):
        import view.PlayvsAI
        view.PlayvsAI.create_PlayvsAI(self.main_window, menu, self.sound_manager)

    def start_vs_player(self, menu):
        import view.PlayervsPlayer
        view.PlayervsPlayer.create_PlayervsPlayer(self.main_window, menu)

    def open_option_menu(self, menu):
        import view.option_menu
        view.option_menu.OptionMenu(menu, self.main_window)
