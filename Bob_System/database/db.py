import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            template_position INTEGER,
            master_secret BLOB
        )
    """)

    conn.commit()
    conn.close()

def insert_or_replace_user(user_id, template_position, master_secret):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, template_position, master_secret)
        VALUES (?, ?, ?)
    """, (user_id, template_position, master_secret))

    conn.commit()
    conn.close()

def get_user_by_position(template_position):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, master_secret FROM users
        WHERE template_position = ?
    """, (template_position,))

    result = cursor.fetchone()
    conn.close()
    return result