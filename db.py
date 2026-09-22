import sqlite3
from config import POSTS_DB_PATH, USERS_DB_PATH

def get_post_conn():
    conn = sqlite3.connect(POSTS_DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_conn():
    conn = sqlite3.connect(USERS_DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_posts_db():
    conn = get_post_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        post TEXT,
        caption TEXT
    )
    """)

    conn.commit()
    conn.close()

def init_users_db():
    conn = get_user_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

def profile_db():
    conn = get_user_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_pic TEXT,
        username TEXT UNIQUE,
        bio TEXT,
        gender TEXT
    )
    """)

    conn.commit()
    conn.close()

def followers_db():

    conn = get_user_conn()

    try:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS followers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower TEXT NOT NULL,
                following TEXT NOT NULL,
                UNIQUE(follower, following)
            )
        """)

        conn.commit()

    finally:
        conn.close()