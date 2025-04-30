import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.function_db.db_login import check_login
from appState import AppState

class LoginModel:
    def __init__(self):
        self.username = ""
        self.password = ""

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self):
        if check_login(self.username, self.password):
            AppState.flag_login = True
            return True
        else:
            AppState.flag_login = False
            return False
