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
git clone https://github.com/yourusername/webcrawl-rag-chatbot.git
cd webcrawl-rag-chatbot
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