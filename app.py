import os

from flask import Flask, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient

from middleware.auth_middleware import token_required

# setup database
load_dotenv()
MONGODB_URI = "mongodb://localhost:27017/database"
try:
    MONGODB_URI = os.environ['MONGODB_URI']
except KeyError:
    print("No MONGODB_URI environment variable found. Using default value")

# Connect to MongoDB cluster:
client = MongoClient(MONGODB_URI)
db = client['database']


def create_app():
    """
    Create app
    add blueprints here to register them as routes
    :return: app
    """
    app = Flask(__name__)

    from routes import auth

    # register blueprints and add prefix to its routes
    app.register_blueprint(auth.bp, url_prefix='/')

    return app


if __name__ == '__main__':
    create_app().run()
