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

    return board_array ,turn_value

# Chuyển Move thành tọa độ số
def move_to_vector(move):
    columns = 'abcdefghi'  # Cột trong ICCS
    start_col = columns.index(move[0])   # Chuyển từ 0-based -> 1-based
    start_row = 9 - int(move[1])  # Chuyển hàng về 1-10 (cờ tướng từ trên xuống)
    end_col = columns.index(move[2]) 
    end_row = 9 - int(move[3])
    
    return [start_col, start_row, end_col, end_row]

# Tiền xử lý dữ liệu
# Tiền xử lý dữ liệu
def preprocess_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Lấy dữ liệu từ database (chỉ lấy 3 cột: fen, move, winrate)
    cursor.execute("SELECT fen, move, winrate FROM ai_training_data")
    rows = cursor.fetchall()

    processed_data = []

    for row in rows:
        fen, move, winrate = row
        fen_array, turn_value = fen_to_array(fen)
        move_vector = move_to_vector(move)
        print(f"turn_value: {turn_value}")
        print(f"🔍 Debug FEN: {fen}")
        print(f"🔍 Debug Move: {move}")
        # Chỉ cần fen_array, turn_value và winrate làm đặc trưng
        features = fen_array + [turn_value] + [winrate]
        
        # Dự đoán nước đi, nước đi là nhãn
        target = move_vector
        
        # Thêm vào danh sách dữ liệu đã xử lý
        processed_data.append(features + target)  # Đặc trưng + Nước đi (move_vector)

    print(f"🔍 Debug FEN: {fen}")
    print(f"🔍 FEN Array Length: {len(fen_array)}")
    print(f"🔍 FEN Array: {fen_array}")
    
    # Xuất dữ liệu ra CSV và xử lý NaN
    df = pd.DataFrame(processed_data)

    df.fillna(0, inplace=True)  # Xử lý NaN nếu có
    df.to_csv("dataset/processed_data_cleaned.csv", index=False)
    
    print(f"📊 FEN Array Length: {len(fen_array)}")   # 64
    print(f"📊 Move Vector Length: {len(move_vector)}")  # 4
    print(f"📊 Winrate: 1")  # 1 giá trị
    print(f"📊 Tổng số đặc trưng tính toán: {len(fen_array) + 1 + 1 + len(move_vector)}")  # Đặc trưng + Winrate + Move

    print("✅ Dữ liệu đã được tiền xử lý, làm sạch và lưu vào processed_data_cleaned.csv!")

    cursor.close()
    conn.close()

# Chạy tiền xử lý
preprocess_data()


df = pd.read_csv("dataset/processed_data_cleaned.csv")
print("📜 Danh sách cột trong dữ liệu huấn luyện (sau khi sua):")
print(df.columns)
print(f"📊 Số lượng cột thực tế trong dataset: {df.shape[1]}")
