import os
import chromadb
from chromadb.config import Settings

CHROMA_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "chroma_db"
)

# Single shared client instance for entire application
_client = None

def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=CHROMA_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
    return _client

def get_collection(name="sitepilot"):
    client = get_client()
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )