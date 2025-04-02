import random
import joblib
import numpy as np
import pandas as pd

class AIModel:
    def __init__(self, board):
        self.board = board  # Nhận đối tượng bàn cờ khi khởi tạo
        self.model_score = joblib.load("ai/random_forest_score.pkl")  # ✅ Tải mô hình Score
        self.model_winrate = joblib.load("ai/random_forest_winrate.pkl")  # ✅ Tải mô hình Winrate
        print("✅ AI Models Loaded!")

    def fen_to_array(self, fen):  
        """Chuyển FEN thành mảng số với đầy đủ số lượng đặc trưng"""
        PIECE_MAPPING = {
            'r': 1, 'n': 2, 'b': 3, 'a': 4, 'k': 5, 'c': 6, 'p': 7,  
            'R': 8, 'N': 9, 'B': 10, 'A': 11, 'K': 12, 'C': 13, 'P': 14,  
            '/': -1,  
            '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0
        }

        parts = fen.split()
        board_fen = parts[0]  
        turn = parts[1]  

        board_array = [PIECE_MAPPING.get(char, 0) for char in board_fen]
        turn_value = 0 if turn == 'w' else 1  

        move_count = self.board.move_count if hasattr(self.board, "move_count") else 0  

        # ✅ Đảm bảo số lượng đặc trưng đủ 95 (hoặc số lượng đặc trưng mô hình yêu cầu)
        while len(board_array) < 95 - 2:  # Trừ đi 2 vì còn turn_value và move_count
            board_array.append(0)  # Thêm giá trị mặc định

        return board_array + [turn_value, move_count]



    def predict_best_move(self):
        """Dự đoán nước đi tốt nhất"""
        all_valid_moves = []
        
        for piece in self.board.pieces:
            if piece.color == "black":
                valid_moves = piece.get_valid_moves(self.board)
                for move in valid_moves:
                    all_valid_moves.append((piece, move))

        if not all_valid_moves:
            print("⚠️ Không có nước đi hợp lệ!")
            return None  

        best_moves = []  
        best_score = -float('inf')

        # Chuyển FEN sang mảng số
        fen_array = self.fen_to_array(self.board.to_fen())
        print(f"✅ FEN Array: {len(fen_array)}")

        for piece, move in all_valid_moves:
            x, y = move  # Giải nén vị trí

            input_data = pd.DataFrame([fen_array], columns=[str(i) for i in range(len(fen_array))])
            predicted_score = self.model_score.predict(input_data)[0]
            predicted_winrate = self.model_winrate.predict(input_data)[0]
            combined_score = predicted_score * 0.7 + predicted_winrate * 0.3  

            # Kiểm tra có ăn quân không
            captured_piece = self.board.get_piece_at(x, y)
            if captured_piece and captured_piece.color != piece.color:  # Nếu có thể ăn quân địch
                combined_score += captured_piece.value * 2  # Cộng điểm dựa trên giá trị quân bị ăn

            if combined_score > best_score:
                best_score = combined_score
                best_moves = [(piece, move)]
            elif combined_score == best_score:
                best_moves.append((piece, move))

        chosen_move = random.choice(best_moves)  
        print(f"✅ AI chọn nước đi: {chosen_move} với điểm {best_score}")
         

        chosen_move = random.choice(best_moves)  # Chọn ngẫu nhiên trong các nước đi tốt nhất
        print(f"✅ AI chọn nước đi: {chosen_move} với điểm {best_score}")
        return chosen_move[1]  # Trả về nước đi (không phải cả tuple)

    
    
    def get_ai_move(self):
        """Lấy nước đi tốt nhất từ AI"""
        best_move = self.predict_best_move()

        print(f"🔍 AI dự đoán nước đi: {best_move}")

        if not best_move:
            print("❌ Không có nước đi hợp lệ! AI bị bí.")
            return None, None  

        found_piece = None  # Lưu lại quân cờ nếu tìm thấy

        # Kiểm tra danh sách nước đi hợp lệ của AI
        for piece in self.board.pieces:
            if piece.color == "black":
                valid_moves = piece.get_valid_moves(self.board)
                print(f"♟️ {piece}: {valid_moves}")

                if best_move in valid_moves:
                    found_piece = piece
                    break  # Thoát vòng lặp khi tìm thấy quân cờ có thể đi

        if found_piece:
            print(f"✅ AI chọn {found_piece} từ {found_piece.x,found_piece.y} di chuyển đến {best_move}")
            return found_piece, best_move  

        print("❌ Không có quân cờ nào có thể thực hiện nước đi này.")
        return None, None

