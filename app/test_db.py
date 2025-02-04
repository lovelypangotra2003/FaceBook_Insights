from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

try:
    collections = db.list_collection_names()
    print(f"Connected to MongoDB: {DATABASE_NAME}")
    print("Collections:", collections)
except Exception as e:
    print(f" MongoDB Connection Failed: {e}")
