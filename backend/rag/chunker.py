from typing import List, Dict, Any
from backend.config import CHUNK_SIZE, CHUNK_OVERLAP
from backend.utils.logging_config import logger

class DocumentChunker:
    """Sliding window document text chunker preserving page metadata and boundaries."""

    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_page(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk single page text into structural segments with overlap."""
        text = page_data.get("text", "")
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)
        chunk_idx = 0

        while start < text_length:
            end = start + self.chunk_size
            
            # If not at the end of text, attempt to find a clean break point (newline, period, or space)
            if end < text_length:
                # Look back up to 100 chars for paragraph break or sentence end
                break_point = max(
                    text.rfind('\n\n', start, end),
                    text.rfind('\n', start, end),
                    text.rfind('. ', start, end),
                    text.rfind('? ', start, end)
                )
                if break_point > start + (self.chunk_size // 2):
                    end = break_point + 1

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunk_meta = {
                    "chunk_id": f"{page_data['source']}_p{page_data['page']}_c{chunk_idx}",
                    "text": chunk_text,
                    "source": page_data["source"],
                    "page": page_data["page"],
                    "category": page_data.get("category", "general"),
                    "document_date": page_data.get("document_date", "2026-01-01"),
                }
                chunks.append(chunk_meta)
                chunk_idx += 1

            # Advance start by chunk_size - chunk_overlap
            advance = max(1, (end - start) - self.chunk_overlap)
            start += advance

        return chunks

    def chunk_documents(self, pages_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chunk a list of extracted document pages."""
        all_chunks = []
        for page_data in pages_data:
            page_chunks = self.chunk_page(page_data)
            all_chunks.extend(page_chunks)
        
        logger.info(f"Created {len(all_chunks)} chunks from {len(pages_data)} pages")
        return all_chunks
