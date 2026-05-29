# test_chroma.py
import chromadb

client = chromadb.Client()
collection = client.create_collection("test")
collection.add(
    documents=["This is a test document"],
    ids=["1"]
)
results = collection.query(query_texts=["test"], n_results=1)
print("ChromaDB working:", results)