
import os
from langchain_community.llms import Ollama     # loads a local LLM through Ollama.(here, we use mistral llm)
from langchain_community.vectorstores import Chroma     # connects LangChain to ChromaDB.
from langchain_community.embeddings import HuggingFaceBgeEmbeddings     # loading the embedding model 
from langchain.chains import RetrievalQA        # Prebuilt RAG pipeline
from chromadb.config import Settings

# Constants
CHROMA_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "chroma_db"
)

MODEL_NAME = "all-MiniLM-L6-v2"     # embedding module

# Creating the entire RAG pipeline
def build_rag_chain(collection_name = "sitepilot", n_results = 3, temperature = 0.1):
    embeddings = HuggingFaceBgeEmbeddings(
        model_name = MODEL_NAME,
        model_kwargs = {"device": "cuda"},      # This makes embedding the query vector significantly faster than CPU(requires GPU).
        encode_kwargs = {"normalize_embeddings": True}      # Normalizes vectors. Helpful for cosine similarity.
    )

    vectorstore = Chroma(       # Loads vector database.
        collection_name = collection_name,
        embedding_function = embeddings,     # generates the query embeddings
        persist_directory  = CHROMA_DIR,     # Database location
        client_settings = Settings(
            anonymized_telemetry=False
        )
    )

    retriever = vectorstore.as_retriever(       # converts Chroma into a retriever.
        search_type = "similarity",     # searches nearest vectors.
        search_kwargs = {"k": n_results}        #  retrieve top 3 chunks by default.
    )

    # loading LLM

    llm = Ollama(       # It creates local AI model
        model = "mistral",
        temperature = temperature,      # used to control creativity(Very factual, less hallucination)
        num_ctx = 4096      # A context window, where llm can read 4096 tokens at once.
    )