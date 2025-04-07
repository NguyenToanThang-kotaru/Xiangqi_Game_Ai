raw_data = """move:h2e2,score:1,rank:2,winrate:50.08|move:b2e2,score:1,rank:2,winrate:50.08|move:g3g4,score:1,rank:2,winrate:50.08|move:c3c4,score:1,rank:2,winrate:50.08|move:b0c2,score:1,rank:2,winrate:50.08|move:h0g2,score:1,rank:2,winrate:50.08|move:h2i2,score:1,rank:2,winrate:50.08|move:b2a2,score:1,rank:2,winrate:50.08|move:g0e2,score:1,rank:2,winrate:50.08|move:c0e2,score:1,rank:2,winrate:50.08|move:h2d2,score:1,rank:2,winrate:50.08|move:b2f2,score:1,rank:2,winrate:50.08|move:b2d2,score:0,rank:2,winrate:50.00|move:h2f2,score:0,rank:2,winrate:50.00|move:h0i2,score:0,rank:2,winrate:50.00|move:b0a2,score:0,rank:2,winrate:50.00|move:h2g2,score:0,rank:2,winrate:50.00|move:b2c2,score:0,rank:2,winrate:50.00|move:d0e1,score:0,rank:2,winrate:50.00|move:f0e1,score:0,rank:2,winrate:50.00|move:i3i4,score:0,rank:2,winrate:50.00|move:a3a4,score:0,rank:2,winrate:50.00|move:b2g2,score:-1,rank:2,winrate:49.92|move:h2c2,score:-1,rank:2,winrate:49.92|move:b2b4,score:-3,rank:1,winrate:49.77|move:h2h4,score:-3,rank:1,winrate:49.77|move:h2h6,score:-32,rank:0,winrate:47.58|move:b2b6,score:-32,rank:0,winrate:47.58|move:h2h1,score:-50,rank:0,winrate:46.22|move:b2b1,score:-50,rank:0,winrate:46.22|move:h2h3,score:-99,rank:0,winrate:42.56|move:b2b3,score:-99,rank:0,winrate:42.56|move:g0i2,score:-106,rank:0,winrate:42.04|move:c0a2,score:-106,rank:0,winrate:42.04|move:h2h5,score:-141,rank:0,winrate:39.48|move:b2b5,score:-141,rank:0,winrate:39.48|move:a0a2,score:-149,rank:0,winrate:38.90|move:i0i2,score:-149,rank:0,winrate:38.90|move:e3e4,score:-170,rank:0,winrate:37.40|move:i0i1,score:-176,rank:0,winrate:36.97|move:a0a1,score:-176,rank:0,winrate:36.97|move:e0e1,score:-207,rank:0,winrate:34.81|move:b2b9,score:-314,rank:0,winrate:27.86|move:h2h9,score:-314,rank:0,winrate:27.86"""

# Chuyển dữ liệu API thành danh sách dictionary
moves = []
for item in raw_data.split("|"):
    move_data = {}
    for pair in item.split(","):
        key, value = pair.split(":")
        if key in ["score", "rank"]:  # Chuyển đổi số nguyên
            move_data[key] = int(value)
        elif key == "winrate":  # Chuyển đổi số thực
            move_data[key] = float(value)
        else:
            move_data[key] = value  # Giữ nguyên chuỗi
    moves.append(move_data)

# ✅ In danh sách nước đi chưa sắp xếp
for move in moves[:5]:
    print(move)