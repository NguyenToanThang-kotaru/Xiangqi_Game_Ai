import tkinter as tk
import config_font
from sound_manager import SoundManager
import socket
import threading
import json
from online_game import OnlineGame

class JoinRoom:
    def __init__(self, parent_window, main_window, sound_manager):
        self.parent = parent_window
        self.main_window = main_window
        self.sound_manager = sound_manager
        
        self.frame = tk.Frame(self.parent, bg="black")
        self.frame.pack(expand=True)
        
        title = tk.Label(self.frame, text="Tham Gia Phòng",
                        font=config_font.get_font(20), fg="pink", bg="black")
        title.pack(pady=30)
        
        # Frame chứa các trường nhập liệu
        input_frame = tk.Frame(self.frame, bg="black")
        input_frame.pack(pady=20)
        
        # IP Address
        ip_label = tk.Label(input_frame, text="IP Phòng:",
                          font=config_font.get_font(12), fg="white", bg="black")
        ip_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        
        self.ip_entry = tk.Entry(input_frame, font=config_font.get_font(12),
                               bg="#333333", fg="white", insertbackground="white")
        self.ip_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Mật khẩu phòng
        password_label = tk.Label(input_frame, text="Mật khẩu:",
                                font=config_font.get_font(12), fg="white", bg="black")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        
        self.password_entry = tk.Entry(input_frame, font=config_font.get_font(12),
                                     bg="#333333", fg="white", insertbackground="white",
                                     show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Nút kết nối
        connect_button = tk.Button(
            self.frame, text="Kết Nối", bg="#FF3399", fg="white",
            font=config_font.get_font(12), pady=8, padx=30, bd=0, relief="flat", cursor="hand2",
            command=self.connect_to_room
        )
        connect_button.pack(pady=20)
        
        # Nút quay lại
        back_button = tk.Button(
            self.frame, text="Quay Lại", bg="#333333", fg="white",
            font=config_font.get_font(12), pady=8, padx=30, bd=0, relief="flat", cursor="hand2",
            command=self.go_back
        )
        back_button.pack(pady=10)
        
        # Label hiển thị trạng thái kết nối
        self.status_label = tk.Label(
            self.frame, text="", font=config_font.get_font(12),
            fg="white", bg="black"
        )
        self.status_label.pack(pady=10)
        
    def connect_to_room(self):
        self.sound_manager.play_click_sound()
        ip = self.ip_entry.get()
        password = self.password_entry.get()
        
        if not ip or not password:
            self.status_label.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
            return
            
        try:
            # Tạo socket và kết nối
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5.0)  # Đặt timeout cho kết nối
            client_socket.connect((ip, 12345))  # Port mặc định
            
            # Gửi thông tin đăng nhập dưới dạng JSON
            login_data = {
                "type": "JOIN",
                "password": password
            }
            client_socket.send(json.dumps(login_data).encode())
            
            # Nhận phản hồi từ server
            response = client_socket.recv(4096).decode()
            if not response:
                raise Exception("Không nhận được phản hồi từ server")
                
            response_data = json.loads(response)
            
            if response_data["type"] == "CONNECT" and response_data["status"] == "SUCCESS":
                self.status_label.config(text="Kết nối thành công!", fg="green")
                # Lưu socket vào main_window để sử dụng sau này
                self.main_window.client_socket = client_socket
                # Đóng cửa sổ tham gia phòng
                self.frame.destroy()
                # Mở màn hình chơi game
                self.start_game(client_socket)
            else:
                self.status_label.config(text="Sai mật khẩu hoặc phòng không tồn tại!", fg="red")
                client_socket.close()
                
        except socket.timeout:
            self.status_label.config(text="Kết nối timeout!", fg="red")
        except json.JSONDecodeError as e:
            self.status_label.config(text=f"Lỗi dữ liệu: {str(e)}", fg="red")
        except Exception as e:
            self.status_label.config(text=f"Lỗi kết nối: {str(e)}", fg="red")
            
    def start_game(self, client_socket):
        # Tạo cửa sổ game mới
        game_window = tk.Toplevel(self.parent)
        game_window.title("Cờ Tướng Online")
        game_window.geometry("400x500")
        config_font.center_window(game_window, 400, 500)
        
        # Khởi tạo game online (is_host=False vì đây là người tham gia)
        OnlineGame(game_window, client_socket, False, self.main_window, self.sound_manager)
        
    def go_back(self):
        self.sound_manager.play_click_sound()
        self.frame.destroy()
        if hasattr(self.main_window, "show_again"):
            self.main_window.show_again() 