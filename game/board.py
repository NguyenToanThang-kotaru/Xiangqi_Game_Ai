import math
import random
import tkinter as tk
import sys
import os
import threading
# from game.checkmate import is_checkmated, is_checked

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game.Piece import Piece
import math
from game.game_logic import GameLogic
from collections import defaultdict
from game.suggestion import Suggestion
from ai.model import AIModel
CELL_SIZE = 40  
PIECE_RADIUS = CELL_SIZE // 2  

CELL_SIZE = 40

class Board:
    board_state = None
    def __init__(self, canvas, conn=None, mode = None):
        self.mode = mode
        self.canvas = canvas
        self.pieces = []
        self.board_state = [[None for _ in range(9)] for _ in range(10)]
        self.current_turn = "red"
        self.game_logic = GameLogic()
        self.fen_counts = defaultdict(int)
        self.ai = AIModel(self)
        self.selected_piece = None
        self.images = {}  # Khởi tạo dictionary rỗng
        self.move_count = 0 
        self.suggestion = Suggestion(self.game_logic, self.canvas)
        self.draw_board()
        self.load_images()  # Load ảnh
        self.place_pieces()
        self.canvas.bind("<Button-1>", self.on_click)
        self.conn =conn
        self.print_board()
        
        if self.conn:
            import threading
            threading.Thread(target=self.listen_for_opponent, daemon=True).start()

    def draw_board(self):
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
        x1 = piece.x
        y1 = piece.y
        x2, y2 = to_pos
        target_piece = self.board_state[y2][x2]
        if x1==x2 and y1==y2:
            return 0
        if target_piece:
            piece = self.board_state[y1][x1]
            if target_piece.color != piece.color:
                if not self.game_logic.check_move(piece,to_pos,self.board_state):
                    print("Di chuyen sai luat")
                    return 0
                # find the king that have same color as piece, and check if it's gonna be attacked
                if self.game_logic.is_king_safe(piece, to_pos, self.board_state) != None:
                    print("Không đi được vì sẽ bị chiếu - di chuyển quân")
                    return 0
                
                print(f"Quân {piece.name} ăn quân {target_piece.name} tại ({x2}, {y2})")
                self.pieces.remove(target_piece)
                self.canvas.delete(target_piece.id)
                piece.move(x2, y2) # Cập nhật trạng thái
                self.board_state[y2][x2] = piece
                self.board_state[y1][x1] = None
                Suggestion.clear() # Xóa các nước đi gợi ý
                self.selected_piece = None
                self.move_count += 1  
                return 1
            else:
                Suggestion.clear()
                print("đã chuyển đổi từ quân ",piece.name ,"sang ",target_piece.name)
                
                
                self.selected_piece = target_piece
                self.suggestion.suggest(self.selected_piece, self.board_state)
                return 0
        else:    
            if not self.game_logic.check_move(piece,to_pos,self.board_state):
                print("Di chuyen sai luat")
                return 0
            # find the king that have same color as piece, and check if it's gonna be attacked
            # create temporary board state
            if self.game_logic.is_king_safe(piece, to_pos, self.board_state) != None:
                print("Không đi được vì sẽ bị chiếu - di chuyển quân")
                return 0


            piece.move(x2, y2)  
            print("Di chuyển quân",piece.name," đến (",to_pos,")")
            self.board_state[y2][x2] = piece
            self.board_state[y1][x1] = None
            self.selected_piece = None
            self.move_count += 1  
            return 1  

    def on_click(self, event):
        """Xử lý click: chọn hoặc di chuyển quân cờ"""
    
        x = ((event.x / CELL_SIZE * CELL_SIZE) - 20)
        y = ((event.y / CELL_SIZE * CELL_SIZE) - 15)
        col = (round(event.x / CELL_SIZE) - 1)  
        row = (round(event.y / CELL_SIZE) - 1)

        if not self.selected_piece:
            piece = self.get_piece_by_position(event.x - 20, event.y - 15)
            if piece and self.game_logic.is_correct_turn(piece):
                self.selected_piece = piece
                print(f"Chọn quân({piece.name}) cờ tại ({piece.x}, {piece.y})")
                self.suggestion.suggest(piece, Board.board_state)
            else:
                print("Không thể chọn quân vì sai màu hoặc không có quân!")
            return

        # trong trường hợp đã chọn quân cờ
        if self.selected_piece and 0<=col<9 and 0<=row<10:
            from_pos = (self.selected_piece.x, self.selected_piece.y)
        if self.move_piece(self.selected_piece, (col, row)) == 1: # nếu di chuyển quân cờ đến ô khác không phải là ô quân cờ đang nằm
        # self.move_piece(self.selected_piece, (col, row))
            if self.conn:
                # piece = self.get_piece_by_position(x, y)
                self.send_move(from_pos, (col, row))
                print("Sent move to opponent")
            self.print_board()
            # fen = self.to_fen()
            # print(fen)

            # check if the king is checkmated
            red_king = self.game_logic.find_king(self.board_state, "red")
            black_king = self.game_logic.find_king(self.board_state, "black")

            if red_king and self.game_logic.is_checkmated(red_king, self.board_state):
                print("Red king is checkmated")
                self.canvas.unbind("<Button-1>")
            elif black_king and self.game_logic.is_checkmated(black_king, self.board_state):
                print("Black king is checkmated")
                self.canvas.unbind("<Button-1>")

                fen = self.to_fen()
                self.fen_counts[fen] += 1
                # print(f"{fen}: Count {self.fen_counts[fen]}")
                if self.fen_counts[fen] >= 3:
                    print("The game is a draw")
                    self.canvas.unbind("<Button-1>")
                
                # --------------- Update FEN String to check repetition ---------------
                self.selected_piece = None
                # Chuyển lượt sau khi di chuyển
                self.game_logic.swap_turn()
                Suggestion.clear()
                if self.mode:
                    if self.game_logic.current_turn == "black":
                        self.make_ai_move()
                        self.game_logic.swap_turn()
            # elif self.move_piece(self.selected_piece, (col, row))==1:

        # chọn quân cờ trong trường hợp chưa chọn quân cờ nào   
        else:
            piece = self.get_piece_by_position(x, y)
            if piece and self.game_logic.is_correct_turn(piece):
                Suggestion.clear() # clear previous suggestion
                self.selected_piece = piece
                print(f"Chọn quân({self.selected_piece.name}) cờ tại ({self.selected_piece.x}, {self.selected_piece.y})")
                self.suggestion.suggest(self.selected_piece, self.board_state)
            else:
                print("Không thể chọn quân vì sai màu!")
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
        for row in self.board_state:
            print([p.name if p else "." for p in row])
        print("\n\n")

    def to_fen(self):
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
        board_fen = "/".join(fen_rows)
        turn_fen = "w" if self.game_logic.current_turn == "red" else "b"
        print(f"{board_fen} {turn_fen}")
        return f"{board_fen} {turn_fen}"
    
    def get_piece_fen_symbol(self, piece):
        symbol_map = {
            "xe_red": "R", "ma_red": "N", "tuongj_red": "B", "si_red": "A", "tuong_red": "K",
            "phao_red": "C", "tot_red": "P",
            "xe_black": "r", "ma_black": "n", "tuongj_black": "b", "si_black": "a", "tuong_black": "k",
            "phao_black": "c", "tot_black": "p",
        }
        return symbol_map.get(piece.name, "?")
    
    # def suggest_move(self):
    #     if self.selected_piece is not None:
    #         Suggestion(self, self.selected_piece)

    def get_legal_moves(self, piece):
        """Trả về danh sách các nước đi hợp lệ cho quân cờ."""
        legal_moves = []
        for row in range(10):
            for col in range(9):
                if self.game_logic.check_move(piece, (col, row), self.board_state):
                    legal_moves.append((col, row))
        return legal_moves

    def make_ai_move(self):
        """Gọi AI để chọn nước đi"""
        ai_move = self.ai.get_ai_move()
        # print(f"AI Move: {ai_move[0].name} từ ({ai_move[0].x}, {ai_move[0].y}) đến ({ai_move[1][0]}, {ai_move[1][1]})")
        
        if ai_move == -50:
            print("Black king is checkmated")
            self.canvas.unbind("<Button-1>")
            pass
        if ai_move:
            piece, move = ai_move
            self.move_piece(piece, move)
        else:
            print("AI không thể di chuyển, hòa")
            
            
            
    def set_fen(self, fen):
        """Cập nhật bàn cờ từ chuỗi FEN."""
        parts = fen.split()
        board_part = parts[0]
        turn_part = parts[1]

        rows = board_part.split('/')

        # XÓA toàn bộ quân cờ cũ trên canvas
        for piece in self.pieces:
            self.canvas.delete(piece.id)  # Xóa hình ảnh của quân cờ trên canvas

        self.board_state = [[None for _ in range(9)] for _ in range(10)]
        self.pieces = []  # Xóa danh sách quân cờ cũ trước khi đặt lại

        for y, row in enumerate(rows):
            x = 0
            for char in row:
                if char.isdigit():
                    x += int(char)
                else:
                    piece_name = self.fen_to_piece_name(char)
                    if piece_name:
                        image = self.images.get(piece_name, None)  # Tránh lỗi KeyError
                        piece = Piece(self.canvas, piece_name, x, y, image)
                        self.pieces.append(piece)
                        self.board_state[y][x] = piece
                    x += 1

        print(f"Đã cập nhật bàn cờ từ FEN: {fen}")
        if turn_part == "w":
            self.game_logic.current_turn = "red"
        else:
            self.game_logic.current_turn = "black"
        print("Lượt hiện tại:", self.game_logic.current_turn)
        print("Trạng thái bàn cờ: ", self.to_fen())

    def apply_move(self, move):
        """Thực hiện nước đi từ ký hiệu như 'b2g2', nhưng đổi lại tọa độ để phù hợp với tiêu chuẩn."""
        columns = 'abcdefghi'
        
        from_x, from_y = columns.index(move[0]), 9 - int(move[1])  # Đảo ngược tọa độ y
        to_x, to_y = columns.index(move[2]), 9 - int(move[3])  # Đảo ngược tọa độ y

        piece = self.board_state[from_y][from_x]
        
        if piece:  # Kiểm tra nếu có quân cờ ở vị trí ban đầu
            if piece.color == self.game_logic.current_turn:  # Kiểm tra màu của quân cờ
                self.move_piece(piece, (to_x, to_y))
                self.game_logic.swap_turn()
                print(f"Đã di chuyển quân {piece.name} từ ({from_x}, {from_y}) đến ({to_x}, {to_y})")
            else:
                print("Lượt của đối thủ. Không thể di chuyển quân cờ này.")
        else:
            print("Không có quân cờ tại vị trí này.")
            
    def fen_to_piece_name(self, char):
        """Chuyển ký hiệu quân cờ từ FEN về tên quân cờ của chương trình."""
        fen_map = {
            'r': 'xe_black', 'n': 'ma_black', 'b': 'tuongj_black',
            'a': 'si_black', 'k': 'tuong_black', 'c': 'phao_black', 'p': 'tot_black',
            'R': 'xe_red', 'N': 'ma_red', 'B': 'tuongj_red',
            'A': 'si_red', 'K': 'tuong_red', 'C': 'phao_red', 'P': 'tot_red'
        }
        return fen_map.get(char, None)
    
    def get_all_valid_moves(self, color):
        """Trả về danh sách các nước đi hợp lệ cho quân cờ có màu 'color'."""
        valid_moves = []
        for piece in self.pieces:
            if piece.color == color:
                for move in piece.get_valid_moves(self.board_state):  # ✅ Trả về (x2, y2)
                    valid_moves.append((piece.x, piece.y, move[0], move[1]))  # ✅ Ghi nhận cả (x1, y1, x2, y2)
        return valid_moves
        
    
    # def get_all_valid_moves(self, color):
    #     """Trả về danh sách các nước đi hợp lệ cho quân cờ có màu 'color'."""
    #     valid_moves = []
    #     # Logic lấy các nước đi hợp lệ cho quân cờ với màu tương ứng
    #     for piece in self.pieces:
    #         if piece.color == color:
    #             valid_moves.extend(piece.get_valid_moves(self.board_state))
    #     return valid_moves
    
    # # def get_all_valid_moves(self, color):
    # #     """Trả về danh sách các nước đi hợp lệ cho quân cờ có màu 'color'."""
    # #     valid_moves = []
    # #     for piece in self.pieces:
    # #         if piece.color == color:
    # #             for move in piece.get_valid_moves(self):  # move hiện tại chỉ là (x, y)
    # #                 valid_moves.append((piece.x, piece.y, move[0], move[1]))  # Thêm tọa độ bắt đầu
    # #     return valid_moves
    def get_piece_at(self, col, row):
        """Trả về quân cờ tại tọa độ (x, y), hoặc None nếu ô trống"""
        return self.board_state[row][col] 
    def get_board_array(self):
        """Chuyển bàn cờ thành danh sách 2D"""
        return [[Board.board_state[y][x] for x in range(9)] for y in range(10)]
        
    def send_move(self, from_pos, to_pos):
        # from_pos should be where the piece was BEFORE moving
        # to_pos should be the new position
        data = f"{from_pos[0]},{from_pos[1]}:{to_pos[0]},{to_pos[1]}"
        print(f"data: {data}")
        if self.conn is not None:
            self.conn.sendall(data.encode("utf-8"))
            print("Sent move to opponent")
        else:
            print("Connection is closed, cannot send move")
            return
            
    def listen_for_opponent(self):
        if self.conn is None:
            print("Connection not established.")
            return
        try:
            while True and self.conn is not None:
                data = self.conn.recv(1024)
                if not data:
                    print("Socket closed by peer.")
                    break
                print("Received data:", data)
                message = data.decode()
                from_str, to_str = message.split(":")
                fx, fy = map(int, from_str.split(","))
                tx, ty = map(int, to_str.split(","))
                self.canvas.after(0, lambda: self.apply_opponent_move((fx, fy), (tx, ty)))
        except Exception as e:
            print("Connection error in listen_for_opponent:", e)
            import traceback; traceback.print_exc()
        finally:
            print("listen_for_opponent thread exiting")


    def apply_opponent_move(self, from_pos, to_pos):
        try:
            x, y = from_pos
            print(f"from pos: {x}, {y}")
            print(f"to pos: {to_pos}")
            piece = Board.board_state[y][x]
            if not piece:
                print("Opponent tried to move a nonexistent piece.")
                return
            self.selected_piece = piece
            if self.move_piece(piece, to_pos) == 1:
                print("Opponent moved:", piece.name, from_pos, "→", to_pos)
                self.print_board()
                self.game_logic.swap_turn()
                Suggestion.clear()
        except Exception as e:
            print("Exception in apply_opponent_move:", e)
            import traceback
            traceback.print_exc()
            if self.conn:
                print("Closing socket due to error in listen_for_opponent!")
                self.conn.close()
                self.conn = None

    def apply_move_from_network(self, x1, y1, x2, y2):
        piece = Board.board_state[y1][x1]
        if piece and self.move_piece(piece, (x2, y2)) == 1:
            self.game_logic.swap_turn()
    
    def __del__(self):
        print("Board instance is being destroyed!")
