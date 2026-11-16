import os
from pathlib import Path
from typing import List, Dict, Any
import fitz  # PyMuPDF
from backend.utils.logging_config import logger
from backend.utils.text_utils import clean_text

class DocumentLoader:
    """PDF document text and metadata extractor using PyMuPDF."""

    @staticmethod
    def load_pdf(filepath: str, category: str = "general") -> List[Dict[str, Any]]:
        """
        Extract text from PDF preserving page boundaries and metadata.
        Returns a list of dicts: [{'text': str, 'page': int, 'source': str, 'category': str}]
        """
        path = Path(filepath)
        if not path.exists():
            logger.error(f"File not found: {filepath}")
            raise FileNotFoundError(f"PDF file does not exist: {filepath}")

        pages_data = []
        filename = path.name

        try:
            doc = fitz.open(filepath)
            total_pages = len(doc)
            logger.info(f"Extracting text from '{filename}' ({total_pages} pages)")

            for page_idx in range(total_pages):
                page = doc.load_page(page_idx)
                raw_text = page.get_text("text")
                cleaned = clean_text(raw_text)

                if cleaned:
                    pages_data.append({
                        "text": cleaned,
                        "page": page_idx + 1,  # 1-indexed page numbering
                        "source": filename,
                        "filepath": str(path),
                        "category": category,
                        "total_pages": total_pages,
                        "document_date": "2026-01-01"
                    })

            doc.close()
            logger.info(f"Extracted {len(pages_data)} non-empty pages from '{filename}'")
            return pages_data

        except Exception as e:
            logger.error(f"Error loading PDF '{filepath}': {str(e)}")
            raise RuntimeError(f"Failed to process PDF file: {str(e)}")
