from typing import List, Dict, Any
from backend.models.schemas import SourceCitation

class CitationService:
    """Extracts, formats, and deduplicates source citations from retrieved vector chunks."""

    @staticmethod
    def extract_citations(chunks: List[Dict[str, Any]]) -> List[SourceCitation]:
        """Convert retrieved chunks into structured SourceCitation objects."""
        citations = []
        seen = set()

        for chunk in chunks:
            doc = chunk.get("source", "Unknown Document")
            page = int(chunk.get("page", 1))
            cat = chunk.get("category", "general")
            doc_date = chunk.get("document_date", "2026-01-01")
            text = chunk.get("text", "").strip()
            score = chunk.get("score", 0.0)

            # Deduplicate by document + page
            key = (doc, page)
            if key not in seen:
                seen.add(key)
                # Create a concise snippet preview (max 200 chars)
                snippet = text[:200] + "..." if len(text) > 200 else text
                citations.append(SourceCitation(
                    document=doc,
                    page=page,
                    category=cat,
                    document_date=doc_date,
                    snippet=snippet,
                    score=score
                ))

        return citations
