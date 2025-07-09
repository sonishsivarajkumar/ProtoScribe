from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import aiofiles
import os
from datetime import datetime
import uuid

from ..models.database import get_db
from ..models.protocol import Protocol, ProtocolCreate, ProtocolResponse
from ..services.document_processor import DocumentProcessor
from ..core.config import settings

router = APIRouter()

# Mock protocol storage (replace with actual database)
MOCK_PROTOCOLS_STORE = {
    "protocol_123": {
        "id": "protocol_123",
        "title": "Hypertension Treatment Study",
        "filename": "hypertension_protocol.pdf",
        "upload_timestamp": "2025-01-08T09:00:00Z",
        "status": "processed",
        "sections_count": 4,
        "content": """
        TITLE: A Randomized Controlled Trial of Antihypertensive Treatment in Adults
        
        INTRODUCTION:
        Hypertension affects millions of adults worldwide and is a major risk factor for cardiovascular disease.
        This study aims to evaluate the efficacy of a new antihypertensive medication.
        
        METHODS:
        Study Design: This is a double-blind, randomized, placebo-controlled trial.
        Participants: Adults aged 18-65 with diagnosed hypertension.
        Primary Outcome: Change in systolic blood pressure from baseline.
        
        STATISTICAL ANALYSIS:
        We will use t-tests to compare groups with p<0.05 considered significant.
        """,
        "sections": {
            "title": "A Randomized Controlled Trial of Antihypertensive Treatment in Adults",
            "introduction": "Hypertension affects millions of adults worldwide and is a major risk factor for cardiovascular disease. This study aims to evaluate the efficacy of a new antihypertensive medication.",
            "methods": "Study Design: This is a double-blind, randomized, placebo-controlled trial. Participants: Adults aged 18-65 with diagnosed hypertension. Primary Outcome: Change in systolic blood pressure from baseline.",
            "statistical_analysis": "We will use t-tests to compare groups with p<0.05 considered significant."
        }
    }
}


@router.post("/upload", response_model=ProtocolResponse)
async def upload_protocol(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process a protocol document"""
    
    # Validate file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_extension} not allowed. Supported types: {settings.ALLOWED_FILE_TYPES}"
        )
    
    # Validate file size
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes"
        )
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, f"{datetime.now().timestamp()}_{file.filename}")
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    try:
        # Process document
        processor = DocumentProcessor()
        processed_data = await processor.process_document(file_path)
        
        # Create protocol record
        protocol_data = {
            "title": processed_data.get("title", file.filename),
            "filename": file.filename,
            "file_path": file_path,
            "content": processed_data.get("content", ""),
            "sections": processed_data.get("sections", {}),
            "upload_timestamp": datetime.now().isoformat()
        }
        
        # Save to database (implement this based on your model)
        # protocol = create_protocol(db, protocol_data)
        
        return {
            "id": "temp_id",  # Replace with actual protocol ID
            "title": protocol_data["title"],
            "filename": protocol_data["filename"],
            "upload_timestamp": protocol_data["upload_timestamp"],
            "status": "processed",
            "sections_count": len(protocol_data["sections"])
        }
        
    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.get("/", response_model=List[Dict[str, Any]])
async def list_protocols(db: Session = Depends(get_db)):
    """List all protocols"""
    protocols = []
    for protocol_id, protocol_data in MOCK_PROTOCOLS_STORE.items():
        protocols.append({
            "id": protocol_data["id"],
            "title": protocol_data["title"],
            "filename": protocol_data["filename"],
            "upload_timestamp": protocol_data["upload_timestamp"],
            "status": protocol_data["status"],
            "sections_count": protocol_data["sections_count"]
        })
    return protocols


@router.get("/{protocol_id}")
async def get_protocol(protocol_id: str, db: Session = Depends(get_db)):
    """Get a specific protocol by ID"""
    if protocol_id not in MOCK_PROTOCOLS_STORE:
        raise HTTPException(status_code=404, detail="Protocol not found")
    
    return MOCK_PROTOCOLS_STORE[protocol_id]


@router.delete("/{protocol_id}")
async def delete_protocol(protocol_id: str, db: Session = Depends(get_db)):
    """Delete a protocol"""
    if protocol_id not in MOCK_PROTOCOLS_STORE:
        raise HTTPException(status_code=404, detail="Protocol not found")
    
    del MOCK_PROTOCOLS_STORE[protocol_id]
    return {"message": "Protocol deleted successfully"}


@router.post("/create-sample")
async def create_sample_protocol(db: Session = Depends(get_db)):
    """Create a sample protocol for testing"""
    protocol_id = f"protocol_{uuid.uuid4().hex[:8]}"
    
    sample_protocol = {
        "id": protocol_id,
        "title": "Sample Clinical Trial Protocol",
        "filename": "sample_protocol.pdf",
        "upload_timestamp": datetime.utcnow().isoformat(),
        "status": "processed",
        "sections_count": 5,
        "content": """
        TITLE: A Sample Randomized Controlled Trial Protocol
        
        BACKGROUND AND RATIONALE:
        This is a sample protocol demonstrating the structure and content of a clinical trial protocol.
        
        OBJECTIVES:
        Primary: To demonstrate protocol structure
        Secondary: To test the AI analysis system
        
        STUDY DESIGN:
        This is a randomized, double-blind, placebo-controlled trial.
        
        PARTICIPANTS:
        Inclusion criteria: Adults over 18 years
        Exclusion criteria: Pregnant women, children
        
        INTERVENTIONS:
        Treatment group: Active medication
        Control group: Placebo
        
        OUTCOMES:
        Primary outcome: Response rate at 12 weeks
        Secondary outcomes: Safety measures
        
        STATISTICAL ANALYSIS:
        Sample size: 100 participants per group
        Analysis: Chi-square test for primary outcome
        """,
        "sections": {
            "title": "A Sample Randomized Controlled Trial Protocol",
            "background": "This is a sample protocol demonstrating the structure and content of a clinical trial protocol.",
            "objectives": "Primary: To demonstrate protocol structure. Secondary: To test the AI analysis system",
            "design": "This is a randomized, double-blind, placebo-controlled trial.",
            "participants": "Inclusion criteria: Adults over 18 years. Exclusion criteria: Pregnant women, children",
            "interventions": "Treatment group: Active medication. Control group: Placebo",
            "outcomes": "Primary outcome: Response rate at 12 weeks. Secondary outcomes: Safety measures",
            "statistical_analysis": "Sample size: 100 participants per group. Analysis: Chi-square test for primary outcome"
        }
    }
    
    MOCK_PROTOCOLS_STORE[protocol_id] = sample_protocol
    
    return {
        "message": "Sample protocol created successfully",
        "protocol_id": protocol_id,
        "protocol": sample_protocol
    }
