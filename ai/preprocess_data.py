import mysql.connector
import pandas as pd

# Kết nối Database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="xiangqi"
    )

# Ánh xạ ký hiệu quân cờ thành số
PIECE_MAPPING = {
    'r': 1, 'n': 2, 'b': 3, 'a': 4, 'k': 5, 'c': 6, 'p': 7,  # Quân đen
    'R': 8, 'N': 9, 'B': 10, 'A': 11, 'K': 12, 'C': 13, 'P': 14,  # Quân đỏ
    '/': -1,  # Phân tách hàng
    '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0
}

# Chuyển FEN thành mảng số
def fen_to_array(fen):
    PIECE_MAPPING = {
        'r': 1, 'n': 2, 'b': 3, 'a': 4, 'k': 5, 'c': 6, 'p': 7,  
        'R': 8, 'N': 9, 'B': 10, 'A': 11, 'K': 12, 'C': 13, 'P': 14,  
    }

    parts = fen.split()
    board_fen = parts[0]  # Phần bàn cờ
    turn = parts[1]  # Lượt đi

    board_array = []
    
    for char in board_fen:
        if char in PIECE_MAPPING:  # Nếu là quân cờ
            board_array.append(PIECE_MAPPING[char])
        elif char.isdigit():  # Nếu là số (ô trống)
            board_array.extend([0] * int(char))  # Thêm đúng số lượng số 0
        elif char == '/':  # Dấu `/` không cần lưu
            continue  

    # Thêm lượt đi vào mảng số (0 nếu là 'w', 1 nếu là 'b')
    turn_value = 0 if turn == 'w' else 1

    return board_array + [turn_value]

# Chuyển Move thành tọa độ số
def move_to_vector(move):
    columns = 'abcdefghi'  # Cột trong ICCS
    start_col = columns.index(move[0]) + 1  # Chuyển từ 0-based -> 1-based
    start_row = 10 - int(move[1])  # Chuyển hàng về 1-10 (cờ tướng từ trên xuống)
    end_col = columns.index(move[2]) + 1
    end_row = 10 - int(move[3])
    
    return [start_col, start_row, end_col, end_row]

# Tiền xử lý dữ liệu
def preprocess_data():
    conn = connect_db()
    cursor = conn.cursor()
    # Lấy dữ liệu từ database
    cursor.execute("SELECT fen, move, score, winrate FROM ai_training_data")
    rows = cursor.fetchall()
    processed_data = []
    for row in rows:
        fen, move, score, winrate = row
        fen_array = fen_to_array(fen)
        move_vector = move_to_vector(move)
    
        turn_value = fen_array[-1]  # Lấy giá trị turn từ cuối mảng FEN
        processed_data.append(fen_array[:-1] + [turn_value] + move_vector + [score, winrate])

    
    df = pd.DataFrame(processed_data)

    df.fillna(0, inplace=True)  # Xử lý NaN nếu có
    df.to_csv("dataset/processed_data_cleaned.csv", index=False)


    df.fillna(0, inplace=True)  # Thay thế NaN bằng 0
    df.to_csv("dataset/processed_data_cleaned.csv", index=False)


    cursor.close()
    conn.close()

# Chạy tiền xử lý
preprocess_data()


df = pd.read_csv("dataset/processed_data_cleaned.csv")
print("📜 Danh sách cột trong dữ liệu huấn luyện (sau khi sua):")
print(df.columns)
print(f"📊 Số lượng cột thực tế trong dataset: {df.shape[1]}")
