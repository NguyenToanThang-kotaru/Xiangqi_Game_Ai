import tkinter as tk
import config_font
from database.function_db.db_regis import check_username, check_password, add_account
from sound_manager import SoundManager

sound_manager = SoundManager()

# Initialize the labels as None
UsedUsername = None
WrongPassword = None
BlankUsername = None
BlankPassword = None

# add new accounts
def register(username, password, repassword, register_window, main_window):
    global UsedUsername, WrongPassword, BlankUsername, BlankPassword
    if UsedUsername:
        UsedUsername.grid_remove()
    if WrongPassword:
        WrongPassword.grid_remove()
    if BlankUsername:
        BlankUsername.grid_remove()
    if BlankPassword:
        BlankPassword.grid_remove()

    user = username.get()
    pw = password.get()
    re_pw = repassword.get()

    if user == '':
        BlankUsername.grid(row=5, column=0, columnspan = 2, sticky="s")
        return
    if pw == '' or re_pw == '':
        BlankPassword.grid(row=5, column=0, columnspan = 2, sticky="s")
        return

    if check_password(pw, re_pw):
        # if the username is unique
        if not check_username(user):
            add_account(user, pw)
            config_font.reset_entry(username)
            config_font.reset_entry(password)
            config_font.reset_entry(repassword)
            config_font.change_gate(register_window, main_window)
        else:
            # print the error message
            UsedUsername.grid(row=5, column=0, columnspan=2, sticky="s")
    else:
        WrongPassword.grid(row=5, column=0, columnspan=2, sticky="s")

# create register window
def openRegister(main_window): 
    global UsedUsername, WrongPassword, BlankUsername, BlankPassword
    register_window = config_font.init_toplevel("800x440", "#333333", "Register")
    config_font.center_window(register_window, 800, 440)
    register_window.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(main_window))
    register_frame = config_font.init_frame(register_window, "#333333", 10, 10)
    register_frame.place(relx=0.5, rely=0.4, anchor="center") 
    button_frame = config_font.init_frame(register_frame, "#333333")
    button_frame.grid(row=4, column=0, columnspan=2, pady=30)
    fontpixel = config_font.get_font(16)
    register_label = tk.Label(
        register_frame, text="Register", bg="#333333", fg="#FF3399", font=config_font.get_font(16))

    username_label = tk.Label(
        register_frame, text="Username", bg="#333333", fg="white", font=config_font.get_font(10))
    username_entry = tk.Entry(register_frame, font=config_font.get_font(10))
    password_label = tk.Label(
        register_frame, text="Password", bg="#333333", fg="white", font=config_font.get_font(10))
    password_entry = tk.Entry(register_frame, show="*", font=config_font.get_font(10))
    re_password_label = tk.Label(
        register_frame, text="Re-Password", bg="#333333", fg="white", font=config_font.get_font(10))
    re_password_entry = tk.Entry(register_frame, show="*", font=config_font.get_font(10))

    register_button = tk.Button(
        button_frame, text="Register", bg="#FF3399", fg="white",
        font=config_font.get_font(10), pady=10, padx=30, bd=0, relief="flat", cursor="hand2",
        command=lambda: [sound_manager.play_click_sound(), register(username_entry, password_entry, re_password_entry, register_window, main_window)]
    )

    cancel_button = tk.Button(
        button_frame, text="Cancel", bg="#FF3399", fg="white",
        font=config_font.get_font(10), pady=10, padx=30, bd=0, relief="flat", cursor="hand2",
        command=lambda: [sound_manager.play_click_sound(), config_font.change_gate(register_window, main_window)]
    )

    register_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=40)
    username_label.grid(row=1, column=0, padx=5, sticky="w")
    username_entry.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0, padx=5, sticky="w")
    password_entry.grid(row=2, column=1, pady=20)
    re_password_label.grid(row=3, column=0, padx=5, sticky="e")
    re_password_entry.grid(row=3, column=1, pady=20)
    register_button.pack(side="left", padx=10)
    cancel_button.pack(side="right", padx=10)

    register_button.bind("<Enter>", config_font.on_enter)
    register_button.bind("<Leave>", config_font.on_leave)
    cancel_button.bind("<Enter>", config_font.on_enter)
    cancel_button.bind("<Leave>", config_font.on_leave)

    # Initialize the error labels after the root window is created
    WrongPassword = tk.Label(
        register_frame, text="Password and re-password are not same", bg="#333333", fg="white", font=config_font.get_font(10)
    )

    UsedUsername = tk.Label(
        register_frame, text="Your username is taken", bg="#333333", fg="white", font=config_font.get_font(10)
    )

    BlankUsername = tk.Label(
        register_frame, text="Please enter your username", bg="#333333", fg="white", font=config_font.get_font(10)
    )

    BlankPassword = tk.Label(
        register_frame, text="Please enter your password", bg="#333333", fg="white", font=config_font.get_font(10)
    )

    register_window.mainloop()
