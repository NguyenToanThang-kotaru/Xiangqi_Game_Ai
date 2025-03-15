class GameLogic:
    def __init__(self):
        self.current_turn = "red"  # Đỏ đi trước

    def swap_turn(self):
        """Đổi lượt chơi"""
        self.current_turn = "black" if self.current_turn == "red" else "red"

    def is_correct_turn(self, piece):
        """Kiểm tra quân cờ có đúng lượt không"""
        return piece.color == self.current_turn
