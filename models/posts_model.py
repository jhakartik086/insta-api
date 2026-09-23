import sqlite3
from db import get_post_conn

def add_post(username, post, caption):
    conn = get_post_conn()
    cur = conn.cursor()
    
    cur.execute('''INSERT INTO posts(username, post, caption) VALUES(?,?,?)''',(username, post, caption))

    conn.commit()
    conn.close()

def get_all_posts(username):
    conn = get_post_conn()
    cur = conn.cursor()

    cur.execute('''
            SELECT id, caption, post
            FROM posts
            WHERE username = ?
            ORDER BY id DESC
    ''',(username,))

    posts = cur.fetchall()

    conn.close()

    return posts

def update_post(post, caption, post_id):
    conn = get_post_conn()
    cur = conn.cursor()

    cur.execute(
        '''
        UPDATE posts
        SET caption = ?,
        post = ?
        WHERE id = ?
        ''',
        (caption, post, post_id)
    )

    conn.commit()
    conn.close()


def delete_post_by_id(post_id):

    conn = get_post_conn()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM posts WHERE id=?",
        (post_id,)
    )

    conn.commit()
    conn.close()

def like_post(post_id):
    conn = get_post_conn()
    cur = conn.cursor()

    cur.execute('''
            UPDATE posts
            SET likes = likes + 1
            WHERE id = ?
    ''',(post_id,))
    conn.commit()
    conn.close()

def dislike_post(post_id):
    conn = get_post_conn()
    cur = conn.cursor()

    cur.execute('''
            UPDATE posts
            SET likes = likes - 1
            WHERE id = ?
    ''',(post_id,))
    conn.commit()
    conn.close()

def get_post_by_id(post_id):

    conn = get_post_conn()
    cur = conn.cursor()

    cur.execute(
        '''
        SELECT *
        FROM posts
        WHERE id = ?
        ''',
        (post_id,)
    )

    post = cur.fetchone()

    conn.close()

    return post

def get_post_randomly(username):
    conn = get_post_conn()
    cur = conn.cursor()

    cur.execute('''
            SELECT * FROM posts
            WHERE username != ?
            ORDER BY RANDOM()
    ''',(username,)) 
    
    posts = cur.fetchall()
    conn.close()

    return posts