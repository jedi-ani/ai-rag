from pymongo import MongoClient
from google import genai

from .config import (
    MONGODB_URI,
    DB_NAME,
    COLLECTION_NAME,
    VECTOR_INDEX_NAME,
    EMBEDDING_MODEL,
)

client = genai.Client()
mongo = MongoClient(MONGODB_URI)
collection = mongo[DB_NAME][COLLECTION_NAME]


def embed_query(question: str):
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[question],
    )
    return result.embeddings[0].values


def retrieve(question: str, limit: int = 6):
    query_vector = embed_query(question)

    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": limit,
            }
        },
        {
            "$project": {
                "text": 1,
                "source_name": 1,
                "page": 1,
                "chunk_index": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    return list(collection.aggregate(pipeline))