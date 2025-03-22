import random
import tkinter as tk
import sys
import os
from game.checkmate import is_checkmated

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
    def __init__(self, canvas):
        self.canvas = canvas
        self.pieces = []
        self.images = {}
        Board.board_state = [[None for _ in range(9)] for _ in range(10)]  # Lưu trạng thái bàn cờ
        self.current_turn = "red"  # Bắt đầu với quân đỏ
        self.game_logic = GameLogic()  # Khởi tạo game logic
        self.fen_counts = defaultdict(int)
        self.ai = AIModel(self)
        self.selected_piece = None
        self.suggestion = Suggestion(self.game_logic, self.canvas) # why???????????????????????????????????????????
        self.draw_board()
        self.load_images()
        self.place_pieces()
        self.canvas.bind("<Button-1>", self.on_click)

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

        # đường truyền kiểu linux
        # self.images = {
        #     "xe_red": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/red-xe.png"),
        #     "ma_red": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/red-ma.png"),
        #     "tuongj_red": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/red-tuongj.png"),
        #     "si_red": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/red-si.png"),
        #     "tuong_red": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/red-tuong.png"),
        #     "phao_red": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/red-phao.png"),
        #     "tot_red": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/red-tot.png"),
        #     "xe_black": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/black-xe.png"),
        #     "ma_black": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/black-ma.png"),
        #     "tuongj_black": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/black-tuongj.png"),
        #     "si_black": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/black-si.png"),
        #     "tuong_black": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/black-tuong.png"),
        #     "phao_black": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/black-phao.png"),
        #     "tot_black": tk.PhotoImage(file="/home/thien408/Documents/programming/python/Xiangqi_Game_Ai/assets/black-tot.png"),
        # } 
        
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
            Board.board_state[y][x] = piece  # Lưu trạng thái bàn cờ

    def move_piece(self, piece, to_pos):
        x1 = piece.x
        y1 = piece.y
        x2, y2 = to_pos
        target_piece = Board.board_state[y2][x2]
        if x1==x2 and y1==y2:
            return 0
        else:
            if target_piece:
                piece = Board.board_state[y1][x1]
                if target_piece.color != piece.color:
                    if not self.game_logic.check_move(piece,to_pos,Board.board_state):
                        print("Di chuyen sai luat")
                        return 0
                    else: 
                        print(f"Quân {piece.name} ăn quân {target_piece.name} tại ({x2}, {y2})")
                        self.pieces.remove(target_piece)
                        self.canvas.delete(target_piece.id)
                        piece.move(x2, y2) # Cập nhật trạng thái
                        Board.board_state[y2][x2] = piece
                        Board.board_state[y1][x1] = None
                        Suggestion.clear() # Xóa các nước đi gợi ý
                        self.selected_piece = None
                        return 1
                else:
                    Suggestion.clear()
                    print("đã chuyển đổi từ quân ",piece.name ,"sang ")
                    self.selected_piece = target_piece
                    self.suggestion.suggest(self.selected_piece, Board.board_state)
                    return 0
            else:    
                if not self.game_logic.check_move(piece,to_pos,Board.board_state):
                    print("Di chuyen sai luat")
                    return 0
                else:
                    piece.move(x2, y2)  
                    print("Di chuyển quân",piece.name," đến (",to_pos,")")
                    Board.board_state[y2][x2] = piece
                    Board.board_state[y1][x1] = None
                    self.selected_piece = None
                    return 1  


    def on_click(self, event):
        """Xử lý click: chọn hoặc di chuyển quân cờ"""
    
        x = (event.x / CELL_SIZE * CELL_SIZE) - 20
        y = (event.y / CELL_SIZE * CELL_SIZE) - 15
        col = round(event.x / CELL_SIZE) - 1  
        row = round(event.y / CELL_SIZE) - 1

        # trong trường hợp đã chọn quân cờ
        if self.selected_piece and 0<=col<9 and 0<=row<10:
            # Tạm thời không kiểm tra luật đi, chỉ thực hiện di chuyển
            if self.move_piece(self.selected_piece, (col, row)) == 1: # nếu di chuyển quân cờ đến ô khác không phải là ô quân cờ đang nằm
            # self.move_piece(self.selected_piece, (col, row))
                self.print_board()
                # fen = self.to_fen()
                # print(fen)

                # check if the king is checkmated
                for piece in self.pieces:
                    if "tuong_" in piece.name:
                        if is_checkmated(piece, self.board_state, self.pieces):
                            if (piece.color == "red"):
                                print("Red king is checkmated")
                            else:
                                print("Black king is checkmated")
                            self.canvas.unbind("<Button-1>")

                # --------------- Update FEN String to check repetition ---------------

                fen = self.to_fen()
                self.fen_counts[fen] += 1
                print(f"{fen}: Count {self.fen_counts[fen]}")
                if self.fen_counts[fen] >= 3:
                    print("The game is a draw")
                    self.canvas.unbind("<Button-1>")
                
                # --------------- Update FEN String to check repetition ---------------
                self.selected_piece = None
                # Chuyển lượt sau khi di chuyển
                self.game_logic.swap_turn()
                Suggestion.clear()
                # if self.game_logic.current_turn == "black":
                #     self.make_ai_move()
            # elif self.move_piece(self.selected_piece, (col, row))==1:

        # chọn quân cờ trong trường hợp chưa chọn quân cờ nào   
        else:
            piece = self.get_piece_by_position(x, y)
            if piece and self.game_logic.is_correct_turn(piece):
                Suggestion.clear() # clear previous suggestion
                self.selected_piece = piece
                print(f"Chọn quân({self.selected_piece.name}) cờ tại ({self.selected_piece.x}, {self.selected_piece.y})")
                self.suggestion.suggest(self.selected_piece, Board.board_state)
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
        for row in Board.board_state:
            print([p.name if p else "." for p in row])
        print("\n\n")

    def to_fen(self):
        fen_rows = []
        
        for row in Board.board_state:
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
                if self.game_logic.check_move(piece, (col, row), Board.board_state):
                    legal_moves.append((col, row))
        return legal_moves

    def make_ai_move(self):
        """Gọi AI để chọn nước đi"""
        ai_move = self.ai.get_ai_move()
        if ai_move:
            piece, move = ai_move
            self.move_piece(piece, move)
        else:
            print("AI không thể di chuyển, hòa")