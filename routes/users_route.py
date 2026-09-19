from flask import Blueprint, request, jsonify, redirect, render_template, session, flash
from hash_pass import hash_password
import hashlib
from models.users_model import *
from models.posts_model import *
from logger import logger_setup
import logging
import os
import time
from werkzeug.utils import secure_filename
import shutil

logger = logger_setup()

users_bp=Blueprint('users_bp',__name__)

# WELCOME
@users_bp.route('/')
def welcome():
    return render_template('index.html')

@users_bp.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':

        return render_template('signup.html')
    

    elif request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        hashed_password = hash_password(password)

        add_login_info(username, hashed_password)

        folder_path = os.path.join(
        'static',
        'users',
        username
        )

        os.makedirs(folder_path, exist_ok=True)

        logger.info(f'New user registered: {username}')
        return redirect('/login')

@users_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_info = get_login_info(username)
        if user_info and hash_password(password) == user_info[2]:
            session['username'] = username
            logger.info(f'User logged in: {username}')
            return redirect('/home')
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "profile_pics"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():

    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    if request.method == 'POST':

        old_profile = get_profile(username)

        # Keep existing profile picture
        filename = old_profile[1] if old_profile else None

        file = request.files.get("profile_pic")

        if file and file.filename:

            if allowed_file(file.filename):
                # Delete old picture
                if old_profile and old_profile[1]:

                    old_path = os.path.join(
                       UPLOAD_FOLDER,
                    old_profile[1]
                )

                if os.path.exists(old_path):
                    os.remove(old_path)

                filename = str(time.time()) + "_" + secure_filename(file.filename)

                filepath = os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )

                # Save new picture
                file.save(filepath)
            else:
                flash("Unsupported file type. Please upload a PNG, JPG, JPEG or WEBP image.", "error")

        bio = request.form.get('bio')
        gender = request.form.get('gender')

        save_profile(
            username,
            bio,
            gender,
            filename
        )

        return redirect('/profile')

    profile_data = get_profile(username)

    return render_template(
        'profile.html',
        profile=profile_data
    )

# LOGOUT
@users_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    logger.info(f'User logged out: {session.get("username")}')
    return redirect('/login')

@users_bp.route('/delete', methods=['GET'])
def delete():

    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    # Delete user data from databases
    delete_profile_pic(username)
    # delete_posts(username)
    delete_profile(username)
    delete_user(username)

    # Delete user's folder
    folder_path = os.path.join(
        'static',
        'users',
        username
    )

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    session.clear()

    logger.info(f'user account deleted : {session.get("username")}')

    return redirect('/signup')

@users_bp.route("/search_api")
def search():
    query = request.args.get("q", "")
    username = session['username']

    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT username, profile_pic
    FROM profile
    WHERE username LIKE ?
    AND username != ?
    LIMIT 10
    """, (f"%{query}%", username))

    rows = cur.fetchall()
    conn.close()

    users = []

    for row in rows:
        users.append({
            "username": row["username"],
            "profile_pic": row["profile_pic"]
        })

    return jsonify(users)

@users_bp.route("/search")
def search_page():
    return render_template("search.html")

@users_bp.route('/view/<string:username>')
def view_user(username):
    profile = get_profile(username)
    return render_template('view_profile.html', profile=profile)