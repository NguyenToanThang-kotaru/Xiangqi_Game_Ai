import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.db_manager import connect_db


def check_login(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    queery = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(queery, (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None


