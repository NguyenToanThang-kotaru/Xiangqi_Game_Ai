import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Xiangqi")
cursor.execute("USE Xiangqi")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL,
        elo INT DEFAULT 1200
    )
""")




cursor.close()
conn.close()
