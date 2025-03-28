from game.game_logic import GameLogic

logic = GameLogic()

def is_checkmated(piece, board_state, pieces):
    enemy_piece = is_checked(piece, board_state, pieces)
    if enemy_piece != None:
        if not is_king_have_valid_move(enemy_piece, board_state, pieces) and not is_other_pieces_have_valid_move(enemy_piece, piece, pieces, board_state):
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
            return enemy_piece
    return None
    
    
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

# check if there are valid moves for other pieces in order to block the attacking piece, or take the attacking piece
def is_other_pieces_have_valid_move(attacking_piece, king_piece, pieces, board_state):
    attacking_move = []
    block_checkmate = []

    x, y = king_piece.x, king_piece.y
    attacking_move.append((attacking_piece.x, attacking_piece.y))

    for col in range(9):
        for row in range(10):
            if logic.check_move(attacking_piece, (col, row), board_state):
                # check if the attacking_piece moved to that position can still attack the king
                original_x = attacking_piece.x
                original_y = attacking_piece.y
                tmp = board_state[attacking_piece.y][attacking_piece.x]
                board_state[attacking_piece.y][attacking_piece.x] = None
                board_state[row][col] = tmp
                attacking_piece.x, attacking_piece.y = col, row
                if logic.check_move(attacking_piece, (x, y), board_state):
                    attacking_move.append((col, row))
                board_state[row][col] = None
                board_state[original_y][original_x] = tmp
                attacking_piece.x, attacking_piece.y = original_x, original_y
    
    for piece in pieces:
        if piece.color == king_piece.color:
            for position in attacking_move:
                if logic.check_move(piece, position, board_state):
                    block_checkmate.append({piece: position})
    
    if block_checkmate == []:
        return False
    return True

    """
    
    aim: check if there are valid moves for other pieces in order to block the attacking piece, or take the attacking piece
    
    things that we need to use:
    king piece, attacking piece, pieces, board_state

    create attacking_move[] 

    add the attacking piece's position into attacking_move[]

    check all of the position of the attacking_piece lies at the original position, if there are position that could attack the king again, add it into attacking_move[]

    after that, for each piece that is friendly to the king, check if they can move legally to that position
    
    if yes, add it into block_checkmate[]
    and we can return the block_checkmate afterwards

    if no, continue the loop
    if there are no piece that can go to any position in attacking_move => return false
    """
