import os
from pymongo import MongoClient


def _db():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB", "mainframe_poc")
    return MongoClient(uri)[db_name]


def raw_collection():
    return _db()[os.getenv("RAW_COLLECTION", "raw_logs")]


def summary_collection():
    return _db()[os.getenv("SUMMARY_COLLECTION", "log_summaries")]


def get_raw_logs(limit: int = 50):
    col = raw_collection()
    return list(col.find({"status": "raw"}).sort("ingested_at", -1).limit(limit))
