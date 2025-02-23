import tkinter as tk
from config_font import pixel_font

def openMenu():
    # pixel_font = font.Font(family="Press Start 2P", size=20)
    menu = tk.Toplevel()
    menu.title("Xiangq")
    menu.geometry("800x440")
    menu.configure(bg="#333333")
    frameMenu=tk.Frame(menu,bg="#333333")

    class Option(tk.Button):
        def __init__(self,parent,text):
            super().__init__(
                            parent, bg="#333333",
                            text=text,fg="white",
                            font=(pixel_font),pady=5,padx=30,
                            bd=0,relief="flat",cursor="hand2")
            self.pack()

    
    frameMenu.pack()
    menu_label = tk.Label(
        frameMenu,text="Main Menu",bg="#333333",fg="#FF3399",pady=50,font=(pixel_font))
    menu_label.pack()
    vs_ai_button = Option(frameMenu,"PLAY VS AI")
    vs_player_button = Option(frameMenu,"PLAYER VS PLAYER")
    option_button = Option(frameMenu,"OPTION")
    logout_button = Option(frameMenu,"LOGOUT")
    menu.mainloop()
