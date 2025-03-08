import math
selected_piece = None
global CELL_SIZE
CELL_SIZE = 40
PIECE_RADIUS = CELL_SIZE // 2
def on_click(event, canvas, pieces):
    global selected_piece
    col = event.x // CELL_SIZE - 1
    row = event.y // CELL_SIZE - 1

    for piece in pieces:
        if piece.get_pixel_y == col and piece.get_pixel_x == row:
            selected_piece = piece
            print(f"Chọn quân: {piece.name} tại ({col}, {row})")
            return
    
    if selected_piece:
        print(f"Di chuyển {selected_piece.name} đến ({col}, {row})")
        selected_piece.move(col, row)
        selected_piece = None  # Bỏ chọn quân
        
def get_piece_by_position(x_click, y_click, pieces):
    nearest_piece = None
    min_distance = float("inf")
    for piece in pieces:  # Sửa 'Piece' thành 'piece'
        x_piece = piece.x * CELL_SIZE + CELL_SIZE // 2  # Tọa độ tâm quân cờ
        y_piece = piece.y * CELL_SIZE + CELL_SIZE // 2  
       
        distance = math.sqrt((x_click - x_piece) ** 2 + (y_click - y_piece) ** 2)
        # print("toa do",x_click, y_click)
        # print("quan co",piece.name, x_piece, y_piece)
        # print("khoang cach la",distance)
        if distance < min_distance and distance <= PIECE_RADIUS:  # Chỉ so sánh với min_distance
            nearest_piece = piece
            print("toa do",x_click, y_click)
            print("quan co",piece.name, x_piece, y_piece)
            print("khoang cach la",distance)
            min_distance = distance
    # print(nearest_piece.name)
    return nearest_piece



    # for Piece in create_pieces(canvas):
    #     print(Piece)
def on_click(event,pieces):
    global selected_piece
    x = (event.x / CELL_SIZE * CELL_SIZE)-20
    y = (event.y / CELL_SIZE * CELL_SIZE )-15
    piece = get_piece_by_position(x, y, pieces)
    col = round(event.x / CELL_SIZE)-1  
    row = round(event.y / CELL_SIZE)-1
    print("col",col)
    print("row",row)
    if selected_piece:
        selected_piece.move(col,row)
        
        selected_piece=None
    else:
        if piece:  
            # if selected_piece == piece:
            #     print("Bỏ chọn quân cờ:", selected_piece.name)
            #     selected_piece = None
            # else:
                selected_piece = piece
                print("Đã chọn quân cờ:", selected_piece.name)
        # if selected_piece:
        
    # else:
        # print("Không có quân cờ nào ở đây")
        
