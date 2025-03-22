import random

class AIModel:
    def __init__(self, board):
        self.board = board  # Nhận đối tượng bàn cờ khi khởi tạo

    def get_ai_move(self):
        """Chọn một nước đi ngẫu nhiên từ tất cả các quân đen có thể di chuyển"""
        ai_pieces = [piece for piece in self.board.pieces if piece.color == 'black']
        movable_pieces = [piece for piece in ai_pieces if piece.get_valid_moves(self.board)]

        if not movable_pieces:
            return None  # Không có nước đi nào hợp lệ

        piece = random.choice(movable_pieces)
        move = random.choice(piece.get_valid_moves(self.board))

        return piece, move  # Trả về quân cờ và nước đi
