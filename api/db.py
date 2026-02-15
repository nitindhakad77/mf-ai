import os
import psycopg2
from psycopg2.extras import RealDictCursor


def conn():
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", "5432")),
        dbname=os.getenv("PG_DB", "pocdb"),
        user=os.getenv("PG_USER", "poc"),
        password=os.getenv("PG_PASSWORD", "poc"),
    )


def latest(limit: int = 10):
    with conn() as c:
        with c.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM log_summaries ORDER BY created_at DESC LIMIT %s", (limit,))
            return cur.fetchall()


def search(q: str, limit: int = 10):
    like = f"%{q}%"
    with conn() as c:
        with c.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM log_summaries WHERE summary ILIKE %s OR filename ILIKE %s ORDER BY created_at DESC LIMIT %s",
                (like, like, limit),
            )
            return cur.fetchall()
