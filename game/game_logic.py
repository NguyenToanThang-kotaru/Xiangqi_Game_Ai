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
            return self.check_tot_move(piece, x2, y2)
        elif "xe" in piece.name:
            return self.check_xe_move(piece, x2, y2, board_state)
        elif "ma" in piece.name:
            return self.check_ma_move(piece, x2, y2, board_state)
            # return True
        elif "tuongj" in piece.name: 
            return self.check_tuongj_move(piece, x2, y2, board_state)
            # return True
        elif "si" in piece.name: 
            return self.check_si_move(piece, x2, y2)
            # return True
        elif "tuong" in piece.name: 
            return self.check_tuong_move(piece, x2, y2)
            # return True
        elif "phao" in piece.name: 
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
                if count == 1:
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
                if count == 1:
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
                    return True

        if y2-y1 == -2:
            if board_state[y1-1][x1] is None:
                if x2-x1 == 1 or x2-x1 == -1:
                    print("đi lên")
                    return True
            
        #đi ngang 
        if x2-x1 == 2:
            if board_state[y1][x1+1] is None:
                if y2-y1 == 1 or y2-y1 == -1:
                        print("phai")
                        return True

        if x2-x1 == -2:
            if board_state[y1][x1-1] is None:
                if y2-y1 == 1 or y2-y1 == -1:
                        print("trai")
                        return True

    def check_tuongj_move(self, piece, x2, y2, board_state):

        x1, y1 = piece.x, piece.y

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
        
        return True
    
    def check_si_move(self, piece, x2, y2):
        
        x1, y1 = piece.x, piece.y

        if abs(x2 - x1) != 1 or abs(y2 - y1) != 1:
            return False 
        
        # Giới hạn di chuyển trong thành
        if piece.color == "red":
            if not (3 <= x2 <= 5 and 7 <= y2 <= 9):  
                return False
        else:  
            if not (3 <= x2 <= 5 and 0 <= y2 <= 2):  
                return False
        
        return True
    
    def check_tuong_move(self, piece, x2, y2):
        
        x1, y1 = piece.x, piece.y

        if abs(x2 - x1) + abs(y2 - y1) != 1:
            return False 
        
        # Giới hạn di chuyển trong thành
        if piece.color == "red":
            if not (3 <= x2 <= 5 and 7 <= y2 <= 9):  
                return False
        else:  
            if not (3 <= x2 <= 5 and 0 <= y2 <= 2):  
                return False
        
        return True
        




    

    









               
                
               
                

            
                    
                
            


               
        