<!--
# SitePilot ✈ — Chat with Any Website

A fully local, production-ready RAG chatbot that crawls any website
and answers questions about its content.
Built with 100% free and open source tools. No API costs. No data leaves your machine.

<img width="1907" height="908" alt="sitepilot_ss1" src="https://github.com/user-attachments/assets/d6254608-87e7-4dee-8b1d-214ca56a261f" />

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

<img width="1917" height="908" alt="sitepilot_ss2" src="https://github.com/user-attachments/assets/cb54062a-a48a-4eee-8005-8fc45b7e1a44" />


### FastAPI Documentation
<img width="1918" height="917" alt="sitepilot_ss4" src="https://github.com/user-attachments/assets/2da2db45-ddc8-4afd-ac62-07a54a8ee93a" />

### Wikipedia
<img width="2190" height="1742" alt="sitepilot_ss5" src="https://github.com/user-attachments/assets/6e7e9e0b-b27f-47a1-bb6c-31f32ca85cac" />

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

-->

# SitePilot ✈ — Chat with Any Website

> Turn any website into a conversational AI assistant. Ask questions in plain English, 
> get instant answers grounded in real website content.


A fully local, production-ready RAG chatbot that crawls any website
and answers questions about its content.
Built with 100% free and open source tools. No API costs. No data leaves your machine.

<img width="1907" height="908" alt="sitepilot_ss1" src="https://github.com/user-attachments/assets/d6254608-87e7-4dee-8b1d-214ca56a261f" />

---

## The Problem SitePilot Solves

### Before SitePilot

Every day, people struggle to extract information from websites:

**The Manual Reading Problem**
You land on a website with 50 pages of documentation, product 
descriptions, or support articles. You need one specific answer. 
You spend 20 minutes clicking through pages, using Ctrl+F, 
reading irrelevant sections, and still not finding what you need.

**The Customer Support Problem**
A business has all its policies, products, and FAQs documented 
on its website. But customers still flood the support team with 
questions that are already answered — because finding answers 
manually is too slow and frustrating.

**The Research Problem**
You need to understand what a company offers, what their pricing 
is, what their policies are. You visit their website, open 10 tabs, 
and spend 30 minutes piecing together information scattered across 
different pages.

**The Language Barrier Problem**
Non-native speakers struggle to skim websites quickly. Dense 
technical documentation is inaccessible to non-experts. Jargon-heavy 
content requires expertise just to navigate.

### After SitePilot

You paste a URL. SitePilot reads the entire website in under 60 
seconds. Then you just ask questions in plain English and get 
instant, accurate answers grounded in the actual website content.

No more manual searching. No more missed information. No more wasted time.

| Before SitePilot | After SitePilot |
|---|---|
| 20 minutes reading through pages | Answer in seconds |
| Ctrl+F keyword searching | Ask in plain English |
| Opening 10 browser tabs | One conversation |
| Missing information on obscure pages | Full website indexed |
| Copying and pasting into ChatGPT | Context-aware answers with sources |
| Answers from general AI knowledge | Answers grounded in real website content |
| Data sent to third-party APIs | Everything stays on your machine |

---

## What It Does

1. Paste any website URL into SitePilot
2. The system crawls the entire website automatically
3. All content is chunked, embedded, and stored in a local vector database
4. Ask questions in plain English about the website
5. Get instant answers with source citations
6. Follow-up questions work naturally — no need to repeat context

---

## Live Examples

### Landing Page
<img width="1907" height="908" alt="sitepilot_ss1" src="https://github.com/user-attachments/assets/d6254608-87e7-4dee-8b1d-214ca56a261f" />

### Python.org — Official Documentation
<img width="1917" height="908" alt="sitepilot_ss2" src="https://github.com/user-attachments/assets/cb54062a-a48a-4eee-8005-8fc45b7e1a44" />

### FastAPI Documentation
<img width="1918" height="917" alt="sitepilot_ss4" src="https://github.com/user-attachments/assets/2da2db45-ddc8-4afd-ac62-07a54a8ee93a" />

### Wikipedia — AI Article
<img width="2190" height="1742" alt="sitepilot_ss5" src="https://github.com/user-attachments/assets/6e7e9e0b-b27f-47a1-bb6c-31f32ca85cac" />

---

## Tech Stack

| Component | Local Development | Production |
|---|---|---|
| Web Crawling | BeautifulSoup4 + Requests | Same |
| JS Site Support | Playwright + Chromium | Same |
| Text Chunking | LangChain RecursiveCharacterTextSplitter | Same |
| Embedding Model | all-MiniLM-L6-v2 (SentenceTransformers) | Same |
| Vector Database | ChromaDB (local, persistent) | Same |
| LLM | Mistral 7B via Ollama | Groq LLaMA 3.1 |
| Orchestration | LangChain RetrievalQA | Same |
| Backend | FastAPI | Same |
| Frontend | HTML, CSS, Vanilla JavaScript | Same |
| Deployment | Local | Docker on Render |

**Total API cost: $0**

---

## Architecture

<div align="center">

