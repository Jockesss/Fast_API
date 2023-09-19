import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()


def connect_mongo() -> Database:
    mongo_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    return db
