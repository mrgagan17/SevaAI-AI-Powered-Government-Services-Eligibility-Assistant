# SevaAI — AI-Powered Government Services & Eligibility Assistant

> **Understand Government Services. Find What Applies to You.**

SevaAI is an independent, source-grounded AI assistance platform that helps citizens understand government schemes, jobs, scholarships, notifications, benefits, required documents, application procedures, deadlines, and basic eligibility using trusted government PDF documents.

> **Disclaimer:** SevaAI is an independent AI assistance project. Information is provided for guidance and should be verified with the official government source before taking action. SevaAI is NOT an official government website and does not claim to be affiliated with or endorsed by any government authority.

---

## 🌟 Key Features

- 🧠 **Source-Grounded RAG Pipeline**: Answers are generated exclusively from indexed official PDFs using Sentence Transformers and local Vector DB (ChromaDB).
- 🚫 **Zero Hallucination Safeguard**: Explicitly refrains from inventing government rules, dates, or eligibility requirements when documents are silent.
- 📑 **Exact Page & Snippet Citations**: Every answer provides clickable source cards with document title, page number, category, and text snippets.
- 👤 **Personalized Eligibility Matching**: Evaluates citizen criteria (Age, Education, Income, Category, State, PwD status) against scheme rules, classifying matches as `MATCH`, `PARTIAL_MATCH`, `NOT_MATCHED`, or `UNKNOWN`.
- 🔐 **Citizen Authentication & Saved Profiles**: User registration & login with bcrypt password encryption and JWT sessions, isolating personal profiles and chat histories.
- ☁️ **Google Cloud Hosting Ready**: Pre-configured for single-container deployment on Google Cloud Run (`Dockerfile`, `cloudbuild.yaml`, and one-click deployment scripts).
- ⚡ **Flexible LLM Provider**: Run 100% locally with Ollama (`qwen3:4b`), or in the cloud using Google Gemini Flash (`gemini-1.5-flash`).
- 📜 **Complete Transparency**: Built-in About Us and Privacy Policy pages ensuring compliance with data minimization and citizen rights.
- 📁 **PDF Document Management**: Upload, preview, re-index, and delete official government PDFs via an intuitive web interface.
- 🛡️ **Ethical & Secure**: No CAPTCHA bypassing, scraping of protected portals, or illegal web automation.

---

## 🏗️ System Architecture

```text
                ┌───────────────────┐
                │      User         │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │  React Frontend   │
                │   (Vite + CSS)    │
                └─────────┬─────────┘
                          │ (REST API)
                          ▼
                ┌───────────────────┐
                │  FastAPI Backend  │
                └─────────┬─────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
      ┌──────────────┐          ┌──────────────┐
      │ RAG Pipeline │          │ User Profile │
      └──────┬───────┘          │   (SQLite)   │
             │                  └──────────────┘
      ┌──────▼───────┐
      │  ChromaDB    │
      └──────┬───────┘
             │
      ┌──────▼───────┐
      │   Ollama     │
      │  qwen3:4b    │
      └──────────────┘
```

### Retrieval & Generation Flow

```text
User Question
      ↓
Query Vectorization (Sentence-Transformers)
      ↓
Semantic Retrieval (ChromaDB Top-K Chunks)
      ↓
Context Construction + Profile Injection
      ↓
Local LLM Prompt (Ollama qwen3:4b)
      ↓
Grounded Answer + Citations + Eligibility Evaluation
```

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy, SQLite
- **RAG & Vector Store**: PyMuPDF (`fitz`), `sentence-transformers/all-MiniLM-L6-v2`, ChromaDB
- **Local LLM**: Ollama (`qwen3:4b`)
- **Frontend**: React 18, Vite, Lucide Icons, Vanilla CSS
- **Testing & Verification**: Pytest, FastAPI TestClient

---

## 📁 Repository Structure

```text
SevaAI/
├── backend/
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Environment configuration
│   ├── database.py              # SQLite SQLAlchemy setup
│   ├── api/                     # REST API endpoint routers
│   ├── models/                  # Database ORM models and Pydantic schemas
│   ├── rag/                     # Loader, Chunker, Embeddings, ChromaDB, Retriever
│   ├── llm/                     # Ollama client and grounding prompts
│   ├── services/                # RAG coordinator, Citations, Eligibility, Profile
│   └── utils/                   # Logging and text sanitization helpers
├── data/
│   ├── documents/               # Categorized official government PDFs
│   ├── chroma/                  # Local persistent ChromaDB vector store
│   └── sample/                  # Sample document instructions
├── frontend/
│   ├── src/                     # React components, pages, API client, and styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── tests/                       # Pytest unit and integration test suite
├── scripts/
│   ├── check_setup.py           # Environment and dependency checker
│   └── ingest_documents.py      # CLI Document ingestion script
├── .env.example                 # Example configuration
├── requirements.txt             # Python dependencies
├── start_sevaai.bat             # Windows one-click launcher
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.11+
- Node.js (v18+)
- Ollama installed ([https://ollama.com](https://ollama.com))

### 2. Install & Launch Local LLM
```bash
# Start Ollama server
ollama serve

# Pull default lightweight model
ollama pull qwen3:4b
```

### 3. Setup Python Backend
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python scripts/check_setup.py
```

### 4. Setup React Frontend
```bash
cd frontend
npm install
cd ..
```

### 5. Running SevaAI

#### Option A: One-Click Launcher (Windows)
Double-click `start_sevaai.bat` in the project root.

#### Option B: Manual Execution
**Terminal 1 (Backend):**
```bash
.venv\Scripts\activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Open your browser to:
- **Web App Interface**: `http://localhost:5173`
- **FastAPI Swagger Docs**: `http://localhost:8000/docs`

---

## 📑 Indexing Official Government Documents

1. Open the **Documents** tab in the Web App.
2. Select a category (`Scholarship`, `Recruitment`, `Welfare Scheme`, `General`) and upload an official government PDF.
3. SevaAI will extract page text, generate embeddings, and update ChromaDB automatically.
4. Alternatively, place PDFs in `data/documents/` subdirectories and run:
   ```bash
   python scripts/ingest_documents.py
   ```

---

## 🧪 Running Unit Tests

To run the automated test suite verifying PDF chunking, vector search, citations, eligibility matching, and API endpoints:

```bash
.venv\Scripts\pytest
```

---

## ⚖️ Legal & Ethical Compliance

- **No Unauthorized Automation**: SevaAI does NOT bypass CAPTCHA, authentication, WAF, or rate limits.
- **Trusted Sources Only**: Uses only user-provided or publicly permitted official PDF notifications.
- **Non-Affiliation**: Clear disclaimer presented across the application UI to prevent misleading citizens.

---

## 📄 License

MIT License. SevaAI is built for public good, citizen empowerment, and AI research.
