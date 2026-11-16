from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# Authentication Schemas
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = "Citizen"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Citizen Profile Schemas
class ProfileBase(BaseModel):
    name: Optional[str] = "Citizen"
    state: Optional[str] = "Unknown"
    district: Optional[str] = "Unknown"
    age: Optional[int] = None
    education: Optional[str] = "Unknown"
    category: Optional[str] = "General"
    gender: Optional[str] = "Prefer not to provide"
    employment_status: Optional[str] = "Unknown"
    annual_income: Optional[float] = None
    disability_status: Optional[str] = "No"

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    user_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

# Document Schemas
class DocumentResponse(BaseModel):
    id: int
    filename: str
    category: str
    upload_date: str
    document_date: Optional[str] = None
    page_count: int
    chunk_count: int
    status: str

    model_config = ConfigDict(from_attributes=True)

# RAG & Citation Schemas
class SourceCitation(BaseModel):
    document: str
    page: int
    category: str
    document_date: Optional[str] = "2026-01-01"
    snippet: str
    score: Optional[float] = 0.0

class EligibilityCriterion(BaseModel):
    criterion: str
    status: str  # MATCH, PARTIAL_MATCH, NOT_MATCHED, UNKNOWN
    user_value: Optional[str] = None
    required_value: Optional[str] = None
    note: str

class EligibilityResult(BaseModel):
    status: str  # MATCH, PARTIAL_MATCH, NOT_MATCHED, UNKNOWN
    summary: str
    criteria: List[EligibilityCriterion] = []
    disclaimer: str

class ChatRequest(BaseModel):
    question: str
    check_eligibility: bool = False

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceCitation] = []
    confidence: str = "medium"  # high, medium, low
    grounded: bool = True
    eligibility: Optional[EligibilityResult] = None
    disclaimer: str
