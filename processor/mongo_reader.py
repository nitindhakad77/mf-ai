import os
from pymongo import MongoClient


def get_raw_logs(limit: int = 50):
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB", "mainframe_poc")
    col_name = os.getenv("MONGO_COLLECTION", "raw_logs")
    client = MongoClient(uri)
    col = client[db_name][col_name]
    # newest first
    return list(col.find({"status": "raw"}).sort("ingested_at", -1).limit(limit))
