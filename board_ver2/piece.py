import pygame
import os

class Piece:
    CELL_SIZE = 70  # Kích thước mỗi ô cờ
    NUM_COL = 9
    NUM_ROW = 10
    board_width = (NUM_COL - 1) * CELL_SIZE
    board_height = (NUM_ROW - 1) * CELL_SIZE

    screen_width, screen_height = 750, 750 #cannot use the function screen.get_size()

    # Vị trí bắt đầu bàn cờ
    BOARD_START_X = (screen_width - board_width) // 2  
    BOARD_START_Y = (screen_height - board_height) // 2 

    PIECE_SIZE = 90  # Kích thước quân cờ

    # Initialize the pieces
    def __init__(self, image_path, col, row):
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.PIECE_SIZE, self.PIECE_SIZE))
        self.col = col  # Vị trí cột 
        self.row = row  # Vị trí hàng 
        self.selected = False
        self.offset_x = 0  # Khoảng cách giữa chuột và tâm quân cờ khi click
        self.offset_y = 0
        self.update_position()

    def update_position(self):
        # Cập nhật vị trí hiển thị quân cờ theo ô cờ 
        self.x = self.BOARD_START_X + self.col * self.CELL_SIZE - self.PIECE_SIZE // 2
        self.y = self.BOARD_START_Y + self.row * self.CELL_SIZE - self.PIECE_SIZE // 2

    def draw(self, screen):
        # Vẽ quân cờ lên màn hình 
        screen.blit(self.image, (self.x, self.y))

    def handle_event(self, event, pieces):
        # Xử lý sự kiện chuột để kéo thả quân cờ 
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if self.x <= mx <= self.x + self.PIECE_SIZE and self.y <= my <= self.y + self.PIECE_SIZE:
                self.selected = True
                self.offset_x = mx - self.x
                self.offset_y = my - self.y

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selected:
                mx, my = event.pos

                # Căn chỉnh vị trí quân cờ (dự kiến) về đúng ô gần nhất 
                draft_col = round((mx - self.BOARD_START_X) / self.CELL_SIZE)
                draft_row = round((my - self.BOARD_START_Y) / self.CELL_SIZE)

                # Giới hạn phạm vi di chuyển trong bàn cờ
                if (draft_col > 8 or draft_row > 9):
                    self.col = max(0, min(8, draft_col))
                    self.row = max(0, min(9, draft_row))
                    return

                # Giới hạn phạm vi di chuyển của từng quân cờ
                # take the name of the image
                piece_base_name = os.path.basename(self.image_path) 
                name = os.path.splitext(piece_base_name)[0]

                if name == "red-tot":
                    if not self.is_friendly_piece_at(draft_col, draft_row, pieces, name):
                        self.redPawn_logic(draft_col, draft_row)
                elif name == "black-tot":
                    if not self.is_friendly_piece_at(draft_col, draft_row, pieces, name):
                        self.blackPawn_logic(draft_col, draft_row)
                elif name == "black-xe" or name == "red-xe":
                    if not self.is_friendly_piece_at(draft_col, draft_row, pieces, name):
                        self.rook_logic(draft_col, draft_row, pieces)
                else:
                    self.col = draft_col
                    self.row = draft_row

                # Cập nhật lại vị trí đúng ô
                self.update_position()
                self.selected = False

        elif event.type == pygame.MOUSEMOTION and self.selected:
            # Di chuyển quân cờ theo chuột nhưng vẫn giữ khoảng cách ban đầu
            mx, my = event.pos
            self.x = mx - self.offset_x
            self.y = my - self.offset_y

    # check if there are friendly piece in the specific position
    def is_friendly_piece_at(self, col, row, pieces, name):
        for piece in pieces:
            if piece.col == col and piece.row == row:
                # Check if the piece is friendly
                if os.path.basename(piece.image_path).split('-')[0] == name.split('-')[0]:
                    return True
        return False

    def blackPawn_logic(self, col, row):
        if self.row <= 4: # Before crossing the river
            if self.col == col and (row - self.row) == 1:
                self.row = row
        else:
            if self.col == col and (row - self.row) == 1:
                self.row = row
            elif self.row == row and abs(self.col - col) == 1:
                self.col = col
    
    def redPawn_logic(self, col, row):
        if self.row >= 5:  # Before crossing the river
            if col == self.col and (self.row - row) == 1:
                self.row = row
        else:  # After crossing the river
            if col == self.col and (self.row - row) == 1:
                self.row = row
            elif row == self.row and abs(col - self.col) == 1:
                self.col = col

    def rook_logic(self, col, row, pieces):
        step = -1
        if self.col == col:
            # check the row 
            if self.row < row:
                step = 1
            for i in range(self.row + step, row, step):
                # if there is a friendly piece at the position (col, i) for the first time => return
                for piece in pieces:
                    if piece.col == self.col and piece.row == i:
                        return
            self.row = row
        elif self.row == row:
            if self.col < col:
                step = 1
            for i in range(self.col + step, col, step):
                # if there is a friendly piece at the position (i, col) for the first time => return
                for piece in pieces:
                    if piece.row == self.row and piece.col == i:
                        return
            self.col = col

