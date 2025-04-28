import tkinter as tk
import config_font
from sound_manager import SoundManager
from waiting_room import WaitingRoom

class CreateRoomForm:
    def __init__(self, root, parent, sound_manager):
        self.root = root
        self.parent = parent
        self.sound_manager = sound_manager
        
        # Frame chính
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(expand=True)

        # Tiêu đề
        title = tk.Label(
            self.frame, 
            text="Create Room",
            font=config_font.get_font(20),
            fg="pink",
            bg="black"
        )
        title.pack(pady=30)

        # Frame chứa các trường nhập liệu
        input_frame = tk.Frame(self.frame, bg="black")
        input_frame.pack(pady=20)

        # Tên phòng
        room_name_label = tk.Label(
            input_frame,
            text="Room Name:",
            font=config_font.get_font(12),
            fg="white",
            bg="black"
        )
        room_name_label.pack()
        self.room_name_entry = tk.Entry(
            input_frame,
            font=config_font.get_font(12),
            bg="#333333",
            fg="white",
            insertbackground="white"
        )
        self.room_name_entry.pack(pady=5)

        # Thời gian cho mỗi nước đi
        time_label = tk.Label(
            input_frame,
            text="Time per move (seconds):",
            font=config_font.get_font(12),
            fg="white",
            bg="black"
        )
        time_label.pack()
        self.time_entry = tk.Entry(
            input_frame,
            font=config_font.get_font(12),
            bg="#333333",
            fg="white",
            insertbackground="white"
        )
        self.time_entry.pack(pady=5)

        # Mật khẩu
        password_label = tk.Label(
            input_frame,
            text="Password:",
            font=config_font.get_font(12),
            fg="white",
            bg="black"
        )
        password_label.pack()
        self.password_entry = tk.Entry(
            input_frame,
            font=config_font.get_font(12),
            bg="#333333",
            fg="white",
            insertbackground="white",
            show="*"
        )
        self.password_entry.pack(pady=5)

        # Frame chứa nút
        button_frame = tk.Frame(self.frame, bg="black")
        button_frame.pack(pady=20)

        # Nút tạo phòng
        create_button = tk.Button(
            button_frame,
            text="Create",
            bg="green",
            fg="white",
            font=config_font.get_font(14),
            pady=8,
            padx=30,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.create_room
        )
        create_button.pack(pady=10)

        # Nút quay lại
        back_button = tk.Button(
            button_frame,
            text="Back",
            bg="#FF3399",
            fg="white",
            font=config_font.get_font(12),
            pady=8,
            padx=30,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.back
        )
        back_button.pack(pady=10)

    def create_room(self):
        self.sound_manager.play_click_sound()
        room_name = self.room_name_entry.get()
        time_per_move = self.time_entry.get()
        password = self.password_entry.get()

        if not room_name:
            self.show_error("Please enter room name")
            return

        try:
            time_per_move = int(time_per_move)
            if time_per_move <= 0:
                raise ValueError
        except ValueError:
            self.show_error("Time per move must be a positive number")
            return

        # Lưu thông tin phòng
        self.room_info = {
            'name': room_name,
            'time_per_move': time_per_move,
            'password': password
        }

        # Chuyển sang giao diện chờ
        self.frame.pack_forget()
        WaitingRoom(
            self.root,
            self.parent,
            self.parent.main_window,
            self.sound_manager,
            is_host=True,
            room_info=self.room_info
        )

    def back(self):
        self.sound_manager.play_click_sound()
        self.frame.pack_forget()
        self.parent.show_again()

    def show_error(self, message):
        error_label = tk.Label(
            self.frame,
            text=message,
            fg="red",
            bg="black",
            font=config_font.get_font(12)
        )
        error_label.pack(pady=10)

   
