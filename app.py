import os

from flask import Flask, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient
from routes import auth, clerk

from middleware.auth_middleware import token_required

# setup database
load_dotenv()
# MONGODB_URI = "mongodb://localhost:27017/database"
# try:
#     MONGODB_URI = os.environ['MONGODB_URI']
# except KeyError:
#     print("No MONGODB_URI environment variable found. Using default value")
#
# # Connect to MongoDB cluster:
# client = MongoClient(MONGODB_URI)
# db = client['database']

app = Flask(__name__)

@app.route('/asd')
def hello_world():
    return 'Hello, World!'


# register blueprints and add prefix to its routes
app.register_blueprint(auth.bp, url_prefix='/')
app.register_blueprint(clerk.bp, url_prefix='/webhook/clerk')

on_dev = os.getenv('FLASK_ENV') != 'production'
if on_dev:
    print("Running on development environment")
    app.run()
else:
    print("Running on production environment")
