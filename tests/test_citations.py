import pytest
from backend.services.citation_service import CitationService

def test_extract_citations():
    chunks = [
        {
            "source": "Scholarship_Notification_2026.pdf",
            "page": 4,
            "category": "scholarship",
            "document_date": "2026-06-01",
            "text": "The post-graduate scholarship provides financial assistance of Rs 10,000 per month.",
            "score": 0.88
        },
        {
            "source": "Scholarship_Notification_2026.pdf",
            "page": 4,  # Duplicate page test
            "category": "scholarship",
            "document_date": "2026-06-01",
            "text": "The candidate must have scored at least 60% in graduation.",
            "score": 0.85
        },
        {
            "source": "Recruitment_2026.pdf",
            "page": 10,
            "category": "recruitment",
            "document_date": "2026-01-15",
            "text": "Age limit for candidates is between 18 and 30 years as of June 1st.",
            "score": 0.92
        }
    ]

    citations = CitationService.extract_citations(chunks)
    assert len(citations) == 2  # Deduplicated by document + page
    assert citations[0].document == "Scholarship_Notification_2026.pdf"
    assert citations[0].page == 4
    assert citations[1].document == "Recruitment_2026.pdf"
    assert citations[1].page == 10
