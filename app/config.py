import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.environ["MONGODB_URI"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
DB_NAME = "ai_rag"
COLLECTION_NAME = "chunks"
VECTOR_INDEX_NAME = "chunk_vector_index"
EMBEDDING_MODEL = "gemini-embedding-001"
ANSWER_MODEL = "gemini-2.5-flash"