```text
User provides URL
        ↓
Smart Crawler (auto-detects static vs JS rendered sites)
        ↓
BeautifulSoup (static) or Playwright (JS)
        ↓
Text Cleaner + Chunker (RecursiveCharacterTextSplitter, 400 chars, 50 overlap)
        ↓
Embedding Model (all-MiniLM-L6-v2, 384 dimensions, runs locally
)
        ↓
Vector Store (ChromaDB, cosine similarity, local persistent)
        ↓
User asks question
        ↓
Similarity Threshold Check (score below 0.45 -> instant fallback, no LLM call)
        ↓
 if above threshold, then
        ↓
Query Embedding → MMR Search → Top-K Chunks
        ↓
 Retrieved Chunks + Prompt Template
        ↓
Local LLM (Mistral7B locally)
        ↓
Answer + Source Citations displayed in chat UI
```

</div>

---

---

## Key Features

**Smart Crawling**
Automatically detects JavaScript-rendered sites and switches to 
Playwright. Static sites use the faster requests-based crawler. 
No manual configuration needed.

**Hallucination Prevention**
Similarity threshold filter returns a clear "I don't have 
information about that" instantly for out-of-scope questions, 
without calling the LLM at all. Faster response, honest answer.

**Source Citations**
Every answer includes clickable links to the exact pages the 
information came from. You can verify every answer instantly.

**Full Data Privacy**
In local mode, no data leaves your machine. Suitable for 
sensitive, proprietary, or confidential website content.

**MMR Retrieval**
Maximal Marginal Relevance retrieval returns diverse chunks 
instead of redundant similar ones, giving the LLM richer context.

**Dual LLM Configuration**
Mistral 7B locally via Ollama for privacy-sensitive use cases. 
Groq LLaMA 3.1 in production via free API for zero-cost deployment. 
One environment variable switches between them.

**ChromaDB Singleton Pattern**
Shared database client prevents multi-instance conflicts in 
FastAPI. Production-grade database management pattern.

---

## Prerequisites

- Python 3.10 or higher
- Ollama from [ollama.ai](https://ollama.ai) (for local LLM)
- Git
- 8GB RAM minimum
- GPU recommended (tested on RTX 3050)

---

## Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/Sami21234/SitePilot.git
cd SitePilot
```

### Step 2 — Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac or Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### Step 4 — Pull Mistral via Ollama

```bash
ollama pull mistral
```

### Step 5 — Start Ollama server

```bash
# Keep this running in a separate terminal
ollama serve
```

### Step 6 — Start SitePilot

```bash
cd backend
python main.py
```

### Step 7 — Open in browser

http://localhost:8000

---

## How to Use

1. Enter any website URL in the input field
2. Set max pages (10 is recommended for most sites)
3. Click **Index Website** and wait 30-60 seconds for indexing
4. Type your question in plain English
5. Receive answers with source citations
6. Ask follow-up questions naturally
7. Click **Index new site** to switch to a different website

---

## Project Structure

sitepilot/

│

├── backend/

│   ├── crawler.py      # Smart web crawler with JS auto-detection

│   ├── chunker.py      # Text splitting into embeddable chunks

│   ├── database.py     # Singleton ChromaDB client manager

│   ├── embedder.py     # Embedding generation and vector storage

│   ├── chain.py        # LangChain RAG pipeline

│   └── main.py         # FastAPI REST API

│

├── frontend/

│   ├── index.html      # Chat interface

│   ├── style.css       # Professional dark theme

│   └── app.js          # Frontend logic and API calls

│

├── chroma_db/          # Persistent vector storage (auto-created)

├── requirements.txt    # Python dependencies

└── README.md

---

## Key Engineering Decisions

**Why local LLM?**
Privacy and cost. No data leaves your machine. Zero per-query 
cost. Suitable for sensitive content including healthcare, legal, 
and financial data. Mistral 7B delivers strong performance for 
factual RAG retrieval tasks.

**Why ChromaDB singleton pattern?**
FastAPI handles concurrent requests. Multiple PersistentClient 
instances pointing to the same database path cause conflicts. 
One shared client managed at module level prevents this.

**Why MMR retrieval?**
Pure similarity search returns redundant chunks from the same 
section. MMR balances relevance with diversity, giving Mistral 
richer context across different parts of the website.

**Why similarity threshold 0.45?**
Out-of-scope questions score below 0.45. Short-circuiting the 
LLM call at this point is faster and more honest than generating 
a hallucinated answer from irrelevant chunks.

**Why 400 character chunks with 50 overlap?**
Preserves complete sentences and semantic context while keeping 
embeddings focused. Overlap prevents critical information at 
chunk boundaries from being lost — a lesson learned by testing 
price queries that span sentence boundaries.

---

## Known Limitations

- JavaScript-rendered navigation may limit page discovery even 
  with Playwright — some frameworks inject links dynamically 
  after the initial render completes
- Similarity threshold may reject valid follow-up questions 
  using pronouns like "it" or "that" — conversation context 
  is not factored into threshold scoring
- Very large websites should use max_pages to limit crawl time
- LLM response speed depends on hardware — RTX 3050 gives 
  acceptable performance with Mistral 7B

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
- [Sentence Transformers](https://sbert.net) for embeddings
- [BeautifulSoup](https://crummy.com/software/BeautifulSoup) 
  for HTML parsing
- [Playwright](https://playwright.dev) for JavaScript site support
