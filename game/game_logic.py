class GameLogic:
    def __init__(self):
        self.current_turn = "red"  # Đỏ đi trước

    def swap_turn(self):
        """Đổi lượt chơi"""
        self.current_turn = "black" if self.current_turn == "red" else "red"

    def is_correct_turn(self, piece):
        """Kiểm tra quân cờ có đúng lượt không"""
        return piece.color == self.current_turn

    def check_move(self, piece, to_pos, board_state):
        """Kiểm tra nước đi có hợp lệ không"""
        # x1, y1 = piece.x, piece.y
        x2, y2 = to_pos
        target_piece = board_state[y2][x2]

        # 1. Không ra ngoài bàn cờ
        if not (0 <= x2 < 9 and 0 <= y2 < 10):
            return False
        
        # 2. Không ăn quân cùng màu
        if target_piece and target_piece.color == piece.color:
            return False
        
        # 3. Kiểm tra luật di chuyển của từng quân cờ
        if "tot" in piece.name:  # Tốt
            return self.check_tot_move(piece, x2, y2)
        elif "xe" in piece.name:  # Xe
            return self.check_xe_move(piece, x2, y2, board_state)
        elif "ma" in piece.name:  # Mã
            return self.check_ma_move(piece, x2, y2, board_state)
        elif "tuongj" in piece.name:  # Tượng
            return self.check_tuong_move(piece, x2, y2)
        elif "si" in piece.name:  # Sĩ
            return self.check_si_move(piece, x2, y2)
        elif "tuong" in piece.name:  # Tướng
            return self.check_tuong_move(piece, x2, y2)
        elif "phao" in piece.name:  # Pháo
            return self.check_phao_move(piece, x2, y2, board_state)
        
        return False  # Mặc định không hợp lệ nếu không thuộc loại nào


    def check_tot_move(self, piece, x2, y2):
        """Kiểm tra di chuyển của tốt"""
        x1, y1 = piece.x, piece.y
        direction = -1 if piece.color == "red" else 1

        # Chưa qua sông: chỉ được đi thẳng 1 ô
        if (piece.color == "red" and y1 >= 5) or (piece.color == "black" and y1 <= 4):
            return x1 == x2 and y2 == y1 + direction

        # Qua sông: đi thẳng hoặc ngang 1 ô
        if (x1 == x2 and y2 == y1 + direction) or (y1 == y2 and abs(x1 - x2) == 1):
            return True

        return False  # Nếu không thoả mãn, nước đi không hợp lệ

    def check_xe_move(self, piece, x2, y2, board_state):
        """Kiểm tra di chuyển của xe (đi ngang hoặc dọc, không bị cản)"""
        x1, y1 = piece.x, piece.y

        if x1 == x2:  # Đi dọc
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if board_state[y][x1] is not None:
                    return False
            return True

        if y1 == y2:  # Đi ngang
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if board_state[y1][x] is not None:
                    return False
            return True

        return False
