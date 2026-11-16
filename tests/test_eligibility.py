import pytest
from backend.models.database_models import UserProfile
from backend.services.eligibility_service import EligibilityService

def test_eligibility_matching():
    service = EligibilityService()

    profile = UserProfile(
        name="Ramesh Kumar",
        age=24,
        education="Graduate",
        annual_income=150000,
        category="OBC",
        gender="Male",
        state="Karnataka",
        district="Bengaluru",
        employment_status="Unemployed",
        disability_status="No"
    )

    context = (
        "Scholarship Scheme Guidelines 2026.\n"
        "Eligibility Criteria:\n"
        "1. Age limit between 18 to 30 years.\n"
        "2. Minimum qualification: Graduate degree.\n"
        "3. Family annual income less than 250000 rupees.\n"
    )

    chunks = [
        {"text": context, "source": "scheme.pdf", "page": 2, "category": "scholarship", "document_date": "2026-01-01"}
    ]

    result = service.evaluate_eligibility(
        profile=profile,
        question="Am I eligible for this scholarship?",
        context=context,
        chunks=chunks
    )

    assert result.status in ["MATCH", "PARTIAL_MATCH"]
    assert "SevaAI guidance only" in result.disclaimer
    assert len(result.criteria) >= 3

def test_eligibility_over_age():
    service = EligibilityService()

    profile = UserProfile(
        name="Anita",
        age=38,
        education="Graduate",
        annual_income=100000,
        category="General"
    )

    context = "Maximum age limit up to 30 years as of 2026."
    chunks = [{"text": context, "source": "job.pdf", "page": 1}]

    result = service.evaluate_eligibility(
        profile=profile,
        question="What is the age limit?",
        context=context,
        chunks=chunks
    )

    assert result.status == "NOT_MATCHED"
