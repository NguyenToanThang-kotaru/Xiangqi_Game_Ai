# PlayvsPlayer.py
import tkinter as tk
import socket
import threading
import config_font
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.board import Board
from game.game_logic import GameLogic

HOST = '192.168.1.3'
PORT = 55555
main_window = tk.Tk()
main_window.withdraw()  # Ẩn cửa sổ chính nếu không cần

def start_server(callback):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Đang chờ người chơi khác kết nối...")
    conn, addr = server.accept()
    print(f"Đã kết nối với {addr}")
    callback(conn)

def connect_to_server(callback):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("Đã kết nối tới server")
    callback(client)

def create_PlayvsPlayer(main_window, main_menu):
    def choose_role():
        role_window = tk.Toplevel(main_window)
        role_window.title("Chọn vai trò")
        role_window.configure(bg="#333333")
        config_font.center_window(role_window, 300, 150)

        label = tk.Label(role_window, text="Chọn vai trò:", bg="#333333", fg="white", font=config_font.get_font(14))
        label.pack(pady=10)

        def start_as_server():
            role_window.destroy()
            threading.Thread(target=start_server, args=(lambda conn: launch_game(conn, True),)).start()

        def start_as_client():
            role_window.destroy()
            threading.Thread(target=connect_to_server, args=(lambda conn: launch_game(conn, False),)).start()

        server_button = tk.Button(role_window, text="Chủ Phòng", command=start_as_server)
        client_button = tk.Button(role_window, text="Khách", command=start_as_client)
        server_button.pack(pady=5)
        client_button.pack(pady=5)

    def launch_game(conn, is_server):
        board_window = tk.Toplevel(main_window)
        board_window.title("Player vs Player")
        config_font.center_window(board_window, 800, 440)
        board_window.configure(bg="#333333")
        board_window.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(main_window))

        canvas = tk.Canvas(board_window, height=425, width=400, highlightthickness=0, bg="#333333")
        canvas.pack()

        game_logic = GameLogic()
        board = Board(canvas)

        is_my_turn = is_server  # Server đi trước

        turn_label = tk.Label(board_window, text="", bg="#333333", fg="white", font=config_font.get_font(12))
        turn_label.pack()

        def update_turn_label():
            if is_my_turn:
                turn_label.config(text="Đến lượt bạn")
            else:
                turn_label.config(text="Chờ đối thủ...")

        def receive_move():
            nonlocal is_my_turn
            while True:
                data = conn.recv(1024).decode()
                if data:
                    print("Nhận:", data)
                    from_pos, to_pos = data.split("-")
                    fx, fy = map(int, from_pos.split(","))
                    tx, ty = map(int, to_pos.split(","))
                    board.move_piece((fx, fy), (tx, ty))
                    is_my_turn = True
                    update_turn_label()

        def on_canvas_click(event):
            nonlocal is_my_turn
            if not is_my_turn:
                return

            board.handle_click(event.x, event.y)

            if board.last_move:
                from_pos, to_pos = board.last_move
                move_str = f"{from_pos[0]},{from_pos[1]}-{to_pos[0]},{to_pos[1]}"
                conn.sendall(move_str.encode())
                board.last_move = None
                is_my_turn = False
                update_turn_label()

        canvas.bind("<Button-1>", on_canvas_click)
        update_turn_label()

        threading.Thread(target=receive_move, daemon=True).start()

        back_button = tk.Button(board_window, text="Back to Menu", command=lambda: config_font.change_gate(board_window, main_menu))
        back_button.place(x=10)

    choose_role()
