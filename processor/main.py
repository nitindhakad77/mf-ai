import os
from dotenv import load_dotenv

from mongo_reader import get_raw_logs
from chunker import chunk_text
from llm_client import call_bedrock_claude
from mongo_writer import upsert_summary

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


def build_prompt(raw: str) -> str:
    return (
        "Explain the following mainframe log in simple English. "
        "Identify likely error cause and suggest possible fix steps. "
        "Keep it concise and actionable."
        f"LOG:{raw}"
    )


def process_once(limit: int = 20):
    docs = get_raw_logs(limit=limit)
    if not docs:
        print("[Processor] No raw logs found.")
        return

    for d in docs:
        raw_id = d.get("_id")
        filename = d.get("filename")
        content = d.get("content", "")
        content_hash = d.get("content_hash")

        chunks = chunk_text(content)
        if not chunks:
            continue

        joined = "".join(chunks[:2])
        prompt = build_prompt(joined)

        try:
            summary = call_bedrock_claude(prompt)
            upsert_summary(raw_id, filename, summary, content_hash=content_hash)
            print(f"[Processor] Saved summary for {filename}")
        except Exception as e:
            print(f"[Processor] ERROR processing {filename}: {e}")


if __name__ == "__main__":
    process_once()
