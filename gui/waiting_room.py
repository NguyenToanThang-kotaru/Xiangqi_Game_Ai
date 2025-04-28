import tkinter as tk
import config_font
from sound_manager import SoundManager
from NetworkGame import NetworkGame
from network_manager import NetworkManager
import time

class WaitingRoom:
    def __init__(self, root, parent, main_window, sound_manager, is_host=False, room_info=None):
        self.root = root
        self.parent = parent
        self.main_window = main_window
        self.sound_manager = sound_manager
        self.is_host = is_host
        self.room_info = room_info or {}
        self.running = True
        
        # Frame chính
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(expand=True)

        # Tiêu đề
        title = tk.Label(
            self.frame, 
            text="Waiting Room" if is_host else "Join Room",
            font=config_font.get_font(20),
            fg="pink",
            bg="black"
        )
        title.pack(pady=30)

        # Thông tin phòng
        room_info_frame = tk.Frame(self.frame, bg="black")
        room_info_frame.pack(pady=20)

        if is_host:
            room_name_label = tk.Label(
                room_info_frame,
                text=f"Room: {self.room_info.get('name', 'Unknown')}",
                font=config_font.get_font(14),
                fg="white",
                bg="black"
            )
            room_name_label.pack(pady=10)

            time_label = tk.Label(
                room_info_frame,
                text=f"Time per move: {self.room_info.get('time_per_move', 'Unknown')} seconds",
                font=config_font.get_font(14),
                fg="white",
                bg="black"
            )
            time_label.pack(pady=10)

            # Trạng thái chờ
            self.status_label = tk.Label(
                self.frame,
                text="Waiting for other player to join...",
                font=config_font.get_font(14),
                fg="white",
                bg="black"
            )
            self.status_label.pack(pady=20)

            # Hiệu ứng loading
            self.loading_label = tk.Label(
                self.frame,
                text="",
                font=config_font.get_font(14),
                fg="gray",
                bg="black"
            )
            self.loading_label.pack(pady=10)

            # Nút hủy
            cancel_button = tk.Button(
                self.frame,
                text="Cancel",
                bg="#FF3399",
                fg="white",
                font=config_font.get_font(12),
                pady=8,
                padx=30,
                bd=0,
                relief="flat",
                cursor="hand2",
                command=self.cancel_waiting
            )
            cancel_button.pack(pady=30)

            # Bắt đầu hiệu ứng loading
            self.frame.after(500, self.animate_dots)
            self.dot_state = ""

            # Bắt đầu server
            self.start_server()
        else:
            # Frame chứa các trường nhập liệu
            input_frame = tk.Frame(self.frame, bg="black")
            input_frame.pack(pady=20)

            # Địa chỉ IP của máy chủ
            ip_label = tk.Label(
                input_frame,
                text="Server IP:",
                font=config_font.get_font(12),
                fg="white",
                bg="black"
            )
            ip_label.pack()
            self.ip_entry = tk.Entry(
                input_frame,
                font=config_font.get_font(12),
                bg="#333333",
                fg="white",
                insertbackground="white"
            )
            self.ip_entry.pack(pady=5)

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

            # Nút tham gia phòng
            join_button = tk.Button(
                button_frame,
                text="Join",
                bg="green",
                fg="white",
                font=config_font.get_font(14),
                pady=8,
                padx=30,
                bd=0,
                relief="flat",
                cursor="hand2",
                command=self.join_room
            )
            join_button.pack(pady=10)

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

    def start_server(self):
        self.network = NetworkManager(is_server=True)
        self.network.set_callback(self.handle_connection)
        server_ip = self.network.start_server()
        if server_ip is None:
            self.show_error("Failed to start server")
            return
        # Lưu IP của máy chủ vào room_info
        self.room_info['server_ip'] = server_ip
        print(f"Server started on {server_ip}:5000")

    def handle_connection(self, message):
        print(f"Server received message: {message}")
        if message.get('type') == 'join':
            # Kiểm tra mật khẩu
            if message.get('password') == self.room_info.get('password'):
                print("Password correct, accepting connection")
                # Chấp nhận kết nối và bắt đầu game
                self.network.send_message({
                    'type': 'accept',
                    'time_per_move': self.room_info.get('time_per_move')
                })
                # Đợi một chút để đảm bảo tin nhắn được gửi
                time.sleep(0.5)
                self.start_game(is_server=True)
            else:
                print("Password incorrect, rejecting connection")
                # Từ chối kết nối
                self.network.send_message({'type': 'reject', 'reason': 'Invalid password'})

    def join_room(self):
        self.sound_manager.play_click_sound()
        server_ip = self.ip_entry.get()
        password = self.password_entry.get()

        if not server_ip:
            self.show_error("Please enter server IP")
            return

        # Lưu thông tin phòng
        self.room_info = {
            'password': password,
            'server_ip': server_ip
        }

        # Kết nối với server
        self.network = NetworkManager(is_server=False, host=server_ip)
        self.network.set_callback(self.handle_join_response)
        
        if not self.network.connect_to_server():
            self.show_error("Failed to connect to server")
            return

        print("Sending join request...")
        # Gửi yêu cầu tham gia phòng
        self.network.send_message({
            'type': 'join',
            'password': password
        })

    def handle_join_response(self, message):
        print(f"Client received message: {message}")
        if message.get('type') == 'accept':
            print("Connection accepted, starting game")
            # Lưu thời gian cho mỗi nước đi
            self.room_info['time_per_move'] = message.get('time_per_move')
            # Đợi một chút để đảm bảo tin nhắn được xử lý
            time.sleep(0.5)
            self.start_game(is_server=False)
        elif message.get('type') == 'reject':
            print("Connection rejected")
            self.show_error(message.get('reason', 'Connection rejected'))

    def start_game(self, is_server):
        print(f"Starting game as {'server' if is_server else 'client'}")
        # Lưu network manager để truyền cho NetworkGame
        network = self.network
        self.running = False
        self.frame.pack_forget()
        # Không đóng kết nối ở đây, để NetworkGame quản lý
        NetworkGame(
            self.main_window,
            self.parent.menu,
            self.sound_manager,
            is_server=is_server,
            room_info=self.room_info,
            network=network  # Truyền network manager cho NetworkGame
        )

    def animate_dots(self):
        if not self.running:
            return
        self.dot_state += "."
        if len(self.dot_state) > 3:
            self.dot_state = ""
        self.loading_label.config(text=self.dot_state)
        self.frame.after(500, self.animate_dots)

    def cancel_waiting(self):
        self.running = False
        self.sound_manager.play_click_sound()
        if hasattr(self, 'network'):
            self.network.close()
        self.frame.pack_forget()
        self.parent.show_again()

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
