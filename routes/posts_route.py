from flask import Blueprint, request, jsonify, render_template, session,redirect
from models.posts_model import *
from models.users_model import *
from db import *
from logger import logger_setup
import logging
import time
import os
import uuid

logger = logger_setup()

posts_bp=Blueprint('posts_bp',__name__)

# HOME
@posts_bp.route('/home',methods=['GET'])
def home():
    if 'username' not in session:
        return redirect('/login')
    
    username = session['username']
    posts = get_post_randomly(username)
    userpics = get_all_profile(username)

    

    return render_template('home.html',username=username,posts=posts,userpics=userpics)
    
    # return render_template('home.html')

UPLOAD_FOLDER = "static/users/"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


#search posts
@posts_bp.route('/search', methods=['GET'])
def search_posts():
    if 'username' not in session:
        logger.warning('Unauthorized access attempt to search posts')
        return jsonify({'error': 'Unauthorized'}), 401
    
    return render_template('search.html')
    # query = request.args.get('query', '')
    # # Logic to search posts based on the query
    # # You can implement this based on your data storage and structure
    # logger.info(f'Post search attempt by user: {session["username"]} with query: {query}')
    # return jsonify({'message': f'search results for query: {query}'})

# ADD POST
@posts_bp.route('/add', methods=['GET', 'POST'])
def add_post_route():
    if request.method == 'POST':

        if 'username' not in session:
            return redirect('/login')
        

        username = session['username']

        # folder inside project directory
        UPLOAD_FOLDER = os.path.join(
            "static",
            "users",
            username
        )

        # create folder if missing
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        caption = request.form.get('caption')
        image = request.files.get('user_img')

        if image is None or image.filename == "":
            return render_template("add.html", error="Please upload an image")

        ext = os.path.splitext(image.filename)[1]

        filename = (
            session['username']
            + "_"
            + str(uuid.uuid4())
            + ext
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        add_post(username, filename, caption)
        image.save(filepath)

        return redirect('/user_posts')

    return render_template("add.html")

#notification
@posts_bp.route('/notification', methods=['GET'])
def notification():
    return render_template('notification.html')

#profile
@posts_bp.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')

#user posts
@posts_bp.route('/user_posts')
def user_posts():
    if 'username' not in session:
        return redirect('/login')
    
    username = session['username']

    posts = get_all_posts(username)
    
    return render_template(
        'user_posts.html',
        posts=posts,
        username=username
    )

@posts_bp.route('/edit_post', methods=['GET', 'POST'])
def edit_post():

    if 'username' not in session:
        return redirect('/login')

    post_id = request.args.get('post_id')
    post = get_post_by_id(post_id)

    if request.method == 'POST':

        caption = request.form['caption']
        image_name = post['post']

        new_image = request.files['new_image']

        if new_image and new_image.filename:

            # Delete old image
            old_image_path = os.path.join(
                'static',
                'users',
                session['username'],
                post['post']
            )

            if os.path.exists(old_image_path):
                os.remove(old_image_path)

            # Save new image
            ext = os.path.splitext(new_image.filename)[1]

            image_name = (
                session['username']
               + "_"
               + str(uuid.uuid4())
               + ext
            )

            new_image.save(
                os.path.join(
                    'static',
                    'users',
                    session['username'],
                    image_name
                )
            )
        else:
            image_name = post['post']

        update_post(image_name, caption, post_id)

        return redirect('/user_posts')

    return render_template(
        'edit_post.html',
        username=session['username'],
        post=post
    )

@posts_bp.route('/delete_post', methods=['GET', 'POST'])
def delete_post():
    post_id = request.args.get('post_id')

    post = get_post_by_id(post_id)
    delete_post_by_id(post_id)
    

    image_path = os.path.join(
        'static',
        'users',
        session['username'],
        post['post']
    )

    if os.path.exists(image_path):
        os.remove(image_path)


    return redirect('/user_posts')

@posts_bp.route('/view/<username>/posts')
def view_posts(username):
    posts = get_all_posts(username)

    return render_template(
        "view_user_posts.html",
        username=username,
        posts=posts
    )
