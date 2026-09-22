import sqlite3
from db import get_user_conn

def add_login_info(username,password):
    conn = get_user_conn()
    cur = conn.cursor()

    cur.execute('''
            INSERT OR IGNORE INTO users(username,password)
            VALUES(?,?)
    ''',(username,password))
    conn.commit()
    conn.close()

def get_login_info(username):
    conn = get_user_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    conn.close()
    return row if row else None

def get_all_users():
    conn = get_user_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    conn.close()
    users = [dict(row) for row in rows]
    return users

def save_profile(username, bio, gender,profile_pic):

    conn = get_user_conn()
    cur = conn.cursor()

    if profile_pic:
        cur.execute("""
        INSERT INTO profile (username, bio, gender, profile_pic)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            bio = excluded.bio,
            gender = excluded.gender,
            profile_pic = excluded.profile_pic
    """, (username, bio, gender, profile_pic))

    else:
        cur.execute("""
        INSERT INTO profile (username, bio, gender)
        VALUES (?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            bio = excluded.bio,
            gender = excluded.gender
    """, (username, bio, gender))
    
    conn.commit()
    conn.close()

def get_profile(username):

    conn = get_user_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM profile
    WHERE username = ?
    """, (username,))

    data = cur.fetchone()

    conn.close()

    return data

def delete_user(username):
    conn = get_user_conn()
    cur = conn.cursor()

    cur.execute('''
            DELETE FROM users WHERE username = ?
    ''',(username,))

    conn.commit()
    conn.close()

def delete_profile(username):
    conn = get_user_conn()
    cur = conn.cursor()

    cur.execute('''
            DELETE FROM profile WHERE username=?
    ''',(username,))

    conn.commit()
    conn.close()

def delete_profile_pic(username):

    conn = get_user_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT profile_pic FROM profile WHERE username=?",
        (username,)
    )

    row = cur.fetchone()

    conn.close()

    if row and row["profile_pic"]:

        pic_path = os.path.join(
            "static",
            "profile_pics",
            row["profile_pic"]
        )

        if os.path.exists(pic_path):
            os.remove(pic_path)

def get_all_profile(username):
    conn = get_user_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT username, profile_pic
        FROM profile
        WHERE username != ?
    """, (username,))

    rows = cur.fetchall()
    conn.close()

    profile_pics = {}

    for row in rows:
        profile_pics[row["username"]] = {
            "profile_pic": row["profile_pic"]
        }

    return profile_pics

def follow_user(follower, following):

    conn = get_user_conn()

    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT OR IGNORE INTO followers(follower, following)
            VALUES (?, ?)
        """, (follower, following))

        conn.commit()
    finally:
        conn.close()

def is_following(follower, following):
    conn = get_user_conn()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 1
            FROM followers
            WHERE follower = ? AND following = ?
        """, (follower, following))

        return cur.fetchone() is not None

    finally:
        conn.close()


def toggle_follow(follower, following):
    conn = get_user_conn()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 1
            FROM followers
            WHERE follower = ? AND following = ?
        """, (follower, following))

        exists = cur.fetchone()

        if exists:
            cur.execute("""
                DELETE FROM followers
                WHERE follower = ? AND following = ?
            """, (follower, following))

            following_status = False

        else:
            cur.execute("""
                INSERT INTO followers(follower, following)
                VALUES (?, ?)
            """, (follower, following))

            following_status = True

        conn.commit()

        return following_status

    finally:
        conn.close()
    

def get_following(username):
    conn = get_user_conn()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT following
            FROM followers
            WHERE follower = ?
        """, (username,))

        rows = cur.fetchall()

        return {row["following"] for row in rows}

    finally:
        conn.close()