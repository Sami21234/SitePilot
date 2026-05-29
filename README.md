# SitePilot - A WebCrawl RAG Chatbot

A fully local, production-ready RAG chatbot that crawls any website
and answers questions about its content.
Built with 100% free and open source tools. No API costs. No data leaves your machine.

---

## What It Does

1. You provide a website URL
2. The system crawls the website and extracts all meaningful content
3. Content is chunked, embedded, and stored in a local vector database
4. You ask questions about the website in plain English
5. The chatbot retrieves relevant content and generates accurate answers using a local LLM

---

## Tech Stack

| Component | Technology |
|---|---|
| Web Crawling | Python, Requests, BeautifulSoup4 |
| Text Chunking | LangChain RecursiveCharacterTextSplitter |
| Embedding Model | all-MiniLM-L6-v2 (SentenceTransformers) |
| Vector Database | ChromaDB (local, persistent) |
| LLM | Mistral 7B via Ollama |
| Orchestration | LangChain |
| Backend API | FastAPI |
| Frontend | HTML, CSS, Vanilla JavaScript |

**Total API cost: $0**

---

## Architecture

<div align="center">

```text
User types URL
        ↓
Web Crawler (BeautifulSoup)
        ↓
Text Cleaner + Chunker (LangChain)
        ↓
Embedding Model (all-MiniLM-L6-v2)
        ↓
Vector Store (ChromaDB)
        ↓
User asks question
        ↓
Query Embedding → Similarity Search → Top-K Chunks
        ↓
Prompt Template + Retrieved Chunks
        ↓
Local LLM (Mistral 7B via Ollama)
        ↓
Answer displayed in chat UI
```

</div>

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
```

### Step 4 — Pull and start Mistral via Ollama

```bash
# Pull the model (one time, around 4GB download)
ollama pull mistral

# Start Ollama server (keep this running)
ollama serve
```

### Step 5 — Start the backend

```bash
cd backend
uvicorn main:app --reload
```

### Step 6 — Open the frontend

Open `frontend/index.html` in your browser.

---

## How to Use

1. Open the chat interface in your browser
2. Paste any website URL into the URL input field
3. Click **Crawl Website** and wait for indexing to complete
4. Type your question in the chat box
5. Receive answers grounded in the website content

---

## Project Structure

```text
SITEPILOT/
│
├── backend/
│   ├── crawler.py
│   │   └── Crawls website and extracts clean text
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
│   │   └── LangChain RAG pipeline
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

**Why all-MiniLM-L6-v2?**
Fast, lightweight, and accurate enough for most RAG use cases.
Runs fully local with no API key required.
384-dimensional embeddings with strong semantic similarity performance.

**Why ChromaDB?**
Zero infrastructure setup. Persists to disk automatically.
Native LangChain integration. Perfect for local and small-scale production use.

**Why chunk size 400 with overlap 50?**
Large enough to preserve full sentences and semantic context.
Small enough to keep embeddings focused and retrieval precise.
Overlap prevents critical information from being lost at chunk boundaries.

---

## Limitations

- JavaScript-heavy websites may not crawl completely with BeautifulSoup
- Very large websites may take several minutes to index
- Local LLM response speed depends on your hardware
- ChromaDB is not recommended for production scale above 100k documents

---

## Future Improvements

- Add Playwright support for JavaScript-rendered websites
- Add multi-website support in a single session
- Add conversation memory for follow-up questions
- Add source citation with clickable links in chat UI
- Add re-ranking layer for improved retrieval precision
- Dockerize for easy deployment

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
