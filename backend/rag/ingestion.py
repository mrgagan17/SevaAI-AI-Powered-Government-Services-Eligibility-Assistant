import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from backend.config import DOCUMENTS_DIR
from backend.rag.document_loader import DocumentLoader
from backend.rag.chunker import DocumentChunker
from backend.rag.vector_store import VectorStore
from backend.models.database_models import DocumentRecord
from backend.utils.logging_config import logger

class DocumentIngestionManager:
    """Orchestrates PDF ingestion pipeline: Load -> Chunk -> Embed -> VectorStore & SQLite."""

    def __init__(self, vector_store: VectorStore = None):
        self.vector_store = vector_store or VectorStore()
        self.loader = DocumentLoader()
        self.chunker = DocumentChunker()

    def process_file(self, filepath: str, category: str, db: Session) -> Tuple[bool, int, int]:
        """Process a single PDF file and store vectors and database records."""
        path = Path(filepath)
        filename = path.name

        try:
            logger.info(f"Starting ingestion pipeline for '{filename}'...")

            # 1. Load PDF pages
            pages_data = self.loader.load_pdf(str(path), category=category)
            if not pages_data:
                logger.warning(f"No text extracted from '{filename}'.")
                return False, 0, 0

            # 2. Chunk pages
            chunks = self.chunker.chunk_documents(pages_data)
            if not chunks:
                logger.warning(f"No chunks produced for '{filename}'.")
                return False, len(pages_data), 0

            # 3. Clean up existing chunks in VectorStore if re-indexing
            self.vector_store.delete_document(filename)

            # 4. Add chunks to ChromaDB
            added_count = self.vector_store.add_documents(chunks)

            # 5. Sync with SQLite DB
            existing_rec = db.query(DocumentRecord).filter(DocumentRecord.filename == filename).first()
            if existing_rec:
                existing_rec.category = category
                existing_rec.page_count = len(pages_data)
                existing_rec.chunk_count = added_count
                existing_rec.status = "indexed"
            else:
                doc_rec = DocumentRecord(
                    filename=filename,
                    filepath=str(path),
                    category=category,
                    page_count=len(pages_data),
                    chunk_count=added_count,
                    status="indexed"
                )
                db.add(doc_rec)
            db.commit()

            logger.info(f"Ingestion complete for '{filename}': {len(pages_data)} pages, {added_count} chunks.")
            return True, len(pages_data), added_count

        except Exception as e:
            logger.error(f"Error ingesting file '{filename}': {str(e)}")
            db.rollback()
            return False, 0, 0

    def ingest_directory(self, docs_dir: Path, db: Session) -> Dict[str, Any]:
        """Scan and ingest all PDFs under data/documents/ subdirectories."""
        results = {
            "scanned_files": 0,
            "successful": 0,
            "failed": 0,
            "total_pages": 0,
            "total_chunks": 0,
            "details": []
        }

        if not docs_dir.exists():
            logger.warning(f"Documents directory does not exist: {docs_dir}")
            return results

        categories = ["recruitment", "scholarships", "schemes", "notifications", "general"]
        
        pdf_files = []
        for cat in categories:
            cat_dir = docs_dir / cat
            if cat_dir.exists():
                for f in cat_dir.glob("*.pdf"):
                    pdf_files.append((f, cat))
        
        # Also check root docs_dir for PDFs
        for f in docs_dir.glob("*.pdf"):
            pdf_files.append((f, "general"))

        results["scanned_files"] = len(pdf_files)
        logger.info(f"Found {len(pdf_files)} PDF files to process in {docs_dir}")

        for filepath, cat in pdf_files:
            success, pages, chunks = self.process_file(str(filepath), cat, db)
            if success:
                results["successful"] += 1
                results["total_pages"] += pages
                results["total_chunks"] += chunks
                results["details"].append({"filename": filepath.name, "status": "success", "pages": pages, "chunks": chunks})
            else:
                results["failed"] += 1
                results["details"].append({"filename": filepath.name, "status": "failed", "pages": 0, "chunks": 0})

        return results
