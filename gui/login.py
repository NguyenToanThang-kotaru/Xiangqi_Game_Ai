import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.function_db.db_login import check_login
from main_menu import openMenu
import tkinter
import config_font 
from register import openRegister

window = tkinter.Tk()
window.title("Xiangqi")
window.geometry("800x440")
window.configure(bg="#333333")
frame=tkinter.Frame(window,bg="#333333")
frame_buttons = tkinter.Frame(frame, bg="#333333")
frame_buttons.grid(row=3, column=0, columnspan=2, pady=30)

config_font.center_window(window, 800, 440)


class AppState():
    flag_login = False



    
window.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(window))

def login(username_entry,password_entry):
    username = username_entry.get()
    password = password_entry.get()
    if check_login(username, password)==True:
        AppState.flag_login = True
    else:
        # WrongPassWord.grid(row=3,column=0,columnspan=2,sticky="s")
        AppState.flag_login = False
    display_menu()


frame.place(relx=0.5,rely=0.5,anchor="center")
#creating widgets
login_label = tkinter.Label(
    frame,text="Login",bg="#333333",fg="#FF3399",font=(config_font.get_font(16)))
username_label = tkinter.Label(
    frame,text="Username",bg="#333333",fg="white",font=(config_font.get_font(10)))

username_entry = tkinter.Entry(frame,font=(config_font.get_font(10)))
password_entry = tkinter.Entry(frame, show="*",font=(config_font.get_font(10)))

password_label = tkinter.Label(
    frame,text="Password",bg="#333333",fg="white",font=(config_font.get_font(10)))
login_button = tkinter.Button(
    frame_buttons, text="Login", bg="#FF3399", fg="white",
    font=(config_font.get_font(10)), pady=10, padx=30, bd=0, relief="flat", cursor="hand2",
    command=lambda: login(username_entry, password_entry)
)
register_button = tkinter.Button(
    frame_buttons, text="Register", bg="#FF3399", fg="white",
    font=(config_font.get_font(10)), pady=10, padx=30, bd=0, relief="flat", cursor="hand2",
    command=lambda: display_register()
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







    
login_button.bind("<Enter>", config_font.on_enter)
login_button.bind("<Leave>", config_font.on_leave)
register_button.bind("<Enter>", config_font.on_enter)
register_button.bind("<Leave>", config_font.on_leave)

def display_register():
    config_font.change_gate(window, openRegister(window))

def display_menu():
    WrongPassWord.grid_remove()
    if AppState.flag_login == True:
        config_font.reset_entry(username_entry)
        config_font.reset_entry(password_entry)
        config_font.change_gate(window, openMenu(window))
    else:
        WrongPassWord.grid(row=3,column=0,columnspan=2,sticky="s")

window.mainloop()