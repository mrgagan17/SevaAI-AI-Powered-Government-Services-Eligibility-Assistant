import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False, default="Citizen")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    name = Column(String, nullable=True, default="Citizen")
    state = Column(String, nullable=True, default="Unknown")
    district = Column(String, nullable=True, default="Unknown")
    age = Column(Integer, nullable=True)
    education = Column(String, nullable=True, default="Unknown")
    category = Column(String, nullable=True, default="General")
    gender = Column(String, nullable=True, default="Prefer not to provide")
    employment_status = Column(String, nullable=True, default="Unknown")
    annual_income = Column(Float, nullable=True)
    disability_status = Column(String, nullable=True, default="No")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class DocumentRecord(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    filepath = Column(String, nullable=False)
    category = Column(String, index=True, default="general")
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
    document_date = Column(String, nullable=True, default="2026-01-01")
    page_count = Column(Integer, default=0)
    chunk_count = Column(Integer, default=0)
    status = Column(String, default="uploaded")  # uploaded, indexing, indexed, error

class ChatMessageRecord(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources_json = Column(Text, nullable=True)
    confidence = Column(String, default="medium")
    grounded = Column(String, default="true")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
