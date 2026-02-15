import os


def chunk_text(text: str) -> list[str]:
    chunk_size = int(os.getenv("CHUNK_SIZE", "8000"))
    overlap = int(os.getenv("CHUNK_OVERLAP", "500"))

    if not text:
        return []

    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunks.append(text[start:end])
        if end == n:
            break
        start = max(0, end - overlap)
    return chunks
