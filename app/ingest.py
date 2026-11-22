import uuid
from pypdf import PdfReader
from pymongo import MongoClient
from google import genai

from .config import MONGODB_URI, DB_NAME, COLLECTION_NAME, EMBEDDING_MODEL

client = genai.Client()
mongo = MongoClient(MONGODB_URI)
collection = mongo[DB_NAME][COLLECTION_NAME]


def chunk_text(text: str, size: int = 900, overlap: int = 150):
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += size - overlap

    return chunks


def embed_texts(texts: list[str]):
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
    )
    return [item.values for item in result.embeddings]


def ingest_pdf(path: str, source_name: str):
    reader = PdfReader(path)
    full_text = "\n".join(page.extract_text() or "" for page in reader.pages)

    chunks = chunk_text(full_text)
    vectors = embed_texts(chunks)
    doc_id = str(uuid.uuid4())

    records = [
        {
            "doc_id": doc_id,
            "source_name": source_name,
            "page": index // 2 + 1,
            "chunk_index": index,
            "text": chunk,
            "embedding": vector,
        }
        for index, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]

    collection.insert_many(records)
    return {"doc_id": doc_id, "chunks": len(records)}