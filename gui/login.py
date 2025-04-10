import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.function_db.db_login import check_login
from main_menu import openMenu
import tkinter
import config_font 
from register import openRegister
from sound_manager import SoundManager
from tkinter import PhotoImage
from appState import AppState
                    
window = tkinter.Tk()
window.title("Xiangqi")
window.geometry("800x440")
window.configure(bg="#333333")
frame=tkinter.Frame(window,bg="#333333")
frame_buttons = tkinter.Frame(frame, bg="#333333")
frame_buttons.grid(row=3, column=0, columnspan=2, pady=30)
config_font.center_window(window, 800, 440)


# Khởi tạo quản lý âm thanh
sound_manager = SoundManager()
        
window.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(window))

def login(username_entry,password_entry):
    username = username_entry.get()
    password = password_entry.get()
    if check_login(username, password)==True:
        AppState.flag_login = True
    else:
        # WrongPassWord.grid(row=3,column=0,columnspan=2,sticky="s")
        AppState.flag_login = False
    display_menu(AppState.flag_login)


frame.place(relx=0.5,rely=0.5,anchor="center")
#creating widgets
login_label = tkinter.Label(
    frame,text="Login",bg="#333333",fg="#FF3399",font=(config_font.get_font(16)))
username_label = tkinter.Label(
    frame,text= "Username",bg="#333333",fg="white",font=(config_font.get_font(10)))

username_entry = tkinter.Entry(frame,font=(config_font.get_font(10)))
password_entry = tkinter.Entry(frame, show="*",font=(config_font.get_font(10)))

password_label = tkinter.Label(
    frame,text="Password",bg="#333333",fg="white",font=(config_font.get_font(10)))
login_button = tkinter.Button(
    frame_buttons, text="Login", bg="#FF3399", fg="white",
    font=(config_font.get_font(10)), pady=10, padx=30, bd=0, relief="flat", cursor="hand2",
    command=lambda: [sound_manager.play_click_sound(), login(username_entry, password_entry)]
)
register_button = tkinter.Button(
    frame_buttons, text="Register", bg="#FF3399", fg="white",
    font=(config_font.get_font(10)), pady=10, padx=30, bd=0, relief="flat", cursor="hand2",
    command=lambda: [sound_manager.play_click_sound(), display_register()]
)
# login_button = tkinter.Button(
#     frame,text="Login",bg="#FF3399",fg="white",font=(config_font.get_font(10)),
#     pady=10,padx=30,bd=0,relief="flat",cursor="hand2",
#     command = login)
# register_button = tkinter.Button(
#     frame,text="Register",bg="#FF3399",fg="white",font=(config_font.get_font(10)),
#     pady=10,padx=30,bd=0,relief="flat",cursor="hand2")
WrongPassWord = tkinter.Label(
    frame,text="Incorrect your username or password",bg="#333333",fg="white",font=(config_font.get_font(10))
)


#placing widgets on the screenz
login_label.grid(row=0,column=0,columnspan=2,sticky="nsew",pady=40)
username_label.grid(row=1,column=0,padx=5,sticky="e")
username_entry.grid(row=1,column=1,pady=20)
password_label.grid(row=2,column=0,padx=5,sticky="e")
password_entry.grid(row=2,column=1,pady=20)
# Đặt nút vào trong frame_buttons
login_button.pack(side="left", padx=10)
register_button.pack(side="right", padx=10)

# Biến lưu trạng thái âm thanh (True: bật, False: tắt)
sound_on = True


def toggle_sound():
    global sound_on
    sound_on = not sound_on
    AppState.sound_on = sound_on # Đồng bộ AppState
    if sound_on:
        sound_button.config(text="🔊 Sound On")
        sound_manager.unmute() # Bật âm thanh
    else:
        sound_button.config(text="🔇 Sound Off")
        sound_manager.mute() # Tắt âm thanh
        sound_manager.set_music_volume(0)
    sound_manager.play_click_sound()

sound_button = tkinter.Button(
    window, text="🔊 Sound On", bg="#FF3399", fg="white",
    font=(config_font.get_font(10)), bd=0, relief="flat", cursor="hand2",
    command=toggle_sound
)

sound_button.pack(side="bottom", anchor="w", padx=20, pady=20) # Đặt ở góc dưới bên trái






    
login_button.bind("<Enter>", config_font.on_enter)
login_button.bind("<Leave>", config_font.on_leave)
register_button.bind("<Enter>", config_font.on_enter)
register_button.bind("<Leave>", config_font.on_leave)

def display_register():
    window.withdraw()
    openRegister(window)

def display_menu(flag):
    WrongPassWord.grid_remove()
    if flag == True:
        config_font.reset_entry(username_entry)
        config_font.reset_entry(password_entry)
        window.withdraw()
        openMenu(window)

        if AppState.sound_on:
            sound_button.config(text="🔊 Sound On")
            sound_manager.unmute()
        else:
            sound_button.config(text="🔇 Sound Off")
            sound_manager.mute()
    else:
        WrongPassWord.grid(row=3,column=0,columnspan=2,sticky="s")

window.mainloop()