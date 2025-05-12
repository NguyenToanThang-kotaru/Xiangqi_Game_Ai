import random
import joblib
import numpy as np
import pandas as pd
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="xiangqi"
    )
X_test = pd.read_csv("dataset/X_test.csv")
class AIModel:
    def __init__(self, board):
        self.board = board  # Nhận đối tượng bàn cờ khi khởi tạo
        self.model_move = joblib.load("ai/random_forest_model2.pkl")  # ✅ Tải mô hình duy nhất
        print("✅ AI Model Loaded!")

    def fen_to_array(self,fen):
        PIECE_MAPPING = {
            'r': 1, 'n': 2, 'b': 3, 'a': 4, 'k': 5, 'c': 6, 'p': 7,  
            'R': 8, 'N': 9, 'B': 10, 'A': 11, 'K': 12, 'C': 13, 'P': 14,  
        }

        parts = fen.split()
        board_fen = parts[0]  # Phần bàn cờ
        turn = parts[1]  # Lượt đi

        board_array = []
        
        for char in board_fen:
            if char in PIECE_MAPPING:  # Nếu là quân cờ
                board_array.append(PIECE_MAPPING[char])
            elif char.isdigit():  # Nếu là số (ô trống)
                board_array.extend([0] * int(char))  # Thêm đúng số lượng số 0
            elif char == '/':  # Dấu `/` không cần lưu
                continue  

        # Thêm lượt đi vào mảng số (0 nếu là 'w', 1 nếu là 'b')
        turn_value = 0 if turn == 'w' else 1

        return board_array ,turn_value

    def predict_best_move(self):
        """Dự đoán nước đi tốt nhất từ winrate của mỗi nước đi"""
        all_valid_moves = []

        # Lấy tất cả các nước đi hợp lệ của quân cờ đen
        for piece in self.board.pieces:
            if piece.color == "black":
                valid_moves = piece.get_valid_moves(self.board)
                for move in valid_moves:
                    all_valid_moves.append((piece, move))

        if not all_valid_moves:
            print("⚠️ Không có nước đi hợp lệ!")
            return None

        best_moves = []
        best_winrate = -float('inf')  # Đặt winrate thấp nhất ban đầu

        # Chuyển FEN sang mảng số
        print("đây là FEN: ", self.board.to_fen())
        fen_array, turn_value = self.fen_to_array(self.board.to_fen())
        fen_with_turn = fen_array + [turn_value] 

        # Duyệt qua tất cả các nước đi hợp lệ
        for move in self.board.get_all_valid_moves("black"):
            from_x, from_y, end_x, end_y = move  # Giải nén vị trí nước đi
            print(f"✅ Duyệt nước đi từ {from_x, from_y} đến {end_x,end_y}")
            # Chuyển FEN và thông tin nước đi thành dữ liệu vào mô hình
            fen_with_move =fen_with_turn + [from_x, from_y, end_x, end_y]  # Thêm thông tin nước đi vào FEN
            
            input_data = pd.DataFrame([fen_with_move], columns=[str(i) for i in range(95)])  # Chuyển đổi thành DataFrame

            # Dự đoán winrate cho mỗi nước đi từ mô hình
            predicted_winrate = self.model_move.predict(input_data)[0]  # Dự đoán winrate cho nước đi
            print(f"✅ Dự đoán winrate cho nước đi {self.board.get_piece_at(from_x,from_y)} từ {from_x, from_y} đến {end_x,end_y}: {predicted_winrate}")
            enemy = self.board.get_piece_at(end_x, end_y)  # Lấy quân cờ địch ở vị trí đích
            if enemy:
                predicted_winrate += 2
            # Chọn nước đi có winrate cao nhất
            if predicted_winrate > best_winrate:
                best_winrate = predicted_winrate
                best_moves = [move]  # Reset lại nước đi tốt nhất


        # Chọn ngẫu nhiên trong các nước đi tốt nhất có winrate cao nhất
        print(f"✅ Nước đi tốt nhất có winrate cao nhất: {best_moves}")
        
    
        return  best_moves  # Trả về nước đi tốt nhất


    def get_ai_move(self):
        """Lấy nước đi tốt nhất từ AI"""
        best_move = self.predict_best_move()
        if not best_move:
            return -50
        piece = self.board.get_piece_at(best_move[0][0], best_move[0][1])
        print(f"✅ Quân cờ: {piece} từ {best_move[0][1], best_move[0][0]} đến {best_move[0][3], best_move[0][2]}")
        # print(f"✅ Nước đi tốt nhất: {piece} từ {best_move[0], best_move[1]} đến {best_move[2], best_move[3]}") 
        if piece is None or best_move is None:
            print("❌ Không có nước đi hợp lệ! AI bị bí.")
            return None, None  

        to_pos = [best_move[0][2], best_move[0][3]]  # Lấy vị trí đích
        return piece,to_pos 