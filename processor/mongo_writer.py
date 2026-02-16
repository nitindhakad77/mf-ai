from datetime import datetime, timezone

from mongo_reader import summary_collection


def upsert_summary(raw_log_id, filename: str, summary: str, content_hash: str | None = None):
    col = summary_collection()
    # Use content_hash if present to avoid duplicates; else use raw_log_id
    key = {"content_hash": content_hash} if content_hash else {"raw_log_id": raw_log_id}

    col.update_one(
        key,
        {"$set": {
            "raw_log_id": raw_log_id,
            "filename": filename,
            "summary": summary,
            "created_at": datetime.now(timezone.utc),
            **({"content_hash": content_hash} if content_hash else {})
        }},
        upsert=True
    )
