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

        x2, y2 = to_pos
        # if target_piece.color == piece.color and target_piece is not None:
        #     return True
        if "tot" in piece.name:
            return self.check_tot_move(piece, x2, y2,board_state)
        elif "xe" in piece.name:
            return self.check_xe_move(piece, x2, y2, board_state)
        elif "ma" in piece.name:
            return self.check_ma_move(piece, x2, y2, board_state)
            # return True
        elif "tuongj" in piece.name: 
            return self.check_tuongj_move(piece, x2, y2, board_state)
            # return True
        elif "si" in piece.name: 
            return self.check_si_move(piece, x2, y2,board_state)
            # return True
        elif "tuong" in piece.name: 
            return self.check_tuong_move(piece, x2, y2, board_state)
            # return True
        elif "phao" in piece.name: 
            return self.check_phao_move(piece, x2, y2, board_state)
        return False  # Mặc định không hợp lệ nếu không thuộc loại nào

    def check_tot_move(self, piece, x2, y2, board_state):
        """Kiểm tra di chuyển của quân Tốt"""
        x1, y1 = piece.x, piece.y
        direction = -1 if piece.color == "red" else 1
        target_piece = board_state[y2][x2]  # Quân cờ tại vị trí đích
    
        # Nếu đi thẳng (chỉ được đi thẳng)
        if x1 == x2 and y2 == y1 + direction:
            if target_piece is None or target_piece.color != piece.color:  # Ăn quân nếu khác màu
                return True
    
        # Nếu đã qua sông, kiểm tra đi ngang
        if (piece.color == "red" and y1 < 5) or (piece.color == "black" and y1 > 4):
            if y1 == y2 and abs(x1 - x2) == 1:  # Đi ngang
                if target_piece is None or target_piece.color != piece.color:
                    return True
    
        return False  # Nếu không thoả mãn, nước đi không hợp lệ
      # Nếu không thoả mãn, nước đi không hợp lệ
    

    def check_xe_move(self, piece, x2, y2, board_state):
        x1, y1 = piece.x, piece.y
        target_piece = board_state[y2][x2]

        if x1 == x2:  # Đi dọc
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if board_state[y][x1] is not None:  # Có quân cản
                    return False

        elif y1 == y2:  # Đi ngang
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if board_state[y1][x] is not None:  # Có quân cản
                    return False

        else:
            return False  # Xe không thể đi chéo

        # Nếu có quân ở đích, kiểm tra màu quân
        if target_piece is not None and target_piece.color == piece.color:
            return False  # Không thể ăn quân cùng màu

        return True  # Hợp lệ


    def check_phao_move(self, piece, x2, y2, board_state):
        
        x1, y1 = piece.x, piece.y
        target_piece = board_state[y2][x2]  # Quân ở ô đích

        if x1 == x2:  # Đi dọc
            step = 1 if y2 > y1 else -1
            count = 0  # Đếm số quân cản

            for y in range(y1 + step, y2, step):
                if board_state[y][x1] is not None:
                    count += 1

            if target_piece is None:
                if count == 0:
                    return True
            else:
                if count == 1 and target_piece.color != piece.color:                    
                    return True

        if y1 == y2:  # Đi ngang 
            step = 1 if x2 > x1 else -1
            count = 0

            for x in range(x1 + step, x2, step):
                if board_state[y1][x] is not None:
                    count += 1

            if target_piece is None:
                if count == 0:
                    return True
            else:
                if count == 1 and target_piece.color != piece.color:
                    return True

        return False  # Không đi chéo
    
    def check_ma_move(self, piece, x2, y2, board_state):
        
        x1, y1 = piece.x, piece.y
        target_piece = board_state[y2][x2]

        #đi dọc
        if y2-y1 == 2: 
            if board_state[y1+1][x1] is None:
                if x2-x1 == 1 or x2-x1 == -1:
                    print("đi xuống")
                    if target_piece is None or target_piece.color != piece.color:  # Ăn quân nếu khác màu
                        return True
                    

        if y2-y1 == -2:
            if board_state[y1-1][x1] is None:
                if x2-x1 == 1 or x2-x1 == -1:
                    print("đi lên")
                    if target_piece is None or target_piece.color != piece.color:  # Ăn quân nếu khác màu
                        return True
            
        #đi ngang 
        if x2-x1 == 2:
            if board_state[y1][x1+1] is None:
                if y2-y1 == 1 or y2-y1 == -1:
                        print("phai")
                        if target_piece is None or target_piece.color != piece.color:  # Ăn quân nếu khác màu
                            return True

        if x2-x1 == -2:
            if board_state[y1][x1-1] is None:
                if y2-y1 == 1 or y2-y1 == -1:
                        print("trai")
                        if target_piece is None or target_piece.color != piece.color:  # Ăn quân nếu khác màu
                            return True

    def check_tuongj_move(self, piece, x2, y2, board_state):

        x1, y1 = piece.x, piece.y
        target_piece = board_state[y2][x2]
        # Giới hạn di chuyển trong thành
        if piece.color == "red" and y2 < 5:
            return False
        
        if piece.color == "black" and y2 >= 5:
            return False
            
        if abs(x2 - x1) != 2 or abs(y2 - y1) != 2:
            return False 
            
        # Bị chặn    
        x_mid  = (x1+x2) // 2
        y_mid  = (y1+y2) // 2
        if board_state[y_mid][x_mid] is not None:
            return False
        
        if target_piece is None or target_piece.color != piece.color:  # Ăn quân nếu khác màu
            return True
    
    def check_si_move(self, piece, x2, y2,board_state):
        
        x1, y1 = piece.x, piece.y
        target_piece = board_state[y2][x2]
        if abs(x2 - x1) != 1 or abs(y2 - y1) != 1:
            return False 
        
        # Giới hạn di chuyển trong thành
        if piece.color == "red":
            if not (3 <= x2 <= 5 and 7 <= y2 <= 9):  
                return False
        else:  
            if not (3 <= x2 <= 5 and 0 <= y2 <= 2):  
                return False
        if target_piece is None or target_piece.color != piece.color:  # Ăn quân nếu khác màu
                return True
    
    def check_tuong_move(self, piece, x2, y2,board_state):
        
        x1, y1 = piece.x, piece.y
        target_piece = board_state[y2][x2]
        if abs(x2 - x1) + abs(y2 - y1) != 1:
            return False 
        
        # Giới hạn di chuyển trong thành
        if piece.color == "red":
            if not (3 <= x2 <= 5 and 7 <= y2 <= 9):  
                return False
            else:
                if target_piece is None:
                    return True
        else:  
            if not (3 <= x2 <= 5 and 0 <= y2 <= 2):  
                return False
            else:
                if target_piece is None:
                    return True
        return False
    