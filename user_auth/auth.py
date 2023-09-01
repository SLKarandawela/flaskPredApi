import bcrypt
import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from db_utils.connection import mongo
from flask import session


def generate_token(username):
    token = jwt.encode(
        {"user": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=600)},
        current_app.config["SECRET_KEY"],
    )
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "Token is invalid"}), 401

        return f(*args, **kwargs)

    return decorated


def register_user(username, password):
    existing_user = mongo.db.users.find_one({"username": username})
    if existing_user:
        return {"message": "Username already exists"}, 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = {
        "username": username,
        "password": hashed_password
    }

    mongo.db.users.insert_one(new_user)
    return {"message": "User registered successfully"}, 201


def login_user(username, password):
    user = mongo.db.users.find_one({"username": username})

    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        token = generate_token(username)
        session['auth_token'] = token
        return {"token": token, "message": "Login successful"}, 200
    else:
        return {"message": "Invalid credentials"}, 401
