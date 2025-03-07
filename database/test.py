import tkinter as tk

CELL_SIZE = 80  # Kích thước ô cờ

class Piece:
    def __init__(self, canvas, name, x, y, color):
        self.canvas = canvas
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.id = canvas.create_oval(
            x * CELL_SIZE + 10, y * CELL_SIZE + 10, 
            (x + 1) * CELL_SIZE - 10, (y + 1) * CELL_SIZE - 10, 
            fill=color
        )

    def move(self, x, y):
        self.x = x
        self.y = y
        self.canvas.coords(
            self.id, 
            x * CELL_SIZE + 10, y * CELL_SIZE + 10, 
            (x + 1) * CELL_SIZE - 10, (y + 1) * CELL_SIZE - 10
        )

# ================== MAIN GAME ==================
root = tk.Tk()
root.title("Cờ Tướng - Click để di chuyển")

canvas = tk.Canvas(root, width=9 * CELL_SIZE, height=10 * CELL_SIZE, bg="white")
canvas.pack()

# Tạo một quân cờ màu đỏ ở vị trí (4, 4)
piece = Piece(canvas, "Tướng", 4, 4, "red")

selected_piece = None

def on_click(event):
    global selected_piece
    x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
    
    if selected_piece:
        # Nếu đã chọn quân, di chuyển quân cờ đến vị trí mới
        selected_piece.move(x, y)
        selected_piece = None  # Bỏ chọn
    else:
        # Chọn quân cờ nếu click vào nó
        if piece.x == x and piece.y == y:
            selected_piece = piece  # Lưu quân cờ đang chọn

canvas.bind("<Button-1>", on_click)  # Lắng nghe sự kiện click chuột trái

root.mainloop()
