import os
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.config import DOCUMENTS_DIR, MAX_UPLOAD_SIZE_MB, ALLOWED_EXTENSIONS
from backend.models.database_models import DocumentRecord, User
from backend.models.schemas import DocumentResponse
from backend.rag.ingestion import DocumentIngestionManager
from backend.rag.vector_store import VectorStore
from backend.utils.text_utils import sanitize_filename
from backend.utils.auth_utils import get_current_user
from backend.utils.logging_config import logger

router = APIRouter(prefix="/api/documents", tags=["Documents"])
ingestion_manager = DocumentIngestionManager()

@router.get("", response_model=List[DocumentResponse])
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all indexed/uploaded government documents (requires login)."""
    records = db.query(DocumentRecord).order_by(DocumentRecord.upload_date.desc()).all()
    formatted = []
    for rec in records:
        formatted.append(DocumentResponse(
            id=rec.id,
            filename=rec.filename,
            category=rec.category or "general",
            upload_date=rec.upload_date.strftime("%Y-%m-%d %H:%M:%S"),
            document_date=rec.document_date or "2026-01-01",
            page_count=rec.page_count or 0,
            chunk_count=rec.chunk_count or 0,
            status=rec.status or "indexed"
        ))
    return formatted

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("general"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload an official government PDF document and automatically index it into SevaAI RAG pipeline (requires login)."""
    # 1. Validate file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Only PDF files (.pdf) are supported. Got '{ext}'")

    # 2. Read content & check size limit
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File size ({size_mb:.1f} MB) exceeds maximum allowed size ({MAX_UPLOAD_SIZE_MB} MB)."
        )

    # 3. Sanitize filename & save
    safe_name = sanitize_filename(file.filename)
    target_category = category.lower().strip()
    if target_category not in ["recruitment", "scholarships", "schemes", "notifications"]:
        target_category = "general"

    category_dir = DOCUMENTS_DIR / target_category
    os.makedirs(category_dir, exist_ok=True)
    target_path = category_dir / safe_name

    with open(target_path, "wb") as f:
        f.write(content)

    logger.info(f"User '{current_user.email}' uploaded file to '{target_path}' ({size_mb:.2f} MB)")

    # 4. Ingest and index document
    success, pages, chunks = ingestion_manager.process_file(str(target_path), target_category, db)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to process and index PDF text. Please check if PDF is valid.")

    return {
        "message": f"Successfully uploaded and indexed '{safe_name}'.",
        "filename": safe_name,
        "category": target_category,
        "pages": pages,
        "chunks": chunks
    }

@router.post("/{doc_id}/reindex")
def reindex_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Re-index an existing document in ChromaDB (requires login)."""
    doc_rec = db.query(DocumentRecord).filter(DocumentRecord.id == doc_id).first()
    if not doc_rec:
        raise HTTPException(status_code=404, detail="Document record not found.")

    if not os.path.exists(doc_rec.filepath):
        raise HTTPException(status_code=404, detail=f"Physical file missing at: {doc_rec.filepath}")

    success, pages, chunks = ingestion_manager.process_file(doc_rec.filepath, doc_rec.category, db)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to re-index document.")

    return {"message": f"Document '{doc_rec.filename}' re-indexed successfully.", "pages": pages, "chunks": chunks}

@router.delete("/{doc_id}")
def delete_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete document from database, ChromaDB vector store, and filesystem (requires login)."""
    doc_rec = db.query(DocumentRecord).filter(DocumentRecord.id == doc_id).first()
    if not doc_rec:
        raise HTTPException(status_code=404, detail="Document record not found.")

    filename = doc_rec.filename
    filepath = doc_rec.filepath

    # 1. Delete from ChromaDB
    vector_store = VectorStore()
    vector_store.delete_document(filename)

    # 2. Delete file if exists
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            logger.warning(f"Could not remove physical file '{filepath}': {str(e)}")

    # 3. Delete DB record
    db.delete(doc_rec)
    db.commit()

    return {"message": f"Document '{filename}' deleted successfully."}
