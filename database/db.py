from pymongo import MongoClient
import os

MONGODB_URI = "mongodb://localhost:27017/database"
try:
    MONGODB_URI = os.environ['MONGODB_URI']
except KeyError:
    print("No MONGODB_URI environment variable found. Using default value")

# Connect to MongoDB cluster:
client = MongoClient(MONGODB_URI)
db = client['database']