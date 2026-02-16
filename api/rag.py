import os
from store import search
from bedrock import call_bedrock


def build_context(question: str) -> str:
    top_k = int(os.getenv("TOP_K", "4"))
    rows = search(question, limit=top_k)
    if not rows:
        return ""

    parts = []
    for r in rows:
        parts.append(
            f"FILENAME: {r.get('filename')}"
            f"SUMMARY: {r.get('summary')}"
            "---"
        )
    return "".join(parts)


def answer(question: str) -> str:
    system = (
        "You are a mainframe log assistant. Use the provided context to answer accurately. "
        "If context is insufficient, say what is missing and suggest what to check next."
    )
    context = build_context(question)
    prompt = (
        f"SYSTEM:{system}CONTEXT:{context}QUESTION:{question}"
        if context else
        f"SYSTEM:{system}QUESTION:{question}"
    )
    return call_bedrock(prompt)
