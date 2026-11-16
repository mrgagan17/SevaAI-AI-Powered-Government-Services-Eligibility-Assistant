import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from backend.config import CHROMA_PATH, CHROMA_COLLECTION_NAME
from backend.rag.embeddings import get_embedding_manager
from backend.utils.logging_config import logger

class VectorStore:
    """ChromaDB local vector store wrapper for SevaAI document chunks."""

    def __init__(self, chroma_path: str = CHROMA_PATH, collection_name: str = CHROMA_COLLECTION_NAME):
        self.chroma_path = chroma_path
        self.collection_name = collection_name
        self.embedding_manager = get_embedding_manager()

        try:
            logger.info(f"Initializing ChromaDB persistent client at: {self.chroma_path}")
            self.client = chromadb.PersistentClient(path=self.chroma_path)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "SevaAI Government Document Chunks"}
            )
            logger.info(f"ChromaDB collection '{self.collection_name}' ready. Count: {self.collection.count()}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {str(e)}")
            raise RuntimeError(f"ChromaDB initialization failed: {str(e)}")

    def add_documents(self, chunks: List[Dict[str, Any]]) -> int:
        """Add text chunks and metadata to ChromaDB collection."""
        if not chunks:
            return 0

        ids = [chunk["chunk_id"] for chunk in chunks]
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [
            {
                "source": chunk["source"],
                "page": chunk["page"],
                "category": chunk.get("category", "general"),
                "document_date": chunk.get("document_date", "2026-01-01"),
            }
            for chunk in chunks
        ]

        logger.info(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.embedding_manager.embed_documents(texts)

        # Upsert into ChromaDB
        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

        logger.info(f"Successfully added/updated {len(chunks)} chunks in ChromaDB.")
        return len(chunks)

    def search(self, query: str, top_k: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Perform semantic similarity search on stored documents."""
        if self.collection.count() == 0:
            logger.warning("Search attempted on empty ChromaDB collection.")
            return []

        query_embedding = self.embedding_manager.embed_query(query)
        where_clause = {"category": category} if category else None

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count()),
            where=where_clause,
            include=["documents", "metadatas", "distances"]
        )

        matched_chunks = []
        if results and results.get("documents") and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0]

            for doc, meta, dist in zip(docs, metas, dists):
                # Convert L2 distance / cosine distance to similarity score
                similarity = max(0.0, 1.0 - (dist / 2.0))
                matched_chunks.append({
                    "text": doc,
                    "source": meta.get("source", "Unknown Document"),
                    "page": int(meta.get("page", 1)),
                    "category": meta.get("category", "general"),
                    "document_date": meta.get("document_date", "2026-01-01"),
                    "score": round(similarity, 4)
                })

        return matched_chunks

    def delete_document(self, filename: str) -> int:
        """Delete all chunks belonging to a specific document source."""
        try:
            # Get matching IDs
            existing = self.collection.get(where={"source": filename})
            if existing and existing.get("ids"):
                ids_to_delete = existing["ids"]
                self.collection.delete(ids=ids_to_delete)
                logger.info(f"Deleted {len(ids_to_delete)} chunks for source document '{filename}'")
                return len(ids_to_delete)
            return 0
        except Exception as e:
            logger.error(f"Error deleting document '{filename}' from ChromaDB: {str(e)}")
            return 0

    def list_documents(self) -> List[str]:
        """List unique source document names present in ChromaDB."""
        try:
            all_records = self.collection.get(include=["metadatas"])
            sources = set()
            if all_records and all_records.get("metadatas"):
                for meta in all_records["metadatas"]:
                    if meta and "source" in meta:
                        sources.add(meta["source"])
            return sorted(list(sources))
        except Exception as e:
            logger.error(f"Error listing documents in ChromaDB: {str(e)}")
            return []

    def get_total_chunks(self) -> int:
        return self.collection.count()
