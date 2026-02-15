import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from db import latest, search
from rag import answer

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="POC MF AI API")


class ChatRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/latest")
def get_latest(limit: int = 10):
    return {"items": latest(limit)}


@app.get("/search")
def get_search(q: str, limit: int = 10):
    return {"items": search(q, limit)}


@app.post("/chat")
def chat(req: ChatRequest):
    return {"answer": answer(req.question)}
