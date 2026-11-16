from typing import List, Dict, Any, Optional
from backend.config import TOP_K
from backend.rag.vector_store import VectorStore
from backend.utils.logging_config import logger

class DocumentRetriever:
    """Retriever for extracting most relevant context chunks from VectorStore."""

    def __init__(self, vector_store: Optional[VectorStore] = None):
        self.vector_store = vector_store or VectorStore()

    def retrieve(self, query: str, top_k: int = TOP_K, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve top_k matching chunks for a query."""
        logger.info(f"Retrieving top {top_k} documents for query: '{query[:60]}...'")
        matched_chunks = self.vector_store.search(query=query, top_k=top_k, category=category)
        logger.info(f"Retrieved {len(matched_chunks)} chunks.")
        return matched_chunks
