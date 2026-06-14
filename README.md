# SitePilot ✈ — Chat with Any Website

A fully local, production-ready RAG chatbot that crawls any website
and answers questions about its content.
Built with 100% free and open source tools. No API costs. No data leaves your machine.

ss1

---

## What It Does

1. You provide a website URL
2. SitePilot crawls the website and extracts all meaningful content
3. Content is chunked, embedded, and stored in a local vector database
4. You ask questions about the website in plain English
5. SitePilot retrieves relevant content and generates accurate answers using a local LLM
6. Full conversation memory — follow-up questions work naturally

---

## Live Examples

### Python.org
![Python.org Demo](screenshots/python_demo.png)

### FastAPI Documentation
![FastAPI Demo](screenshots/fastapi_demo.png)

### Wikipedia
![Wikipedia Demo](screenshots/wikipedia_demo.png)

---

## Tech Stack

| Component | Technology | Cost
|---|---|
| Web Crawling | Python, Requests, BeautifulSoup4 |
| Free | JS Site Support | Playwright + Chromium |
| Text Chunking | LangChain RecursiveCharacterTextSplitter |
| Embedding Model | all-MiniLM-L6-v2 (SentenceTransformers) |
| Vector Database | ChromaDB (local, persistent) |
| LLM | Mistral 7B via Ollama |
| Orchestration | LangChain ConversationalRetrievalChain |
| Backend API | FastAPI |
| Frontend | HTML, CSS, Vanilla JavaScript |

**Total API cost: $0**

---

## Architecture

<div align="center">

```text
User provides URL
        ↓
Smart Crawler (auto-detects static vs JS site)
        ↓
BeautifulSoup (static) or Playwright (JS)
        ↓
Text Cleaner + Chunker (RecursiveCharacterTextSplitter, 400 chars, 50 overlap)
        ↓
Embedding Model (all-MiniLM-L6-v2, 384 dimensions)
        ↓
Vector Store (ChromaDB, cosine similarity, local persistent)
        ↓
User asks question
        ↓
Similarity Threshold Check (0.45 minimum)
        ↓
 if above threshold, then
        ↓
Query Embedding → MMR Search → Top-K Chunks
        ↓
Conversation Memory + Retrieved Chunks + Prompt Template
        ↓
Local LLM (Mistral 7B via Ollama)
        ↓
Answer + Source Citations displayed in chat UI
```

</div>

---

## Key Features

- **Smart Crawling** — Auto-detects JavaScript-rendered sites and
  switches to Playwright automatically. Static sites use the faster
  requests-based crawler.
- **Conversation Memory** — Uses ConversationalRetrievalChain with
  ConversationBufferMemory. Follow-up questions like "what is its
  price?" work correctly without repeating context.
- **Hallucination Prevention** — Similarity threshold filter returns
  "I don't have information about that" instantly for out-of-scope
  questions without calling the LLM at all.
- **MMR Retrieval** — Maximal Marginal Relevance retrieval returns
  diverse chunks instead of redundant similar ones.
- **Source Citations** — Every answer includes clickable links to the
  exact pages the information came from.
- **Full Privacy** — No data leaves your machine. Suitable for
  sensitive or proprietary content.

---


## Prerequisites

