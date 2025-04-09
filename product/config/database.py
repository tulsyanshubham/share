import os
from pymongo import MongoClient

# MONGO_URI=mongodb://localhost:27017/
# MONGO_DB_NAME=migration_db
# MONGO_COLLECTION_NAME=repo_migrations

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
mongo_db_name = os.environ.get("MONGO_DB_NAME", "migration_db")
mongo_collection_name = os.environ.get("MONGO_COLLECTION_NAME", "repo_migrations")

def get_collection():
    client = MongoClient(mongo_uri)
    db = client[mongo_db_name]
    return db[mongo_collection_name]