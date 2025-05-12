import requests
import sys
import os
import mysql.connector
import time  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.db_manager import connect_db
from game.board import Board
from tkinter import Tk, Canvas
total_count = 0
# Tạo root nhưng không hiển thị cửa sổ

conn = connect_db()
cursor = conn.cursor()

def is_data_existing(fen, move):
    """Kiểm tra xem FEN và nước đi đã tồn tại trong database chưa"""
    cursor.execute("SELECT COUNT(*) FROM ai_training_data WHERE fen = %s AND move = %s", (fen, move))
    exists = cursor.fetchone()[0] > 0
    if exists:
        print(f"⚠️ Bỏ qua: {fen} → {move} đã có trong DB.")
    return exists

def fetch_and_store_moves(fen_string, max_retries=5):
    """Gọi API, kiểm tra và lưu dữ liệu mới vào database"""
    import requests, time

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
                move = None
                winrate = 50.0  # giá trị mặc định nếu không tìm thấy

                for part in parts:
                    if part.startswith("move:"):
                        move = part.split(":", 1)[1]
                    elif part.startswith("winrate:"):
                        try:
                            winrate = float(part.split(":", 1)[1].replace("\x00", "").strip())
                        except ValueError:
                            print(f"❌ Lỗi parsing winrate: {part}. Sử dụng giá trị mặc định.")
                            winrate = 50.0  # fallback nếu lỗi parsing

                if move:  # chỉ lưu nếu có nước đi hợp lệ
                    new_moves.append({"move": move, "winrate": winrate})

            return new_moves

        except requests.exceptions.RequestException as e:
            print(f"🚨 Lỗi kết nối API: {e}. Thử lại ({attempt + 1}/{max_retries})...")
            time.sleep(2)

    print("❌ Lỗi API liên tục, bỏ qua trạng thái này.")
    return []



def update_fen(board,fen, move):
    """Cập nhật FEN dựa trên nước đi, đổi lượt đi"""
    board.set_fen(fen)  
    board.apply_move(move)  
    new_fen = board.to_fen()  
    return new_fen  

def crawl_data(start_fen, max_depth=3, request_delay=1.0, batch_size=1000):
    stack = [(start_fen, 0)]  # Khởi tạo với FEN ban đầu
    visited = set()
    root = Tk()
    root.withdraw()  
    fake_canvas = Canvas(root, width=1, height=1)
    fake_canvas.pack()

    tempboard = Board(fake_canvas, "")  # Khởi tạo bàn cờ
    insert_batch = []  # Danh sách chứa các bản ghi cần insert
    red_moves_count = 0  # Đếm số lượt đi của quân đỏ

    while stack:
        print(f"🔍 Stack hiện tại: {stack}")
        current_fen, level = stack.pop(0)  # FIFO

        if level > max_depth :
            print(f"⚠️ Đã dừng tại FEN: {current_fen}, level: {level}")
            continue  # Bỏ qua nếu đã duyệt hoặc vượt quá độ sâu

        # Gọi API lấy danh sách nước đi từ current_fen
        new_moves = fetch_and_store_moves(current_fen)
        time.sleep(request_delay)

        if not new_moves:
            print(f"❌ Không có nước đi từ FEN: {current_fen}")
            continue  # Nếu không có nước đi mới, bỏ qua

        print(f"🔍 Nước đi từ FEN {current_fen}: {new_moves}")
        
        for move_data in new_moves:
            move = move_data["move"]
            winrate = move_data["winrate"]
            if winrate > 40:  # Chỉ lưu nếu winrate hợp lý
                # Lưu nước đi vào database
                if not is_data_existing(current_fen, move):
                    insert_batch.append((current_fen, move, winrate))
                    print(f"✅ Lưu thành công: {current_fen} -> {move} với winrate {winrate}")
                
                if winrate > 60:
                    insert_batch.append((current_fen, move, winrate))
                    print(f"✅ Lưu thành công: {current_fen} -> {move} với winrate {winrate} X2 đã trùng lại")      

                # Tạo FEN mới sau khi thực hiện move → để tiếp tục crawl
                new_fen = update_fen(tempboard, current_fen, move)
                print(f"♻️ Cập nhật FEN mới: {new_fen}")

                # Kiểm tra xem FEN đã duyệt chưa
                if new_fen not in visited:
                    print(f"🔍 Thêm FEN mới vào stack: {new_fen}")
                    stack.insert(0, (new_fen, level + 1))  # Thêm FEN mới vào stack
                    visited.add(new_fen)

        # Commit nếu batch đã đủ lớn
        if len(insert_batch) >= batch_size:
            cursor.executemany("""
                INSERT INTO ai_training_data (fen, move, winrate)
                VALUES (%s, %s, %s)
            """, insert_batch)
            conn.commit()  # Commit vào cơ sở dữ liệu
            print(f"✅ Đã commit {len(insert_batch)} bản ghi vào cơ sở dữ liệu.")
            insert_batch = []  # Reset danh sách sau khi commit

    root.destroy()  # Đóng cửa sổ Tkinter sau khi hoàn thành

    # Commit nếu còn dữ liệu trong batch khi vòng lặp kết thúc
    if insert_batch:
        cursor.executemany("""
            INSERT INTO ai_training_data (fen, move, winrate)
            VALUES (%s, %s, %s)
        """, insert_batch)
        conn.commit()
        print(f"✅ Đã commit {len(insert_batch)} bản ghi vào cơ sở dữ liệu.")


# def crawl_data(start_fen, max_depth=3, request_delay=1.0):
#     stack = [(start_fen, 0)]
#     visited = set()
#     root = Tk()
#     root.withdraw()  
#     fake_canvas = Canvas(root, width=1, height=1)
#     fake_canvas.pack()

#     tempboard = Board(fake_canvas,"")  # Khởi tạo bàn cờ
#     while stack:
#         current_fen, level = stack.pop(0)

#         if level > max_depth or current_fen in visited:
#             continue
#         visited.add(current_fen)

#         # Gọi API lấy danh sách nước đi từ current_fen
#         new_moves = fetch_and_store_moves(current_fen)
#         time.sleep(request_delay)

#         if not new_moves:
#             continue

#         for move_data in new_moves:
#             move = move_data["move"]
#             winrate = move_data["winrate"]
#             if(winrate > 40):                                    
#                 # ✅ Lưu lại đúng: nước đi xuất phát từ current_fen
#                 if not is_data_existing(current_fen, move):
#                     cursor.execute("""
#                         INSERT INTO ai_training_data (fen, move, winrate)
#                         VALUES (%s, %s, %s)
#                     """, (current_fen, move, winrate))
#                     conn.commit()
#                     print(f"✅ Lưu thành công: {current_fen} -> {move} với winrate {winrate}")
#                 if winrate > 60:
#                     cursor.execute("""
#                         INSERT INTO ai_training_data (fen, move, winrate)
#                         VALUES (%s, %s, %s)
#                     """, (current_fen, move, winrate))
#                     conn.commit()       
#                     print(f"✅ Lưu thành công: {current_fen} -> {move} với winrate {winrate} X2 đã trùng lại")      

#                 # ✅ Tạo FEN mới sau khi thực hiện move → để tiếp tục crawl
#                 new_fen = update_fen(tempboard,current_fen, move)
#                 print(f"♻️ Cập nhật FEN mới: {new_fen}")
#                 stack.append((new_fen, level + 1))


initial_fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
crawl_data(initial_fen, max_depth=3)

cursor.close()
conn.close()