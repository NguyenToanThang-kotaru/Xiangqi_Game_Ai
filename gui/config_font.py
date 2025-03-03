from tkinter import font
from tkinter import *
def get_font(size):
    return font.Font(family="Press Start 2P", size=size)


def init_frame(parent, bg, padx=None, pady=None):
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
    

def close_all(window, main_window=None):
    window.destroy()
    if main_window and main_window.winfo_exists():
        main_window.deiconify()

def change_gate(window, new_window):
    if window.winfo_exists():  # ✅ Kiểm tra nếu cửa sổ vẫn còn tồn tại
        window.withdraw()
    new_window.deiconify()



def reset_entry(entry):
    entry.delete(0, 'end')
    entry.insert(0, "")
    
def on_enter(e):
    e.widget.config(bg="#DD2277")

def on_leave(e):
    e.widget.config(bg="#FF3399")