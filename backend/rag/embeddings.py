from typing import List
from sentence_transformers import SentenceTransformer
from backend.config import EMBEDDING_MODEL_NAME
from backend.utils.logging_config import logger

class EmbeddingManager:
    """Singleton embedding manager utilizing local sentence-transformers model."""
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingManager, cls).__new__(cls)
            try:
                logger.info(f"Loading local embedding model: '{EMBEDDING_MODEL_NAME}'...")
                cls._model = SentenceTransformer(EMBEDDING_MODEL_NAME)
                logger.info("Local embedding model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load embedding model '{EMBEDDING_MODEL_NAME}': {str(e)}")
                cls._model = None
        return cls._instance

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding vector for a single string."""
        if not self._model:
            raise RuntimeError("Embedding model is not initialized.")
        return self._model.encode(text, convert_to_numpy=True).tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embedding vectors for a list of document strings."""
        if not self._model:
            raise RuntimeError("Embedding model is not initialized.")
        embeddings = self._model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding vector for search query."""
        return self.embed_text(query)

# Global helper instance getter
def get_embedding_manager() -> EmbeddingManager:
    return EmbeddingManager()
