import tkinter as tk

class BoardView:
    def __init__(self, window):
        self.window = window
        self.canvas = tk.Canvas(window, height=425, width=400, highlightthickness=0)
        self.canvas.configure(bg="#333333")
        self.canvas.pack()

    def create_back_button(self, command):
        back_button = tk.Button(self.window, text="Back to Menu", command=command)
        back_button.place(x=10)
