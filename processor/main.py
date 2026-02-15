import os
from dotenv import load_dotenv

from mongo_reader import get_raw_logs
from chunker import chunk_text
from llm_client import call_bedrock_claude
from postgres import init_schema, insert_summary

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


def build_prompt(raw: str) -> str:
    return (
        "Explain the following mainframe log in simple English. "
        "Identify likely error cause and suggest possible fix steps. "
        "Keep it concise and actionable."
        f"LOG:{raw}"
    )


def process_once(limit: int = 20):
    init_schema()
    docs = get_raw_logs(limit=limit)
    if not docs:
        print("[Processor] No raw logs found.")
        return

    for d in docs:
        mongo_id = str(d.get("_id"))
        filename = d.get("filename")
        ingested_at = d.get("ingested_at")
        content = d.get("content", "")

        # chunk (for large logs)
        chunks = chunk_text(content)
        if not chunks:
            continue

        # For POC: summarize first chunk only (or join a few)
        joined = "".join(chunks[:2])
        prompt = build_prompt(joined)

        try:
            summary = call_bedrock_claude(prompt)
            insert_summary(mongo_id, filename, ingested_at, summary)
            print(f"[Processor] Saved summary for {filename}")
        except Exception as e:
            print(f"[Processor] ERROR processing {filename}: {e}")


if __name__ == "__main__":
    process_once()
