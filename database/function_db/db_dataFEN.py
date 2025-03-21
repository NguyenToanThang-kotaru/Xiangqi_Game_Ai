import requests
from bs4 import BeautifulSoup

# FEN của bàn cờ
fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/6P2/P1P1P3P/1C5C1/9/RNBAKABNR_b"
url = f"https://chessdb.cn/query_en/?{fen}"

# Gửi request với User-Agent để tránh bị chặn
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)

# Phân tích HTML
soup = BeautifulSoup(response.text, "html.parser")

# Tìm bảng nước đi
move_table = soup.find("table", class_="movelist")

if move_table:
    rows = move_table.find_all("tr")[1:]  # Bỏ qua hàng tiêu đề
    move_list = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            move_span = cols[0].find("span")  # Lấy nội dung trong <span>
            move = move_span.text.strip() if move_span else cols[0].text.strip()
            rank = cols[1].text.strip()
            score = cols[2].text.strip()
            move_list.append((move, rank, score))

    # In danh sách nước đi
    for move, rank, score in move_list:
        print(f"Nước đi: {move}, Xếp hạng: {rank}, Điểm số: {score}")

else:
    print("Không tìm thấy bảng nước đi.")
