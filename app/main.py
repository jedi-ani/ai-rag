import time
from fastapi import FastAPI
from pydantic import BaseModel

from .ingest import ingest_pdf
from .retriever import retrieve
from .generator import generate_answer

app = FastAPI(title="ai-rag API")


class AskRequest(BaseModel):
    question: str
    temperature: float = 0.2
    top_k: int = 6


@app.post("/ingest")
def ingest(payload: dict):
    return ingest_pdf(payload["file_path"], payload["source_name"])


@app.post("/ask")
def ask(request: AskRequest):
    started = time.perf_counter()
    passages = retrieve(request.question, request.top_k)
    answer = generate_answer(
        request.question,
        passages,
        request.temperature,
    )

    return {
        "answer": answer,
        "citations": passages,
        "latency_seconds": round(time.perf_counter() - started, 3),
        "temperature": request.temperature,
    }