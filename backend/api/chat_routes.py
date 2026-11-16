import json
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.schemas import ChatRequest, ChatResponse
from backend.models.database_models import ChatMessageRecord, User
from backend.services.chat_service import ChatService
from backend.utils.auth_utils import get_current_user

router = APIRouter(prefix="/api/chat", tags=["Chat"])
chat_service = ChatService()

@router.post("", response_model=ChatResponse)
def post_chat_question(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ask a question about government services, schemes, jobs, or scholarships (requires login)."""
    if not chat_request.question or not chat_request.question.strip():
        raise HTTPException(status_code=400, detail="Question string cannot be empty.")
    
    return chat_service.process_chat(chat_request, db, user_id=current_user.id)

@router.get("/history")
def get_chat_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get previous chat messages scoped strictly to the authenticated user."""
    records = db.query(ChatMessageRecord)\
        .filter(ChatMessageRecord.user_id == current_user.id)\
        .order_by(ChatMessageRecord.created_at.desc())\
        .limit(limit)\
        .all()
    history = []
    for rec in reversed(records):
        sources = json.loads(rec.sources_json) if rec.sources_json else []
        history.append({
            "id": rec.id,
            "question": rec.question,
            "answer": rec.answer,
            "sources": sources,
            "confidence": rec.confidence,
            "grounded": rec.grounded == "true",
            "created_at": rec.created_at.isoformat()
        })
    return history

@router.delete("/history")
def clear_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear chat message history strictly for the authenticated user."""
    db.query(ChatMessageRecord)\
        .filter(ChatMessageRecord.user_id == current_user.id)\
        .delete(synchronize_session=False)
    db.commit()
    return {"message": "Chat history cleared successfully."}
