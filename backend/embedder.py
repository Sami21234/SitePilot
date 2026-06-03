
import chroma_db
from chromadb.config import Settings        # Configuration settings for ChromaDB.
from sentence_transformers import SentenceTransformer       # loads embedding model.(example--> "What is AI?" into: [0.12, -0.55, 0.88, ...])
import os       # used for file paths.

MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "chroma-db"
)

'''
It creates a path:

    project/
    │
    ├── backend/
    │    embedder.py
    │
    └── chroma_db/
This is where vectors are stored.
'''

model = SentenceTransformer(MODEL_NAME)     # Loads model into memory.

# Now, Creating or loading chroma_collection. (Database --> Table(collection))

def get_chroma_collection(collection_name="sitepilot"):
    client = chromadb.PersistentClient(     # PersistentClient means Data(vectors) are saved to the disk at CHROMA_DIR. even after restarting it persists
        path = CHROMA_DIR,      # store database on disk.
        settings = Settings(anonymized_telemetry=False)     # anonymized_telemetry=False stops ChromaDB from sending usage statistics to their servers. On a privacy-focused project this matters.
    )

    collection = client.get_or_create_collection(
        name = collection_name,
        metadata = {"hnsw:space": "cosine"}     # hnsw:space: cosine metadata tells ChromaDB to use cosine similarity for distance calculations. HNSW stands for Hierarchical Navigable Small World, it is the algorithm that makes vector search fast at scale.
    )
    return collection
    '''
            Either: load existing collection
            or
            Create new collection
    '''

# Now, creating the main storage funciton.

