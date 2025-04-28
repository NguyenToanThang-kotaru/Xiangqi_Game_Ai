import tkinter as tk
import config_font
import sys
import os
import socket
import threading
import json
from tkinter import messagebox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.board import Board
from game.game_logic import GameLogic

CELL_SIZE=40

class NetworkManager:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.is_server = False
        self.connected = False
        # Lấy IP thực của máy tính
        self.host = self.get_local_ip()
        self.port = 5000
        self.connection = None  # Socket connection for server

    def get_local_ip(self):
        try:
            # Tạo socket tạm thời để lấy IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"  # Fallback về localhost nếu không lấy được IP

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.is_server = True
            print(f"Server đang chờ kết nối tại {self.host}:{self.port}")
            self.connection, _ = self.server_socket.accept()
            self.connected = True
            print("Client đã kết nối!")
            return True
        except Exception as e:
            print(f"Server error: {e}")
            return False

    def connect_to_server(self, server_ip):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, self.port))
            self.connected = True
            print(f"Đã kết nối tới server {server_ip}:{self.port}")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def send_data(self, data):
        try:
            if self.is_server and self.connected:
                self.connection.sendall(json.dumps(data).encode())
            elif self.connected:
                self.client_socket.sendall(json.dumps(data).encode())
        except Exception as e:
            print(f"Send error: {e}")

    def receive_data(self):
        try:
            if self.is_server and self.connected:
                return json.loads(self.connection.recv(1024).decode())
            elif self.connected:
                return json.loads(self.client_socket.recv(1024).decode())
        except Exception as e:
            print(f"Receive error: {e}")
            return None


