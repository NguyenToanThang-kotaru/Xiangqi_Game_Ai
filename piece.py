import pygame

class Piece:
    CELL_SIZE = 80  # Kích thước mỗi ô cờ
    BOARD_START_X = 50  # Lề trái bàn cờ
    BOARD_START_Y = 50  # Lề trên bàn cờ
    PIECE_SIZE = 120  # Kích thước quân cờ

    selected_piece = None  # Biến static để lưu quân cờ đang được chọn

    def __init__(self, image_path, col, row):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.PIECE_SIZE, self.PIECE_SIZE))
        self.col = col  # Vị trí cột (0-8)
        self.row = row  # Vị trí hàng (0-9)
        self.update_position()

    def update_position(self):
        # """ Cập nhật vị trí hiển thị quân cờ theo tọa độ ô bàn cờ """
        self.x = self.BOARD_START_X + self.col * self.CELL_SIZE - self.PIECE_SIZE // 2
        self.y = self.BOARD_START_Y + self.row * self.CELL_SIZE - self.PIECE_SIZE // 2

    def draw(self, screen):
        # """ Vẽ quân cờ lên màn hình """
        screen.blit(self.image, (self.x, self.y))

    @classmethod
    def handle_event(cls, event, pieces):
        # """ Xử lý sự kiện chuột: Click chọn và click di chuyển """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Kiểm tra nếu click vào quân cờ
            for piece in pieces:
                if piece.x <= mx <= piece.x + piece.PIECE_SIZE and piece.y <= my <= piece.y + piece.PIECE_SIZE:
                    cls.selected_piece = piece  # Chọn quân cờ này
                    return  

            #Click vào ô mới để di chuyển
            if cls.selected_piece:
                new_col = round((mx - cls.BOARD_START_X) / cls.CELL_SIZE)
                new_row = round((my - cls.BOARD_START_Y) / cls.CELL_SIZE)

                # Không thể di chuyển ra ngoài bàn cờ
                new_col = max(0, min(8, new_col))
                new_row = max(0, min(9, new_row))

                # Kiểm tra xem có quân cờ nào ở vị trí mới không
                if not any(p.col == new_col and p.row == new_row for p in pieces):
                    cls.selected_piece.col = new_col
                    cls.selected_piece.row = new_row
                    cls.selected_piece.update_position()

                cls.selected_piece = None  # Bỏ chọn quân cờ sau khi di chuyển
