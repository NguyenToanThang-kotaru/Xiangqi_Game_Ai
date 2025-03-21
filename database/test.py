import requests
import mysql.connector
import re
import time

# ====== Cấu hình MySQL ======
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "xiangqi"
}

# ====== Kết nối MySQL ======
class DBManager:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("✅ Kết nối MySQL thành công!")
        except mysql.connector.Error as err:
            print(f"❌ Lỗi kết nối MySQL: {err}")
            self.conn = None

    def insert_training_data(self, game_id, move_number, prev_fen, move, new_fen, score, player):
        """Lưu dữ liệu nước đi vào bảng training_data"""
        if not self.conn:
            print("⚠️ Không có kết nối MySQL, bỏ qua việc lưu dữ liệu.")
            return
        
        result = "win" if score > 0 else "loss" if score < 0 else "draw"
        
        try:
            insert_query = """
                INSERT INTO training_data (game_id, move_number, prev_fen, move, new_fen, score, player, result, frequency) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (game_id, move_number, prev_fen, move, new_fen, score, player, result, 1))
            self.conn.commit()
            print(f"✅ Thêm mới: {prev_fen} -> {move} -> {new_fen} ({result})")
        except mysql.connector.Error as err:
            print(f"❌ Lỗi MySQL khi chèn dữ liệu: {err}")

    def close(self):
        """Đóng kết nối MySQL."""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("🔌 Kết nối MySQL đã đóng.")

# ====== Lấy nước đi tốt nhất từ API ======
def get_best_move(fen):
    """Gửi FEN lên API và lấy nước đi tốt nhất"""
    url = f"http://www.chessdb.cn/chessdb.php?action=queryall&board={fen}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and response.text.strip():
            match = re.search(r"move:([a-z0-9]+),score:([-]?\d+)", response.text)
            if match:
                return match.group(1), int(match.group(2))  # (Nước đi, Điểm số)
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi API: {e}")
    return None, None

# ====== Lưu dữ liệu nước đi ======
def simulate_game(initial_fen, db, game_id, max_moves=50):
    """Lấy nước đi từ API và lưu vào database"""
    current_fen = initial_fen
    player = "red"  # Bắt đầu với bên đỏ
    
    print(f"🏁 Bắt đầu ván cờ mới! Game ID: {game_id}")
    print(f"📌 Trạng thái khởi đầu: {current_fen}")
    
    for move_count in range(1, max_moves + 1):
        best_move, score = get_best_move(current_fen)
        if not best_move:
            print("❌ Không tìm được nước đi hợp lệ! Dừng trò chơi.")
            break

        # Giả lập trạng thái FEN mới bằng cách thêm nước đi
        new_fen = f"{current_fen} -> {best_move}"
        
        # Lưu dữ liệu vào MySQL
        db.insert_training_data(game_id, move_count, current_fen, best_move, new_fen, score, player)
        
        current_fen = new_fen  # Cập nhật trạng thái mới
        player = "black" if player == "red" else "red"  # Đổi bên đi
        time.sleep(1)  # Nghỉ 1 giây trước lượt tiếp theo
    
    print("🏆 Trò chơi kết thúc!")

# ====== Chạy chương trình ======
if __name__ == "__main__":
    db = DBManager()
    if db.conn:
        initial_fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C2B2C1/9/RNBAKA1NR b"
        game_id = int(time.time())  # Sử dụng timestamp làm game_id
        simulate_game(initial_fen, db, game_id)
        db.close()