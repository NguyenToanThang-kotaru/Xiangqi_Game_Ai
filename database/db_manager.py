import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Xiangqi"
    )
    return conn
conn = connect_db()
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
# CREATE TABLE ai_training_data (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     fen TEXT NOT NULL,
#     move VARCHAR(10) NOT NULL,
#     score INT NOT NULL,
#     rank INT NOT NULL,
#     winrate FLOAT
# );
