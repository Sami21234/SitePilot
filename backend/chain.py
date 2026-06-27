
# import os
# import chromadb
# from langchain_ollama import OllamaLLM     # loads a local LLM through Ollama.(here, we use mistral llm)
# from langchain_chroma import Chroma     # connects LangChain to ChromaDB.
# from langchain_huggingface import HuggingFaceEmbeddings     # loading the embedding model 
# from langchain_classic.chains import RetrievalQA        # Prebuilt RAG pipeline
# from langchain_core.prompts import PromptTemplate     # To create custom prompt template for RAG chain.
# from chromadb.config import Settings
# from database import get_client
# from langchain_huggingface import HuggingFaceEndpoint

# # Constants
# CHROMA_DIR = os.path.join(
#     os.path.dirname(__file__),
#     "..",
#     "chroma_db"
# )

# print("Chain CHROMA_DIR:", CHROMA_DIR)

# MODEL_NAME = "all-MiniLM-L6-v2"     # embedding module

# # Creating the entire RAG pipeline
# def build_rag_chain(collection_name = "sitepilot", n_results = 3, temperature = 0.1):
    
#     embeddings = HuggingFaceEmbeddings(
#         model_name = MODEL_NAME,
#         model_kwargs = {"device": "cpu"},      # This makes embedding the query vector significantly faster than CPU(requires GPU).
#         encode_kwargs = {"normalize_embeddings": True}      # Normalizes vectors. Helpful for cosine similarity.
#     )



#     vectorstore = Chroma(       # Loads vector database.
#         client=get_client(),     # uses the shared ChromaDB client instance.
#         collection_name = collection_name,
#         embedding_function = embeddings,     # generates the query embeddings
#     )

#     print("Collection count:", vectorstore._collection.count())

#     retriever = vectorstore.as_retriever(       # converts Chroma into a retriever.
#         search_type="mmr",
#         search_kwargs={"k": n_results,"fetch_k": 10}        #  retrieve top 3 chunks by default.
#     )

#     USE_HF_API = os.getenv("USE_HF_API", "false").lower() == "true"

#     if USE_HF_API:

#         llm = HuggingFaceEndpoint(
#             repo_id="HuggingFaceH4/zephyr-7b-beta",
#             huggingfacehub_api_token=os.getenv("HF_TOKEN"),
#             temperature=temperature,
#             max_new_tokens=512,
#             task="text-generation"
#         )
#     else:
#     # loading LLM
#         llm = OllamaLLM(       # It creates local AI model
#             model = "mistral",
#             temperature = temperature,      # used to control creativity(Very factual, less hallucination)
#             num_ctx = 4096      # A context window(maximum amount of information llm can process at a single time), where llm can read 4096 tokens at once.
#         )

#     # Prommpt template for RAG chain, this controls AI behaviour.
#     system_prompt = """<|system|>
# You are SitePilot, a helpful assistant that answers questions about a specific website.

# Rules you must follow:
# - Answer using ONLY the context provided below
# - If the answer is not in the context, say exactly:
#   "I don't have information about that on this website."
# - Never make up information
# - Never use your general knowledge
# - Keep answers concise and direct

# Context:
# {context}</s>
# <|user|>
# {question}</s>
# <|assistant|>"""

#     qa_prompt = PromptTemplate(
#         template=system_prompt,
#         input_variables=["context", "question"]
#     )

#     # Building RAG Chain
#     chain = RetrievalQA.from_chain_type(        # This creates complete RAG system.
#         llm = llm,      # uses Mistral
#         chain_type = "stuff",        # Stuff means: Retrieve chunks --> Concatenate them --> Send all to LLM
#         retriever = retriever,
#         return_source_documents = True,     # It returns Answers + Source Chunks for citations.(citation means reference that proves where AI got its information)
#         chain_type_kwargs = {"prompt": qa_prompt}
#     )

#     return chain        # returns completed RAG system.

# # Now, creating the ask() fucntion, to ask the questions.

# def ask(chain, question):
#     print(f"\nQuestion: {question}")        # Displays the query.
#     print("Thinking...")

#     result = chain.invoke({"query": question})      # This is where everything happens.(Question --> Embed Question --> Search Chroma --> Get Chunks --> Build Prompt --> Call Mistral --> Return Answer)

#     answer = result["result"]       # Extracts the answer
#     sources = result["source_documents"]        # Gets retrieved chunks.

#     # now, removing the duplicate pages, sources...etc.
#     unique_sources = list(set(
#         doc.metadata.get("source", "unknown")
#         for doc in sources
#     ))

#     return {
#         "answer": answer,
#         "sources": sources
#     }

# # main testing block
# if __name__ == "__main__":

#     from embedder import embed_and_store
#     from crawler import crawl_website
#     from chunker import chunk_pages

