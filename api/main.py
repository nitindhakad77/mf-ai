import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from store import latest, search
from rag import answer

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="POC MF AI API (MongoDB Only)")

origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173")
origins = [o.strip() for o in origins_env.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
