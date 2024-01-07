from pymongo import MongoClient
from mongoengine import connect
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/database')


def initialize_db():
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    connect(host=MONGODB_URI)
    return db