- Python 3.10 or higher
- Ollama installed from [ollama.ai](https://ollama.ai)
- Git
- 8GB RAM minimum (16GB recommended)
- GPU optional but recommended for faster inference

---

## Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/Sami21234/SitePilot.git
cd SitePilot
```

### Step 2 — Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac or Linux
source venv/bin/activate
```

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### Step 4 — Pull and start Mistral via Ollama

```bash
# Pull the model (one time, around 4GB download)
ollama pull mistral

# Start Ollama server (keep this running)
ollama serve
```

### Step 5 — Start the backend(SitePilot)

```bash
cd backend
python main.py
```

### Step 6 — Open the frontend

Open `frontend/index.html` in your browser.<br>
<div align="center"> OR </div><br>
Open in browser :-

http://localhost:8000/docs 


---

## How to Use

1. Enter any website URL in the input field
2. Set max pages (10 is recommended for most sites)
3. Click **Index Website** and wait for indexing (30-60 seconds)
4. Type questions in plain English
5. Follow-up questions work naturally — no need to repeat context
6. Click **Index new site** to switch to a different website

---

## Project Structure

```text
SITEPILOT/
│
├── backend/
│   ├── crawler.py
│   │   └── Crawls website with JS detection and extracts clean text
│   │
│   ├── chunker.py
│   │   └── Splits text into embeddable chunks
│   │
│   ├── embedder.py
│   │   └── Creates embeddings and stores them in ChromaDB
│   │
│   ├── retriever.py
│   │   └── Handles similarity search
│   │
│   ├── chain.py
│   │   └── ConversationalRetrievalChain RAG pipeline
│   │
│   └── main.py
│       └── FastAPI routes and application entry point
│
├── frontend/
│   ├── index.html
│   │   └── Chat interface
│   │
│   ├── style.css
│   │   └── Frontend styling
│   │
│   └── app.js
│       └── Frontend logic and API calls
│
├── chroma_db/
│   └── Persistent vector database storage
│
├── requirements.txt
│   └── Python dependencies
│
└── README.md
    └── Project documentation
```

---

## Key Design Decisions

**Why local LLM instead of GPT-4?**
Privacy and cost. No data leaves your machine. Zero per-query cost.
Suitable for sensitive domains like healthcare, legal, and finance.
Mistral 7B outperforms GPT-3.5 on many benchmarks.

**Why all-MiniLM-L6-v2?**
Fast, lightweight, and accurate for most RAG use cases.
Runs fully local, no API key required.
384-dimensional embeddings with strong semantic similarity.

**Why ChromaDB?**
Zero infrastructure setup. Persists to disk automatically.
Native LangChain integration. Singleton pattern prevents
multi-client conflicts in FastAPI.

**Why MMR over pure similarity search?**
Pure similarity returns redundant chunks from the same page section.
MMR balances relevance with diversity, giving the LLM richer context.

**Why ConversationalRetrievalChain?**
RetrievalQA is stateless — every question is independent.
ConversationalRetrievalChain maintains chat history so pronouns
like "it", "that", and "its price" resolve correctly.

**Why similarity threshold 0.45?**
Below this score, retrieved chunks are semantically unrelated to
the question. Returning the fallback response immediately is faster
and more honest than letting the LLM hallucinate from irrelevant context.


---

## Known Limitations

- JavaScript-heavy websites may return incomplete content with
  BeautifulSoup — Playwright handles this automatically for
  detected JS frameworks
- Cross-page content contamination may occur on e-commerce sites
  with "recently viewed" sections embedded in product page HTML
- Similarity threshold may reject valid follow-up questions that
  lack explicit keywords — conversation context is not used for
  threshold scoring
- Very large websites should use max_pages to limit crawl time
- Local LLM response speed depends on hardware

---

## Future Improvements

- Server-Sent Events for real-time crawl progress updates
- Re-ranking layer with cross-encoder for improved retrieval precision
- Threshold scoring using conversation context not just raw query
- Multi-website support in a single session
- Docker container for one-command deployment
- Export conversation history as PDF or markdown

---

## Author

Built by <b>MOHD. SAMI</b><br>
GitHub: [Sami2123](https://github.com/Sami21234)
LinkedIn: [mohd-sami-dev](https://linkedin.com/in/mohd-sami-dev)

---

## License

MIT License — free to use, modify, and distribute.

---

## Acknowledgements

- [LangChain](https://langchain.com) for LLM orchestration
- [Ollama](https://ollama.ai) for local LLM runtime
- [ChromaDB](https://trychroma.com) for vector storage
- [Sentence Transformers](https://sbtransformers.net) for embeddings
- [BeautifulSoup](https://crummy.com/software/BeautifulSoup) for HTML parsing
