from tkinter import font
from tkinter import *
def get_font(size):
    return font.Font(family="Press Start 2P", size=size)

def init_window(geometry, bg, title):
    window = Tk()
    window.geometry(geometry)
    window.configure(bg=bg)
    window.title(title)
    return window

def init_frame(parent, bg, padx, pady):
    frame = Frame(parent, bg=bg, padx=padx, pady=pady)
    return frame


def init_toplevel(geometry, bg, title):
    window = Toplevel()
    window.geometry(geometry)
    window.configure(bg=bg)
    window.title(title)
    return window



def center_window(window, width=800, height=440):
    # Lấy kích thước màn hình
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Tính toán vị trí để căn giữa
    x = (screen_width - width) // 2
    y = (screen_height - height-50) // 2
    
    # Đặt vị trí cửa sổ
    window.geometry(f"{width}x{height}+{x}+{y}")
    

def close_all(window,main_window=None):

    # Đóng cửa sổ menu
    window.destroy()
    if main_window:
        main_window.quit()
        main_window.destroy()

def reset_entry(entry):
    entry.delete(0, 'end')
    entry.insert(0, "")