def create_PlayvsPlayer(main_window, main_menu):
    network = NetworkManager()
    game_logic = GameLogic()

    # Tạo cửa sổ kết nối
    conn_window = tk.Toplevel()
    config_font.center_window(conn_window, 400, 200)
    conn_window.configure(bg="#333333")
    conn_window.title("Xiangqi - Connect to Player")

    tk.Label(conn_window, text="Your IP: " + network.host,
             bg="#333333", fg="white").pack(pady=10)

    ip_entry = tk.Entry(conn_window)
    ip_entry.pack(pady=10)
    ip_entry.insert(0, network.host)  # Hiển thị IP của máy hiện tại

    def start_server():
        if network.start_server():
            conn_window.withdraw()
            start_game(True)
        else:
            messagebox.showerror("Error", "Failed to start server")

    def connect_client():
        server_ip = ip_entry.get()
        if network.connect_to_server(server_ip):
            conn_window.withdraw()
            start_game(False)
        else:
            messagebox.showerror("Error", "Failed to connect to server")

    tk.Button(conn_window, text="Start Server", command=start_server).pack(pady=5)
    tk.Button(conn_window, text="Connect to Server", command=connect_client).pack(pady=5)

    def start_game(is_server):
        board_window = tk.Toplevel()
        config_font.center_window(board_window, 800, 440)
        board_window.configure(bg="#333333")
        board_window.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(main_window))
        board_window.title("Xiangqi - Player vs Player")

        canvas = tk.Canvas(board_window, height=425, width=400, highlightthickness=0)
        canvas.configure(bg="#333333")
        canvas.pack()

        board = Board(canvas)
        current_turn = "red"
        is_my_turn = is_server
        selected_piece = None

        def convert_coordinates(x, y):
            """Convert coordinates between server and client view"""
            if not is_server:
                return (8 - x, 9 - y)
            return (x, y)

        def handle_move(move):
            nonlocal is_my_turn
            if is_my_turn:
                # Get the piece at the from position
                from_piece = board.get_piece_at(move['from'][0], move['from'][1])
                if from_piece and game_logic.check_move(from_piece, move['to'], board.board_state):
                    # Check if the move is safe for the king
                    if game_logic.is_king_safe(from_piece, move['to'], board.board_state) is None:
                        # Make the move
                        board.move_piece(from_piece, move['to'])
                        # Convert coordinates before sending
                        if not is_server:
                            from_x, from_y = convert_coordinates(move['from'][0], move['from'][1])
                            to_x, to_y = convert_coordinates(move['to'][0], move['to'][1])
                            move = {
                                'from': (from_x, from_y),
                                'to': (to_x, to_y)
                            }
                        # Send move data immediately
                        network.send_data({"type": "move", "move": move})
                        is_my_turn = False
                        update_turn_label()
                    else:
                        print("Không đi được vì sẽ bị chiếu - di chuyển quân")
                else:
                    print("Di chuyển sai luật")

        def receive_moves():
            nonlocal is_my_turn
            while True:
                try:
                    data = network.receive_data()
                    if data and data["type"] == "move":
                        move = data["move"]
                        # Convert coordinates based on who received the move
                        if is_server:
                            # Server received move from client, convert from client coordinates
                            from_x, from_y = 8 - move['from'][0], 9 - move['from'][1]
                            to_x, to_y = 8 - move['to'][0], 9 - move['to'][1]
                            move = {
                                'from': (from_x, from_y),
                                'to': (to_x, to_y)
                            }
                        
                        # Get the piece at the from position
                        from_piece = board.get_piece_at(move['from'][0], move['from'][1])
                        if from_piece:
                            # Move the piece
                            board.move_piece(from_piece, move['to'])
                            # Update turn
                            is_my_turn = True
                            update_turn_label()
                            # Redraw the board
                            board.draw_board()
                except Exception as e:
                    print(f"Error receiving move: {e}")
                    break

        receive_thread = threading.Thread(target=receive_moves, daemon=True)
        receive_thread.start()

        turn_label = tk.Label(board_window, 
                            text=f"Your turn (Playing as {'Red' if is_server else 'Black'})" if is_my_turn 
                            else f"Opponent's turn (Playing as {'Red' if is_server else 'Black'})", 
                            bg="#333333", fg="white")
        turn_label.pack()

        def update_turn_label():
            turn_label.config(text=f"Your turn (Playing as {'Red' if is_server else 'Black'})" if is_my_turn 
                            else f"Opponent's turn (Playing as {'Red' if is_server else 'Black'})")

        back_button = tk.Button(board_window, text="Back to Menu", 
                              command=lambda: config_font.change_gate(board_window, main_menu))
        back_button.place(x=10)

        def on_click(event):
            nonlocal selected_piece, is_my_turn
            # Convert click coordinates for client
            if not is_server:
                x = 8 - (round(event.x / 40) - 1)
                y = 9 - (round(event.y / 40) - 1)
                piece = board.get_piece_at(x, y)
            else:
                piece = board.get_piece_by_position(event.x, event.y)
            
            if piece:
                if selected_piece is None:
                    # Select piece
                    if (is_server and piece.color == "red") or (not is_server and piece.color == "black"):
                        selected_piece = piece
                        print(f"Selected piece: {piece.name} at ({piece.x}, {piece.y})")
                else:
                    # Move piece
                    if selected_piece != piece:
                        move = {
                            'from': (selected_piece.x, selected_piece.y),
                            'to': (piece.x, piece.y)
                        }
                        handle_move(move)
                        selected_piece = None
                    else:
                        # Deselect piece
                        selected_piece = None
            else:
                # Click on empty space
                if selected_piece:
                    # Get grid position
                    if not is_server:
                        grid_x = 8 - (round(event.x / 40) - 1)
                        grid_y = 9 - (round(event.y / 40) - 1)
                    else:
                        grid_x = round(event.x / 40) - 1
                        grid_y = round(event.y / 40) - 1
                        
                    if 0 <= grid_x < 9 and 0 <= grid_y < 10:
                        move = {
                            'from': (selected_piece.x, selected_piece.y),
                            'to': (grid_x, grid_y)
                        }
                        handle_move(move)
                        selected_piece = None

        canvas.bind("<Button-1>", on_click)

        board_window.mainloop()

    conn_window.mainloop()


# Để test: tạo Tkinter window
# create_PlayvsPlayer(tk.Tk(), tk.Toplevel())