#     print("Building RAG Chain...")
#     chain = build_rag_chain()

#     test_question = [
#         "What is the price of A Light in the Attic?",
#         "Tell me about Sharp Objects book",
#         "What is the most expensive book?",
#         "Do you sell electronics?"
#     ] 

#     for question in test_question:
#         response = ask(chain, question)        # runs full RAG pipeline for each question and gets the answer + sources.
#         print(f"\nAnswer: {response['answer']}")        # shows AI generated answer.
#         print(f"Sources: {response['sources']}")        # shows the retrieved chunks(pages) that were used to generate the answer.
#         print("-" * 60)

# import os
# from langchain_ollama import OllamaLLM
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_classic.chains import RetrievalQA
# from langchain_core.prompts import PromptTemplate
# from database import get_client


# CHROMA_DIR = os.path.join(
#     os.path.dirname(__file__),
#     "..",
#     "chroma_db"
# )

# EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# def build_rag_chain(
#     collection_name: str = "sitepilot",
#     n_results: int = 3,
#     temperature: float = 0.1,
# ):
#     embeddings = HuggingFaceEmbeddings(
#         model_name=EMBEDDING_MODEL,
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True},
#     )

#     vectorstore = Chroma(
#         client=get_client(),
#         collection_name=collection_name,
#         embedding_function=embeddings,
#     )

#     retriever = vectorstore.as_retriever(
#         search_type="mmr",
#         search_kwargs={"k": n_results, "fetch_k": 10},
#     )

#     USE_HF_API = os.getenv("USE_HF_API", "false").lower() == "true"

#     if USE_HF_API:
#         from langchain_groq import ChatGroq
#         llm = ChatGroq(
#             model="llama-3.1-8b-instant",
#             api_key=os.getenv("GROQ_API_KEY"),
#             temperature=temperature,
#             max_tokens=512
#         )
#     else:
#         llm = OllamaLLM(
#             model="mistral",
#             temperature=temperature,
#             num_ctx=4096,
#         )

#     prompt = PromptTemplate(
#         template="""You are SitePilot, a helpful assistant that answers \
# questions using ONLY the provided context.

# Rules:
# - Use only the context below to answer
# - If the answer is not in the context, say exactly:
#   "I don't have information about that on this website."
# - Do not make up information
# - Be concise and direct

# Context:
# {context}

# Question:
# {question}

# Answer:""",
#         input_variables=["context", "question"],
#     )

#     chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True,
#         chain_type_kwargs={"prompt": prompt},
#     )

#     return chain


# _chain = None


# def get_answer(question: str) -> str:
#     global _chain
#     if _chain is None:
#         _chain = build_rag_chain()
#     result = _chain.invoke({"query": question})

#     answer =  result["result"]
#     sources = list(set(
#         doc.metadata.get("source", "unknown")
#         for doc in result["source_documents"]
#         if doc.metadata.get("source")
#     ))



# if __name__ == "__main__":
#     test_questions = [
#         "Tell me about Sharp Objects",
#         "What is the most expensive book?",
#         "Do you sell electronics?",
#     ]
#     for q in test_questions:
#         print("\nQ:", q)
#         print("A:", get_answer(q))
#         print("-" * 50)

import os
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from database import get_client

CHROMA_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "chroma_db"
)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def build_rag_chain(
    collection_name: str = "sitepilot",
    n_results: int = 3,
    temperature: float = 0.1,
):
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vectorstore = Chroma(
        client=get_client(),
        collection_name=collection_name,
        embedding_function=embeddings,
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": n_results, "fetch_k": 10},
    )

    llm = OllamaLLM(
        model="mistral",
        temperature=temperature,
        num_ctx=4096,
    )

    prompt = PromptTemplate(
        template="""You are SitePilot, a helpful assistant that answers \
questions using ONLY the provided context.

Rules:
- Use only the context below to answer
- If the answer is not in the context, say exactly:
  "I don't have information about that on this website."
- Do not make up information
- Be concise and direct

Context:
{context}

Question:
{question}

Answer:""",
        input_variables=["context", "question"],
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )

    return chain


_chain = None


def get_answer(question: str):
    global _chain
    if _chain is None:
        _chain = build_rag_chain()

    result = _chain.invoke({"query": question})

    answer = result["result"]
    sources = list(set(
        doc.metadata.get("source", "")
        for doc in result["source_documents"]
        if doc.metadata.get("source")
    ))

    return answer, sources


if __name__ == "__main__":
    test_questions = [
        "Tell me about Sharp Objects",
        "What is the most expensive book?",
        "Do you sell electronics?",
    ]
    for q in test_questions:
        print("\nQ:", q)
        answer, sources = get_answer(q)
        print("A:", answer)
        print("Sources:", sources)
        print("-" * 50)