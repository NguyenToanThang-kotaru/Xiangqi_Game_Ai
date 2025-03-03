import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.db_manager import connect_db

# check if the username is unique
def check_username(username):
    conn = connect_db() # connect database
    cursor = conn.cursor() # create object to execute SQL
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None

def check_password(pw, re_pw):
    if pw == re_pw:
        return True
    return False

def add_account(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    queery = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(queery, (username, password))
    conn.commit()
    conn.close()
    cursor.close()