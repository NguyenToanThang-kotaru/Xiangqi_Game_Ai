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
    
class AIModel:
    def __init__(self, board):
        self.board = board  # Nhận đối tượng bàn cờ khi khởi tạo
        self.model_move = joblib.load("ai/random_forest_move_predictor.pkl")  # ✅ Tải mô hình duy nhất
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
        turn_value = 1 if turn == 'w' else 0

        return board_array ,turn_value

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
        print("đây là FEN: ", self.board.to_fen())
        fen_array,turn_value = self.fen_to_array(self.board.to_fen())
        print(f"✅ FEN Array: {len(fen_array)}")
        winrate = get_winrate_from_fen_fulltext(self.board.to_fen())
        fen_with_turn = fen_array + [turn_value] + [winrate]
        
        # Dự đoán trực tiếp vector nước đi từ mô hình
        input_data = pd.DataFrame([fen_with_turn], columns=[str(i) for i in range(len(fen_with_turn))])
        print(input_data.columns)
        predicted_move_vector = self.model_move.predict(input_data)[0]  # Dự đoán vector nước đi
        from_x = round(predicted_move_vector[0])
        from_y = round(predicted_move_vector[1])
        to_x   = round(predicted_move_vector[2])
        to_y   = round(predicted_move_vector[3])
        print(f"✅ Dự đoán vector nước đi: {from_x, from_y, to_x, to_y}")
        
        print(f"✅ Dự đoán nước đi ICCS: {vector_to_move(predicted_move_vector)}")
        choose_Pice = self.board.get_piece_at(from_x, from_y)  # Lấy quân cờ từ vị trí dự đoán
        if choose_Pice is None: 
            print("❌ Không tìm thấy quân cờ tại vị trí dự đoán!")
        print(f"✅ Quân cờ dự đoán: {choose_Pice} tại {from_x, from_y}")
        # Kiểm tra các nước đi hợp lệ và chọn nước đi tốt nhất
        for piece, move in all_valid_moves:
            x, y = move  # Giải nén vị trí

            # Kiểm tra xem dự đoán có phù hợp với nước đi hợp lệ hay không

            combined_score = 0
            
            # Kiểm tra có ăn quân không
            captured_piece = self.board.get_piece_at(x, y)
            if captured_piece and captured_piece.color != piece.color:  # Nếu có thể ăn quân địch
                combined_score += captured_piece.value * 0.5  # Cộng điểm dựa trên giá trị quân bị ăn

            if combined_score > best_score:
                best_score = combined_score
                best_moves = [(piece, move)]
            if(from_x, from_y, to_x, to_y) == (piece.x, piece.y, x, y):  # Nếu dự đoán đúng nước đi
                combined_score += 200
                print(f"✅ Dự đoán đúng nước đi: {piece} từ {piece.x, piece.y} đến {x, y}")
            elif (from_x, from_y, to_x, to_y) != (piece.x, piece.y, x, y):  # Nếu dự đoán sai nước đi
                print(f"❌ Dự đoán sai nước đi: {piece} từ {piece.x, piece.y} đến {x, y}")
            elif combined_score == best_score:
                best_moves.append((piece, move))

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


def get_winrate_from_fen_fulltext(fen):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM ai_training_data WHERE MATCH(fen) AGAINST(%s IN BOOLEAN MODE) LIMIT 0, 25"
    cursor.execute(query, (fen,))
    result = cursor.fetchone()
    if result:
        print("co ket qua cua chuoi" ,fen," ket qua: ", result[3])
        return result[3]  # Winrate
    else:
        print("khong co ket qua cua chuoi roiiii" )
        return None  # Không tìm thấy FEN
    # Ví dụ sử dụng
    

   
def vector_to_move(predicted_move_vector):
    # Giả sử predicted_move_vector có cấu trúc [start_col, start_row, end_col, end_row]
    start_col, start_row, end_col, end_row = predicted_move_vector

    # Chuyển start_col và start_row thành số nguyên
    start_col = int(start_col)
    start_row = int(start_row)
    end_col = int(end_col)
    end_row = int(end_row)

    # Sử dụng các giá trị đã ép kiểu để tạo chuỗi ICCS
    columns = 'abcdefghi'
    start_iccs_row = 10 - start_row  # Đảo ngược hàng từ 0-9

    return columns[start_col] + str(start_iccs_row) + columns[end_col] + str(10 - end_row)