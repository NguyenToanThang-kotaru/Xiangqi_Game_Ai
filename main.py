import tkinter as tk

# Tạo cửa sổ chính
window = tk.Tk()
window.title("Xiangqi - Login")
window.geometry("350x500")
window.configure(bg="#222222")

# Tạo Frame chính
frame = tk.Frame(window, bg="#333333", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor="center")  # Căn giữa frame

# Tạo tiêu đề
login_label = tk.Label(
    frame, text="Login", bg="#333333", fg="#FF3399", font=("Roboto", 30, "bold")
)
login_label.grid(row=0, column=0, columnspan=2, pady=20)

# Nhãn & Ô nhập Username
username_label = tk.Label(
    frame, text="Username:", bg="#333333", fg="white", font=("Roboto", 14)
)
username_label.grid(row=1, column=0, sticky="w", pady=10)
username_entry = tk.Entry(frame, font=("Roboto", 14), width=20, bd=2, relief="ridge")
username_entry.grid(row=1, column=1, pady=10)

# Nhãn & Ô nhập Password
password_label = tk.Label(
    frame, text="Password:", bg="#333333", fg="white", font=("Roboto", 14)
)
password_label.grid(row=2, column=0, sticky="w", pady=10)
password_entry = tk.Entry(frame, show="*", font=("Roboto", 14), width=20, bd=2, relief="ridge")
password_entry.grid(row=2, column=1, pady=10)

# Nút đăng nhập với hiệu ứng hover
def on_enter(e):
    login_button.config(bg="#DD2277")

def on_leave(e):
    login_button.config(bg="#FF3399")

login_button = tk.Button(
    frame,
    text="Login",
    bg="#FF3399",
    fg="white",
    font=("Roboto", 12, "bold"),
    padx=10,
    pady=5,
    bd=0,
    relief="flat",
    cursor="hand2"
)
login_button.grid(row=3, column=0, columnspan=2, pady=20, ipadx=50)

# Thêm hiệu ứng hover
login_button.bind("<Enter>", on_enter)
login_button.bind("<Leave>", on_leave)

# Chạy giao diện
window.mainloop()
