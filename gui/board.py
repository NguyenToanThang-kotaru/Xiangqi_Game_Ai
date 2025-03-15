import tkinter as tk
from game.Piece import Piece
import math
from game.game_logic import GameLogic
CELL_SIZE = 40  
PIECE_RADIUS = CELL_SIZE // 2  

CELL_SIZE = 40

class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.pieces = []
        self.images = {}
        self.board_state = [[None for _ in range(9)] for _ in range(10)]  # Lưu trạng thái bàn cờ
        self.current_turn = "red"  # Bắt đầu với quân đỏ
        self.game_logic = GameLogic()  # Khởi tạo game logic

        self.selected_piece = None
        self.draw_board()
        self.load_images()
        self.place_pieces()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        """Vẽ bàn cờ trên canvas"""
        for col in range(9):
            x = (col + 1) * CELL_SIZE
            if col == 0 or col == 8:
                self.canvas.create_line(x, CELL_SIZE, x, 10*CELL_SIZE, width=2, fill="#FF3399")
            else:
                self.canvas.create_line(x, CELL_SIZE, x, 5*CELL_SIZE, width=2, fill="#FF3399")
                self.canvas.create_line(x, 6*CELL_SIZE, x, 10*CELL_SIZE, width=2, fill="#FF3399")
        for row in range(10):
            y = (row + 1) * CELL_SIZE
            self.canvas.create_line(CELL_SIZE, y, CELL_SIZE * 9, y, width=2, fill="#FF3399")

        # Vẽ đường chéo trong cung tướng
        self.canvas.create_line(CELL_SIZE*4, CELL_SIZE, CELL_SIZE*6, CELL_SIZE*3, width=2, fill="#FF3399")
        self.canvas.create_line(CELL_SIZE*4, CELL_SIZE*3, CELL_SIZE*6, CELL_SIZE, width=2, fill="#FF3399")
        self.canvas.create_line(CELL_SIZE*4, CELL_SIZE*8, CELL_SIZE*6, CELL_SIZE*10, width=2, fill="#FF3399")
        self.canvas.create_line(CELL_SIZE*4, CELL_SIZE*10, CELL_SIZE*6, CELL_SIZE*8, width=2, fill="#FF3399")

    def load_images(self):
        """Tải ảnh quân cờ"""
        self.images = {
            "xe_red": tk.PhotoImage(file="assets/red-xe.png"),
            "ma_red": tk.PhotoImage(file="assets/red-ma.png"),
            "tuongj_red": tk.PhotoImage(file="assets/red-tuongj.png"),
            "si_red": tk.PhotoImage(file="assets/red-si.png"),
            "tuong_red": tk.PhotoImage(file="assets/red-tuong.png"),
            "phao_red": tk.PhotoImage(file="assets/red-phao.png"),
            "tot_red": tk.PhotoImage(file="assets/red-tot.png"),
            "xe_black": tk.PhotoImage(file="assets/black-xe.png"),
            "ma_black": tk.PhotoImage(file="assets/black-ma.png"),
            "tuongj_black": tk.PhotoImage(file="assets/black-tuongj.png"),
            "si_black": tk.PhotoImage(file="assets/black-si.png"),
            "tuong_black": tk.PhotoImage(file="assets/black-tuong.png"),
            "phao_black": tk.PhotoImage(file="assets/black-phao.png"),
            "tot_black": tk.PhotoImage(file="assets/black-tot.png"),
        }

    def place_pieces(self):
        """Đặt quân cờ lên bàn và lưu vào board_state"""
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

        for name, x, y in initial_pieces:
            piece = Piece(self.canvas, name, x, y, self.images[name])
            self.pieces.append(piece)
            self.board_state[y][x] = piece  # Lưu trạng thái bàn cờ

    def move_piece(self, piece, to_pos):
        """Di chuyển quân cờ và cập nhật trạng thái"""
        
        x1 = piece.x
        y1 = piece.y
        x2, y2 = to_pos
        

        if self.board_state[y1][x1]:  # Nếu có quân cờ ở vị trí ban đầu
            piece = self.board_state[y1][x1]
            piece.move(x2, y2)  
            print("Di chuyển quân",piece.name," đến (",to_pos,")")
            self.board_state[y2][x2] = piece
            self.board_state[y1][x1] = None
            self.selected_piece = None  
        

    def on_click(self, event):
        """Xử lý click: chọn hoặc di chuyển quân cờ"""
    
        x = (event.x / CELL_SIZE * CELL_SIZE) - 20
        y = (event.y / CELL_SIZE * CELL_SIZE) - 15
        col = round(event.x / CELL_SIZE) - 1  
        row = round(event.y / CELL_SIZE) - 1

        if self.selected_piece and 0<col<9 and 0<row<10:
            # Tạm thời không kiểm tra luật đi, chỉ thực hiện di chuyển
            self.move_piece(self.selected_piece, (col, row))
            self.print_board()
            fen = self.to_fen()
            print(fen)
            self.selected_piece = None
            # Chuyển lượt sau khi di chuyển
            self.current_turn = "black" if self.current_turn == "red" else "red"
        else:
            piece = self.get_piece_by_position(x, y)
            if piece and piece.color == self.current_turn:
                self.selected_piece = piece
                print(f"Chọn quân({self.selected_piece.name}) cờ tại ({self.selected_piece.x}, {self.selected_piece.y})")
            else:
                print("Không thể chọn quân cờ này hoặc sai màu!")
                self.selected_piece = None



    def get_piece_by_position(self, x_click, y_click):
        """Tìm quân cờ gần nhất với vị trí click"""
        nearest_piece = None
        min_distance = float("inf")

        for piece in self.pieces:
            x_piece = piece.x * CELL_SIZE + CELL_SIZE // 2  
            y_piece = piece.y * CELL_SIZE + CELL_SIZE // 2  
            distance = math.sqrt((x_click - x_piece) ** 2 + (y_click - y_piece) ** 2)

            if distance < min_distance and distance <= PIECE_RADIUS:
                nearest_piece = piece
                min_distance = distance

        return nearest_piece

    
    def print_board(self):
        """In trạng thái bàn cờ (debug)"""
        for row in self.board_state:
            print([p.name if p else "." for p in row])
        print("\n\n\n\n\n")

    def to_fen(self):
        """Chuyển trạng thái bàn cờ thành chuỗi FEN chuẩn"""
        fen_rows = []
        
        for row in self.board_state:
            empty_count = 0
            fen_row = ""
            
            for piece in row:
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    # Lấy ký hiệu quân cờ theo chuẩn FEN
                    fen_row += self.get_piece_fen_symbol(piece)
    
            if empty_count > 0:
                fen_row += str(empty_count)
    
            fen_rows.append(fen_row)
    
        # Ghép thành chuỗi FEN hoàn chỉnh
        board_fen = "/".join(fen_rows)
        turn_fen = "w" if self.current_turn == "red" else "b"
    
        return f"{board_fen} {turn_fen}"
    
    def get_piece_fen_symbol(self, piece):
        """Trả về ký hiệu FEN của quân cờ theo chuẩn ICCS"""
        symbol_map = {
            "xe_red": "R", "ma_red": "N", "tuongj_red": "B", "si_red": "A", "tuong_red": "K",
            "phao_red": "C", "tot_red": "P",
            "xe_black": "r", "ma_black": "n", "tuongj_black": "b", "si_black": "a", "tuong_black": "k",
            "phao_black": "c", "tot_black": "p",
        }
        return symbol_map.get(piece.name, "?")
    

