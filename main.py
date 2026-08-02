from flask import Flask, request, jsonify
from routes.users_route import users_bp
from routes.posts_route import posts_bp
from db import *
from logger import logger_setup
import logging

app = Flask(__name__)
app.secret_key = 'KJ08654'

#init database
init_users_db()
init_posts_db()
profile_db()
followers_db()


#register blueprints
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)

if __name__ == '__main__':
    app.run(debug=True)