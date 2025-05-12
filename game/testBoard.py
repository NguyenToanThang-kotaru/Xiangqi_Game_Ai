import tkinter as tk
from board import Board
if __name__ == "__main__":
    import tkinter as tk
    from Piece import Piece

    root = tk.Tk()
    canvas = tk.Canvas(root, width=800, height=900)
    canvas.pack()
    board = Board(canvas)
    test_fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C2C4/9/RNBAKABNR b"
    board.set_fen(test_fen)  # Gọi để test
    board.apply_move("i9i8")  # Gọi để test
    board.to_fen()  # Gọi để test
    board.apply_move("i0i2")  # Gọi để test
    board.to_fen()  # Gọi để test
    valid = board.get_all_valid_moves("black")
    print("Valid moves for black:", valid)  # In ra danh sách nước đi hợp lệ
    for move in board.get_all_valid_moves("black"):
        start_x, start_y, end_x, end_y = move
        print(f"Quân cờ: ({board.get_piece_at(start_x,start_y).name}), Nước đi: ({end_x}, {end_y})")

    # board.place_pieces # Vẽ bàn cờ với FEN đã cập nhật
    root.mainloop()
