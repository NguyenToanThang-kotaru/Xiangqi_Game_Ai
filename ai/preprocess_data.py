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
    board = []
    for char in fen:
        board.append(PIECE_MAPPING.get(char, 0))
    return board

# Chuyển Move thành tọa độ số
def move_to_vector(move):
    columns = 'abcdefghi'
    return [columns.index(move[0]), int(move[1]), columns.index(move[2]), int(move[3])]

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

        processed_data.append(fen_array + move_vector + [score, winrate])

    # Xuất dữ liệu ra CSV và xử lý NaN
    df = pd.DataFrame(processed_data)
    df.fillna(0, inplace=True)  # Thay thế NaN bằng 0
    df.to_csv("processed_data_cleaned.csv", index=False)

    print("✅ Dữ liệu đã được tiền xử lý, làm sạch và lưu vào processed_data_cleaned.csv!")

    cursor.close()
    conn.close()

# Chạy tiền xử lý
preprocess_data()
