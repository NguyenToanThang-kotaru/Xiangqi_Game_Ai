import tkinter as tk
from controller.login_controller import LoginController

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginController(root)
    root.mainloop()
