import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# JWT & Authentication Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "sevaai-secure-jwt-secret-key-change-in-production-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(60 * 24 * 7)))  # 7 days

# LLM Provider Configuration ("ollama" or "gemini")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Ollama LLM Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")

# Embedding Model Configuration
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Vector DB Configuration
CHROMA_PATH = os.path.abspath(os.getenv("CHROMA_PATH", str(BASE_DIR / "data" / "chroma")))
CHROMA_COLLECTION_NAME = "sevaai_documents"

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/sevaai.db")

# Document Upload & Processing Config
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))
ALLOWED_EXTENSIONS = {".pdf"}

# RAG Settings
TOP_K = int(os.getenv("TOP_K", "5"))
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Static Web Hosting (Production build from frontend/dist)
SERVE_STATIC = os.getenv("SERVE_STATIC", "true").lower() in ("true", "1", "yes")
STATIC_DIR = BASE_DIR / "frontend" / "dist"

# Application Disclaimer
DISCLAIMER = (
    "SevaAI is an independent AI assistance project. "
    "Information is provided for guidance and should be verified with the "
    "official government source before taking action."
)

# Ensure data directories exist
os.makedirs(CHROMA_PATH, exist_ok=True)
os.makedirs(DOCUMENTS_DIR / "recruitment", exist_ok=True)
os.makedirs(DOCUMENTS_DIR / "scholarships", exist_ok=True)
os.makedirs(DOCUMENTS_DIR / "schemes", exist_ok=True)
os.makedirs(DOCUMENTS_DIR / "notifications", exist_ok=True)
