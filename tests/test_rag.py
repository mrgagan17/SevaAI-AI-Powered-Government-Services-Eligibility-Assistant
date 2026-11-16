import pytest
from backend.rag.chunker import DocumentChunker
from backend.rag.context_builder import ContextBuilder

def test_chunker_basic():
    chunker = DocumentChunker(chunk_size=100, chunk_overlap=20)
    page_data = {
        "text": "First section about government schemes for citizens. Second section about eligibility and deadlines.",
        "page": 1,
        "source": "test_doc.pdf",
        "category": "scheme",
        "document_date": "2026-01-01"
    }

    chunks = chunker.chunk_page(page_data)
    assert len(chunks) >= 1
    assert chunks[0]["source"] == "test_doc.pdf"
    assert chunks[0]["page"] == 1

def test_context_builder():
    chunks = [
        {"source": "doc1.pdf", "page": 1, "category": "scheme", "text": "Content of doc1 page 1"},
        {"source": "doc2.pdf", "page": 3, "category": "job", "text": "Content of doc2 page 3"}
    ]
    context = ContextBuilder.build_context(chunks)
    assert "--- SOURCE 1 ---" in context
    assert "Document: doc1.pdf" in context
    assert "Content of doc2 page 3" in context
