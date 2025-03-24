import requests
import sys
import os
import mysql.connector
import time  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.db_manager import connect_db
from game.board import Board
from tkinter import Tk, Canvas

# Tạo root nhưng không hiển thị cửa sổ
root = Tk()
root.withdraw()  
fake_canvas = Canvas(root, width=1, height=1)

board = Board(fake_canvas)  # Khởi tạo bàn cờ
conn = connect_db()
cursor = conn.cursor()

def is_data_existing(fen, move):
    """Kiểm tra xem FEN và nước đi đã tồn tại trong database chưa"""
    cursor.execute("SELECT COUNT(*) FROM ai_training_data WHERE fen = %s AND move = %s", (fen, move))
    return cursor.fetchone()[0] > 0  

def fetch_and_store_moves(fen_string, max_retries=5):
    """Gọi API, kiểm tra và lưu dữ liệu mới vào database"""
    url = f"https://chessdb.cn/chessdb.php?action=queryall&board={fen_string}"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)  
            if "checkmate" in response.text.lower():
                print(f"🚨 Checkmate! Không lưu FEN: {fen_string}")
                return []  

            if response.status_code != 200 or not response.text.strip():
                print(f"❌ API lỗi, thử lại ({attempt + 1}/{max_retries})...")
                time.sleep(2)  
                continue

            moves_data = response.text.strip().split("|")  
            new_moves = []

            for move_str in moves_data:
                parts = move_str.split(",")  
                move, score, rank, winrate = None, 0, None, 50.0  

                for part in parts:
                    if part.startswith("move:"):
                        move = part.split(":")[1]
                    elif part.startswith("score:"):
                        score = int(part.split(":")[1])
                    elif part.startswith("rank:"):
                        rank = int(part.split(":")[1])
                    elif part.startswith("winrate:"):
                        winrate = float(part.split(":")[1].replace("\x00", "").strip())

                if move and not is_data_existing(fen_string, move):
                    cursor.execute("""
                        INSERT INTO ai_training_data (fen, move, score, rank, winrate)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (fen_string, move, score, rank, winrate))
                    conn.commit()
                    new_moves.append(move)
                    print(f"✅ Đã lưu: {fen_string} -> {move} (Winrate: {winrate})")

            return new_moves  

        except requests.exceptions.RequestException as e:
            print(f"🚨 Lỗi kết nối API: {e}. Thử lại ({attempt + 1}/{max_retries})...")
            time.sleep(2)  

    print("❌ Lỗi API liên tục, bỏ qua trạng thái này.")
    return []

def update_fen(fen, move):
    """Cập nhật FEN dựa trên nước đi, đổi lượt đi"""
    board.set_fen(fen)  
    board.apply_move(move)  
    new_fen = board.to_fen()  
    return new_fen  

def crawl_data(fen, depth=3, request_delay=2):
    """Duyệt cây trạng thái bằng DFS, tạo FEN mới sau mỗi nước đi"""
    visited_fen = set()
    stack = [(fen, 0)]  

    while stack:
        current_fen, level = stack.pop()

        if level >= depth:
            continue  

        if current_fen in visited_fen:
            continue  
        visited_fen.add(current_fen)

        new_moves = fetch_and_store_moves(current_fen)
        time.sleep(request_delay)  

        if not new_moves:
            continue  

        for move in new_moves:
            new_fen = update_fen(current_fen, move)  
            print(f"♻️ Cập nhật FEN mới: {new_fen}")

            if not is_data_existing(new_fen, move):
                cursor.execute("""
                    INSERT INTO ai_training_data (fen, move, score, rank, winrate)
                    VALUES (%s, %s, %s, %s, %s)
                """, (new_fen, move, 0, 0, 50.0))  
                conn.commit()

            stack.append((new_fen, level + 1))  

initial_fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
crawl_data(initial_fen, depth=3)

cursor.close()
conn.close()
