import jwt
from db_utils.connection import mongo
from flask import session

SECRET_KEY = 'your-secret-key'


def get_logged_token():
    user_token = session.get('auth_token')
    return user_token


def get_logged_user_info():
    token = get_logged_token()
    if token:
        try:
            # decoded_token = jwt.decode(token)
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            logged_user = decoded_token["user"]

            user_document = mongo.db.users.find_one({"username": logged_user})
            if user_document:
                user_object_id = str(user_document["_id"])
                return {"username": logged_user, "objectId": user_object_id}
            else:
                return {"message": "User not found"}, 404
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, 401
    else:
        print('token not fount')
        return None
