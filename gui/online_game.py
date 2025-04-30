import tkinter as tk
import config_font
from game.board import Board
from game.Piece import Piece
from sound_manager import SoundManager
import threading
import json
import time
import socket

class OnlineGame:
    def __init__(self, parent_window, client_socket, is_host, main_window, sound_manager):
        self.parent = parent_window
        self.client_socket = client_socket
        self.is_host = is_host
        self.main_window = main_window
        self.sound_manager = sound_manager
        self.running = True
        
        # Thiết lập kích thước cửa sổ
        self.parent.geometry("500x600")
        self.parent.title("Cờ Tướng Online")
        self.parent.configure(bg="#F0F0F0")
        
        # Frame chứa bàn cờ
        self.board_frame = tk.Frame(self.parent, bg="#F0F0F0")
        self.board_frame.pack(pady=20)
        
        # Tạo canvas cho bàn cờ với kích thước phù hợp
        self.canvas = tk.Canvas(self.board_frame, width=400, height=440, bg="#E8C887", highlightthickness=2, highlightbackground="#8B4513")
        self.canvas.pack()
        
        # Khởi tạo bàn cờ với mode ONLINE
        self.board = Board(self.canvas, "ONLINE")
        self.board.client_socket = client_socket
        self.board.is_host = is_host
        
        # Thiết lập vị trí quân cờ dựa trên vai trò (host/client)
        if is_host:
            self.board.setup_board(red_bottom=True)  # Server: quân đỏ ở dưới
        else:
            self.board.setup_board(red_bottom=False)  # Client: quân đen ở dưới
        
        # Vẽ lại bàn cờ với màu sắc và kích thước giống board.py
        self.canvas.delete("all")
        self.board.draw_board()
        self.board.load_images()
        self.board.place_pieces()
        
        # Frame chứa thông tin và nút
        self.info_frame = tk.Frame(self.parent, bg="#F0F0F0")
        self.info_frame.pack(pady=10)
        
        # Label hiển thị lượt đi
        self.turn_label = tk.Label(
            self.info_frame, 
            text="Lượt của bạn" if is_host else "Đợi đối phương",
            font=config_font.get_font(14, "bold"),
            fg="#8B4513",
            bg="#F0F0F0"
        )
        self.turn_label.pack(pady=5)
        
        # Nút đầu hàng
        self.surrender_button = tk.Button(
            self.info_frame,
            text="Đầu Hàng",
            bg="#8B4513",
            fg="white",
            font=config_font.get_font(12),
            pady=8,
            padx=30,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.surrender
        )
        self.surrender_button.pack(pady=10)
        
        # Nếu không phải host, disable bàn cờ
        if not is_host:
            self.canvas.unbind("<Button-1>")
            self.turn_label.config(text="Đợi đối phương đi")
            
        # Tạo thread để nhận dữ liệu từ đối phương
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        
        # Thêm xử lý khi đóng cửa sổ
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        self.running = False
        self.close_connection()
        self.parent.destroy()
    
    def receive_data(self):
        while self.running:
            try:
                # Đặt timeout cho socket
                self.client_socket.settimeout(1.0)
                data = self.client_socket.recv(4096).decode()
                if not data:
                    print("Kết nối bị đóng")
                    break
                    
                try:
                    move_data = json.loads(data)
                    print(f"Nhận được dữ liệu: {move_data}")
                    
                    if move_data["type"] == "MOVE":
                        # Cập nhật bàn cờ
                        from_pos = move_data["from"]
                        to_pos = move_data["to"]
                        
                        # Tìm quân cờ tại vị trí from_pos
                        piece = self.board.get_piece_at(from_pos[0], from_pos[1])
                        if piece:
                            # Di chuyển quân cờ
                            if self.board.move_piece(piece, to_pos) == 1:  # Nếu di chuyển thành công
                                # Cập nhật lượt đi
                                self.turn_label.config(text="Lượt của bạn")
                                # Bật lại bàn cờ
                                self.canvas.bind("<Button-1>", self.board.on_click)
                                # Cập nhật lại bàn cờ
                                self.canvas.delete("all")
                                self.board.draw_board()
                                self.board.load_images()
                                self.board.place_pieces()
                                # Gửi dữ liệu di chuyển cho đối phương
                                self.send_move(from_pos, to_pos)
                            
                    elif move_data["type"] == "SURRENDER":
                        self.turn_label.config(text="Đối phương đã đầu hàng!")
                        self.canvas.unbind("<Button-1>")
                        
                except json.JSONDecodeError as e:
                    print(f"Lỗi giải mã JSON: {e}")
                except Exception as e:
                    print(f"Lỗi xử lý dữ liệu: {e}")
                
            except socket.timeout:
                continue
            except ConnectionResetError:
                print("Kết nối bị đóng đột ngột bởi đối phương")
                self.close_connection()
                break
            except Exception as e:
                print(f"Lỗi nhận dữ liệu: {e}")
                self.close_connection()
                break
                
        # Đóng kết nối khi thread kết thúc
        self.close_connection()
    
    def send_move(self, from_pos, to_pos):
        if not self.running:
            return
            
        try:
            move_data = {
                "type": "MOVE",
                "from": from_pos,
                "to": to_pos
            }
            json_data = json.dumps(move_data) + "\n"
            print(f"Gửi dữ liệu: {json_data}")
            self.client_socket.send(json_data.encode())
            
            # Cập nhật lượt đi
            self.turn_label.config(text="Đợi đối phương đi")
            # Tạm thời disable bàn cờ
            self.canvas.unbind("<Button-1>")
            
        except Exception as e:
            print(f"Lỗi gửi dữ liệu: {e}")
            self.close_connection()
    
    def surrender(self):
        if not self.running:
            return
            
        try:
            surrender_data = {
                "type": "SURRENDER"
            }
            json_data = json.dumps(surrender_data)
            print(f"Gửi dữ liệu đầu hàng: {json_data}")
            self.client_socket.send(json_data.encode())
            self.turn_label.config(text="Bạn đã đầu hàng!")
            self.canvas.unbind("<Button-1>")
            
        except Exception as e:
            print(f"Lỗi gửi dữ liệu đầu hàng: {e}")
            
    def close_connection(self):
        self.running = False
        try:
            self.client_socket.close()
        except:
            pass
        self.parent.destroy()

    def place_pieces(self):
        # Xác định vị trí quân cờ dựa trên vai trò (host/client)
        if self.is_host:  # Server: quân đỏ ở dưới
            initial_pieces = [
                # Quân đỏ (dưới bàn cờ)
                ("xe_red", 0, 9), ("xe_red", 8, 9),
                ("ma_red", 1, 9), ("ma_red", 7, 9),
                ("tuongj_red", 2, 9), ("tuongj_red", 6, 9),
                ("si_red", 3, 9), ("si_red", 5, 9),
                ("tuong_red", 4, 9),
                ("phao_red", 1, 7), ("phao_red", 7, 7),
                ("tot_red", 0, 6), ("tot_red", 2, 6), ("tot_red", 4, 6), ("tot_red", 6, 6), ("tot_red", 8, 6),

                # Quân đen (trên bàn cờ)
                ("xe_black", 0, 0), ("xe_black", 8, 0),
                ("ma_black", 1, 0), ("ma_black", 7, 0),
                ("tuongj_black", 2, 0), ("tuongj_black", 6, 0),
                ("si_black", 3, 0), ("si_black", 5, 0),
                ("tuong_black", 4, 0),
                ("phao_black", 1, 2), ("phao_black", 7, 2),
                ("tot_black", 0, 3), ("tot_black", 2, 3), ("tot_black", 4, 3), ("tot_black", 6, 3), ("tot_black", 8, 3),
            ]
        else:  # Client: quân đen ở dưới
            initial_pieces = [
                # Quân đen (dưới bàn cờ)
                ("xe_black", 0, 9), ("xe_black", 8, 9),
                ("ma_black", 1, 9), ("ma_black", 7, 9),
                ("tuongj_black", 2, 9), ("tuongj_black", 6, 9),
                ("si_black", 3, 9), ("si_black", 5, 9),
                ("tuong_black", 4, 9),
                ("phao_black", 1, 7), ("phao_black", 7, 7),
                ("tot_black", 0, 6), ("tot_black", 2, 6), ("tot_black", 4, 6), ("tot_black", 6, 6), ("tot_black", 8, 6),

                # Quân đỏ (trên bàn cờ)
                ("xe_red", 0, 0), ("xe_red", 8, 0),
                ("ma_red", 1, 0), ("ma_red", 7, 0),
                ("tuongj_red", 2, 0), ("tuongj_red", 6, 0),
                ("si_red", 3, 0), ("si_red", 5, 0),
                ("tuong_red", 4, 0),
                ("phao_red", 1, 2), ("phao_red", 7, 2),
                ("tot_red", 0, 3), ("tot_red", 2, 3), ("tot_red", 4, 3), ("tot_red", 6, 3), ("tot_red", 8, 3),
            ]

        for name, x, y in initial_pieces:
            piece = Piece(self.canvas, name, x, y, self.images[name])
            self.pieces.append(piece)
            Board.board_state[y][x] = piece 