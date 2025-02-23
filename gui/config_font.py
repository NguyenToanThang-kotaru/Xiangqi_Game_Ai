import tkinter as tk
from tkinter import font

# Tạo biến font chung
root = tk.Tk()
root.withdraw()
pixel_font = font.Font(family="Press Start 2P", size=20)
pixel_font30 = font.Font(family="press Start 2P", size= 30)
pixel_font16 = font.Font(family="press Start 2P", size= 16)
pixel_font10 = font.Font(family="press Start 2P", size= 10)
def get_font(Newsize):
    new_font = pixel_font.copy()
    new_font.configure(size=Newsize)  
    return new_font