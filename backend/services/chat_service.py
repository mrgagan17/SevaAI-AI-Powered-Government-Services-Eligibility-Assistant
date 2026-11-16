import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.models.schemas import ChatRequest, ChatResponse, SourceCitation
from backend.models.database_models import ChatMessageRecord
from backend.rag.retriever import DocumentRetriever
from backend.rag.context_builder import ContextBuilder
from backend.services.citation_service import CitationService
from backend.services.eligibility_service import EligibilityService
from backend.services.profile_service import ProfileService
from backend.llm.ollama_client import OllamaClient
from backend.config import DISCLAIMER
from backend.utils.logging_config import logger

class ChatService:
    """Core RAG pipeline coordinator for SevaAI conversational assistant."""

    def __init__(self):
        self.retriever = DocumentRetriever()
        self.ollama = OllamaClient()
        self.eligibility_service = EligibilityService(self.ollama)

    def process_chat(self, chat_request: ChatRequest, db: Session, user_id: Optional[int] = None) -> ChatResponse:
        """Process user question through complete RAG pipeline."""
        question = chat_request.question.strip()
        logger.info(f"Processing chat question: '{question}' (user_id={user_id})")

        # 1. Retrieve relevant chunks from VectorStore
        chunks = self.retriever.retrieve(query=question)
        citations = CitationService.extract_citations(chunks)

        # 2. Check Grounding & Relevance (Anti-Hallucination safeguard)
        if not chunks:
            logger.info("No matching chunks found in ChromaDB.")
            unfound_answer = (
                "I couldn't find this information in the available official documents indexed in SevaAI.\n\n"
                "Please verify the latest official notification or upload the relevant document."
            )
            # Evaluate eligibility if requested even without docs
            eligibility_res = None
            if chat_request.check_eligibility:
                profile = ProfileService.get_profile(db, user_id=user_id)
                eligibility_res = self.eligibility_service.evaluate_eligibility(
                    profile=profile, question=question, context="", chunks=[]
                )

            # Record in DB
            chat_rec = ChatMessageRecord(
                user_id=user_id,
                question=question,
                answer=unfound_answer,
                sources_json=json.dumps([]),
                confidence="low",
                grounded="false"
            )
            db.add(chat_rec)
            db.commit()

            return ChatResponse(
                answer=unfound_answer,
                sources=[],
                confidence="low",
                grounded=False,
                eligibility=eligibility_res,
                disclaimer=DISCLAIMER
            )

        # 3. Build Context
        context = ContextBuilder.build_context(chunks)

        # 4. Generate Answer via LLM
        llm_result = self.ollama.generate_grounded_answer(question=question, context=context)

        if not llm_result["success"]:
            # Fallback when LLM is unavailable or errors out
            error_msg = llm_result["error"]
            fallback_answer = (
                f"**System Notice:** {error_msg}\n\n"
                f"**Retrieved Government Document Snippet:**\n"
                f"{chunks[0]['text'][:400]}..."
            )
            return ChatResponse(
                answer=fallback_answer,
                sources=citations,
                confidence="low",
                grounded=True,
                eligibility=None,
                disclaimer=DISCLAIMER
            )

        answer_text = llm_result["answer"]

        # 5. Determine eligibility if explicitly requested or query mentions eligibility
        eligibility_res = None
        is_eligibility_query = chat_request.check_eligibility or any(
            kw in question.lower() for kw in ["eligible", "eligibility", "qualification", "age limit", "can i apply", "am i eligible"]
        )

        if is_eligibility_query:
            profile = ProfileService.get_profile(db, user_id=user_id)
            eligibility_res = self.eligibility_service.evaluate_eligibility(
                profile=profile, question=question, context=context, chunks=chunks
            )

        # 6. Save chat record in DB
        sources_payload = [c.model_dump() for c in citations]
        chat_rec = ChatMessageRecord(
            user_id=user_id,
            question=question,
            answer=answer_text,
            sources_json=json.dumps(sources_payload),
            confidence="high" if len(chunks) >= 3 else "medium",
            grounded="true"
        )
        db.add(chat_rec)
        db.commit()

        return ChatResponse(
            answer=answer_text,
            sources=citations,
            confidence="high" if len(chunks) >= 3 else "medium",
            grounded=True,
            eligibility=eligibility_res,
            disclaimer=DISCLAIMER
        )
