from flask_restful import Resource, reqparse, Api
from user_auth.auth import register_user, login_user, token_required
from db_utils.connection import configure_db
from flask import Flask, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"
mongo = configure_db(app)
api = Api(app)


class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", help="Username cannot be blank", required=True)
        parser.add_argument("password", help="Password cannot be blank", required=True)
        args = parser.parse_args()

        response, status_code = register_user(args["username"], args["password"])
        return response, status_code


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", help="Username cannot be blank", required=True)
        parser.add_argument("password", help="Password cannot be blank", required=True)
        args = parser.parse_args()

        response, status_code = login_user(args["username"], args["password"])
        return response, status_code


class ProtectedResource(Resource):
    @token_required
    def get(self):
        return {"message": "This is a protected resource"}


api.add_resource(UserRegistration, "/register")
api.add_resource(UserLogin, "/")
api.add_resource(ProtectedResource, "/protected")

# if __name__ == "__main__":
#     app.run(debug=True)
