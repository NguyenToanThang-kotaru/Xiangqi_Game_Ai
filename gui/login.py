import tkinter

window = tkinter.Tk()
window.title("Xiangqi")
window.geometry("800x440")
window.configure(bg="#333333")
frame=tkinter.Frame(bg="#333333")

def login():
    username = 'admin'
    password = '123456'
    if username_entry.get() == username and password_entry.get() == password:
        print("Login successful")

frame.place(relx=0.5,rely=0.5,anchor="center")

#creating widgets
login_label = tkinter.Label(
    frame,text="Login",bg="#333333",fg="#FF3399",font=("Roboto",30))
username_label = tkinter.Label(
    frame,text="Username",bg="#333333",fg="white",font=("Roboto",16))

username_entry = tkinter.Entry(frame,font=("Roboto",16))
password_entry = tkinter.Entry(frame, show="*",font=("Roboto",16))

password_label = tkinter.Label(
    frame,text="Password",bg="#333333",fg="white",font=("Roboto",16))
login_button = tkinter.Button(
    frame,text="Login",bg="#FF3399",fg="white",font=("Roboto",10,"bold"),
    pady=10,padx=30,bd=0,relief="flat",cursor="hand2",
    command = login)

#placing widgets on the screen
login_label.grid(row=0,column=0,columnspan=2,stick="nsew",pady=40)
username_label.grid(row=1,column=0,padx=5,sticky="e")
username_entry.grid(row=1,column=1,pady=20)
password_label.grid(row=2,column=0,padx=5,sticky="e")
password_entry.grid(row=2,column=1,pady=20)
login_button.grid(row=3,column=0,columnspan=2,pady=30,sticky="s")




def on_enter(e):
    login_button.config(bg="#DD2277")

def on_leave(e):
    login_button.config(bg="#FF3399")


    
login_button.bind("<Enter>", on_enter)
login_button.bind("<Leave>", on_leave)


window.mainloop()