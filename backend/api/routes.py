from fastapi import APIRouter
from backend.config import DISCLAIMER, OLLAMA_MODEL
from backend.llm.ollama_client import OllamaClient
from backend.rag.vector_store import VectorStore

router = APIRouter()

@router.get("/")
def read_root():
    return {
        "name": "SevaAI API",
        "version": "1.0.0",
        "description": "AI-Powered Government Services & Eligibility Assistant",
        "disclaimer": DISCLAIMER
    }

@router.get("/health")
def health_check():
    ollama_client = OllamaClient()
    ollama_status = ollama_client.check_health()
    
    vector_store = VectorStore()
    chunk_count = vector_store.get_total_chunks()

    return {
        "status": "healthy",
        "ollama": ollama_status,
        "indexed_chunks": chunk_count,
        "model": OLLAMA_MODEL
    }
