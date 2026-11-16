import pytest
from backend.rag.vector_store import VectorStore
from backend.rag.retriever import DocumentRetriever

def test_vector_store_and_retrieval():
    vs = VectorStore()
    
    # Add dummy chunks
    chunks = [
        {
            "chunk_id": "test_doc_p1_c0",
            "text": "The government announces post-matric scholarship for minority students.",
            "source": "test_scholarship.pdf",
            "page": 1,
            "category": "scholarships",
            "document_date": "2026-01-01"
        }
    ]
    
    added = vs.add_documents(chunks)
    assert added == 1

    retriever = DocumentRetriever(vector_store=vs)
    results = retriever.retrieve("scholarship for minority students", top_k=1)
    
    assert len(results) >= 1
    assert "scholarship" in results[0]["text"].lower()

    # Clean up test doc
    vs.delete_document("test_scholarship.pdf")
