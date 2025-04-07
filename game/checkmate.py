from game.game_logic import GameLogic

logic = GameLogic()

def is_checkmated(piece, board_state, pieces):
    if is_checked(piece, board_state, pieces) == True:
        if not is_king_have_valid_move(piece, board_state, pieces):
            return True
    return False

def is_checked(piece, board_state, pieces):
    # check for the position if it's being checked by other pieces
    x, y = piece.x, piece.y # coorodinates of the king
    for enemy_piece in pieces:
        if enemy_piece.color == piece.color:
            continue
        if logic.check_move(enemy_piece, (x, y), board_state):
            print("checked")
            return True
    return False
    
    
# check if the king has valid moves
def is_king_have_valid_move(piece, board_state, pieces):
    valid_position = []

    col_min = 3
    col_max = 5
    row_min = row_max = 0

    if piece.color == "red":
        row_min = 7
        row_max = 9
    else:
        row_min = 0
        row_max = 2
    
    # check the valid moves for king (not count being checked by the other pieces)
    for x in range(col_min, col_max + 1):
        for y in range(row_min, row_max + 1):
            if logic.check_tuong_move(piece, x, y, board_state):
                valid_position.append((x, y))

    # check if valid positions are being attacked by other pieces (chatgpt)
    for (col, row) in valid_position:
        # Temporarily remove the King from it's original position and move to new valid_position
        old_x, old_y = piece.x, piece.y
        board_state[old_y][old_x] = None

        original_position = board_state[row][col]
        board_state[row][col] = piece
        piece.x, piece.y = col, row

        # Check if new position is not safe
        if not is_checked(piece, board_state, pieces):
            # Restore the board
            board_state[row][col] = original_position
            board_state[old_y][old_x] = piece
            piece.x, piece.y = old_x, old_y
            return True
        board_state[row][col] = original_position
        board_state[old_y][old_x] = piece
        piece.x, piece.y = old_x, old_y
    return False
