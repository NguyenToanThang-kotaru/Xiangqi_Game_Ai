import mysql.connector

def connect_db():
    # Kết nối đến MySQL mà không chọn database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    return conn

# 1. Kết nối MySQL ban đầu (chưa chọn database)
conn = connect_db()
cursor = conn.cursor()

# 2. Tạo database nếu chưa tồn tại
cursor.execute("CREATE DATABASE IF NOT EXISTS Xiangqi")

# 3. Đóng kết nối cũ
cursor.close()
conn.close()

# 4. Kết nối lại nhưng lần này chọn database "Xiangqi"
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Xiangqi"
)
cursor = conn.cursor()

# 5. Tạo bảng users
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL,
        elo INT DEFAULT 1200
    )
""")

sql = "INSERT INTO users (username, password, elo) VALUES (%s, %s, %s)"
values = ("player1", "123456", 1200)

cursor.execute(sql,values)
conn.commit()

# 6. Đóng kết nối
cursor.close()
conn.close()