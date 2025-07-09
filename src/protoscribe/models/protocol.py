from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

from .database import Base


class Protocol(Base):
    """Protocol database model"""
    __tablename__ = "protocols"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    content = Column(Text)
    sections = Column(JSON)
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    last_analyzed = Column(DateTime(timezone=True))
    status = Column(String(50), default="uploaded")


class Analysis(Base):
    """Analysis results database model"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    protocol_id = Column(Integer, nullable=False)
    compliance_score = Column(Float)
    consort_score = Column(Float)
    spirit_score = Column(Float)
    missing_items = Column(JSON)
    suggestions = Column(JSON)
    analysis_timestamp = Column(DateTime(timezone=True), server_default=func.now())


# Pydantic models for API

class ProtocolCreate(BaseModel):
    """Protocol creation model"""
    title: str
    filename: str
    file_path: str
    content: str
    sections: Dict[str, Any]
    upload_timestamp: datetime


class ProtocolResponse(BaseModel):
    """Protocol response model"""
    id: str
    title: str
    filename: str
    upload_timestamp: datetime
    status: str
    sections_count: int
    
    class Config:
        from_attributes = True


class AnalysisResponse(BaseModel):
    """Analysis response model"""
    protocol_id: str
    compliance_score: float
    consort_score: Optional[float] = None
    spirit_score: Optional[float] = None
    missing_items: list
    suggestions: list
    analysis_timestamp: datetime
    
    class Config:
        from_attributes = True


class SuggestionItem(BaseModel):
    """Individual suggestion model"""
    item_id: str
    section: str
    issue_type: str  # "missing", "incomplete", "unclear"
    description: str
    suggested_text: str
    confidence: float
    reasoning: str


class ComplianceItem(BaseModel):
    """Compliance check item model"""
    item_id: str
    guideline: str  # "CONSORT" or "SPIRIT"
    section: str
    description: str
    status: str  # "pass", "fail", "warning"
    found_text: Optional[str] = None
    suggestion: Optional[str] = None
