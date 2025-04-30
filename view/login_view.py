import tkinter as tk
from utils import config_font

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Xiangqi")
        self.root.geometry("800x440")
        self.root.configure(bg="#333333")
        config_font.center_window(self.root, 800, 440)

        self.frame = tk.Frame(self.root, bg="#333333")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.frame_buttons = tk.Frame(self.frame, bg="#333333")
        self.frame_buttons.grid(row=3, column=0, columnspan=2, pady=30)

        self.login_label = tk.Label(self.frame, text="Login", bg="#333333", fg="#FF3399",
                                    font=(config_font.get_font(16)))
        self.username_label = tk.Label(self.frame, text="Username", bg="#333333", fg="white",
                                       font=(config_font.get_font(10)))
        self.password_label = tk.Label(self.frame, text="Password", bg="#333333", fg="white",
                                       font=(config_font.get_font(10)))

        self.username_entry = tk.Entry(self.frame, font=(config_font.get_font(10)))
        self.password_entry = tk.Entry(self.frame, show="*", font=(config_font.get_font(10)))

        self.login_button = tk.Button(self.frame_buttons, text="Login", bg="#FF3399", fg="white",
                                      font=(config_font.get_font(10)), pady=10, padx=30, bd=0,
                                      relief="flat", cursor="hand2")
        self.register_button = tk.Button(self.frame_buttons, text="Register", bg="#FF3399", fg="white",
                                         font=(config_font.get_font(10)), pady=10, padx=30, bd=0,
                                         relief="flat", cursor="hand2")
        self.wrong_label = tk.Label(self.frame, text="Incorrect username or password", bg="#333333",
                                    fg="white", font=(config_font.get_font(10)))

        self.login_label.grid(row=0, column=0, columnspan=2, pady=40)
        self.username_label.grid(row=1, column=0, padx=5, sticky="e")
        self.username_entry.grid(row=1, column=1, pady=20)
        self.password_label.grid(row=2, column=0, padx=5, sticky="e")
        self.password_entry.grid(row=2, column=1, pady=20)

        self.login_button.pack(side="left", padx=10)
        self.register_button.pack(side="right", padx=10)

    def get_username(self):
        return self.username_entry.get()

    def get_password(self):
        return self.password_entry.get()

    def show_error(self):
        self.wrong_label.grid(row=3, column=0, columnspan=2, sticky="s")

    def hide_error(self):
        self.wrong_label.grid_remove()

    def reset_entries(self):
        config_font.reset_entry(self.username_entry)
        config_font.reset_entry(self.password_entry)
