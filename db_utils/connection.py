import os

from flask_pymongo import PyMongo
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def configure_db(app: Flask) -> PyMongo:
    app.config["MONGO_URI"] = os.getenv("MONGO_URL")
    return PyMongo(app)


mongo = configure_db(Flask(__name__))

