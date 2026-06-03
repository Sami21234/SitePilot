
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

def embed_and_store(chunks, collection_name = "sitepilot"):
    collection = get_chroma_collection(collection_name)   # get the collection to store the vectors.
    texts = [chunks["text"] for chunk in chunks]        # Extracts the texts
    metadatas = [       # Extracts metadata
        {
            "source": chunk["source"],
            "title": chunk["title"],
            "chunk_index": chunk["chunk_index"]
        }
        for chunk in chunks
    ]
    ids = [     # Creates IDs, so that every chunk gets unique ID.
        f"{chunk['source']}__chunk_{chunk['chunk_index']}"
        for chunk in chunks
    ]

    print(f"Embedding {len(texts)} chunks...")

    # Now, generating the embeddings
    embeddings = model.encode(      # example --> "AI is a field of study", then --> [0.212,-0.334, 0.992,...]
        texts,
        batch_size=32,      #  Encode 32 chunks at once.
        show_progress_bar=True,     # Shows progress bar while processing.
        convert_to_numpy=True       # returns numpy array.
    )

    embeddings_list = embeddings.tolist()       # converts the embeddings to the python lists, cause chroma excepts normal python lists.

    # Now, storing everything
    collection.upsert(
        documents = texts,      # Actual chunk text.
        embeddings = embeddings_list,       # vectors list.
        metadatas = metadatas,      # source information.
        ids = ids       # ids for chunks for unique indentifiers.
    )

    print(f"Stored {len(texts)} chunks in ChromaDB")
    return collection