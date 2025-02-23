import tkinter as tk

def openMenu():
    menu = tk.Tk()
    menu.title("Xiangqi")
    menu.geometry("800x440")
    menu.configure(bg="#333333")
    frameMenu=tk.Frame(bg="#333333")
    
    class Option(tk.Frame):
        def __init__(self,parent,text):
            super().__init__(parent, bg="#FF3399"),
            text=text,fg="white",
            font=("Roboto",10,"bold"),pady=10,padx=30,
            bd=0,relief="flat",cursor="hand2"


    
    frameMenu.pack()
    menu_label = tk.Label(
        frameMenu,text="Main Menu",bg="#333333",fg="#FF3399",font=("Roboto",30))
    vs_ai_button = Option(frameMenu,"Play vs AI")
    

    menu_label.grid(row=0,column=0,columnspan=2,stick="nsew",pady=40)

    menu.mainloop()
    
openMenu()