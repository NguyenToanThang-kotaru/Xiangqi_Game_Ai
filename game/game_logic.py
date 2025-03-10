import math
selected_piece = None
global CELL_SIZE
CELL_SIZE = 40
PIECE_RADIUS = CELL_SIZE // 2
        
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
    # print("col",col)
    # print("row",row)
    if selected_piece and (0<=col<=8) and (0<=row<=9):
        print(f"before Quân cờ: {selected_piece.name}, Vị trí: ({selected_piece.x}, {selected_piece.y})") 
        selected_piece.move(col,row)
        print(f"after Quân cờ: {selected_piece.name}, Vị trí: ({selected_piece.x}, {selected_piece.y})") 
        # for piece in pieces:
        #     if(piece.y==9):
        #         print(f"Quân cờ: {piece.name}, Vị trí: ({piece.x}, {piece.y})")
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
        
