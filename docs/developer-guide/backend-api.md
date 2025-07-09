# Backend API

Comprehensive guide to ProtoScribe's FastAPI backend, including endpoints, data models, and integration patterns.

## API Overview

ProtoScribe's backend API is built with FastAPI, providing high-performance, type-safe endpoints for protocol management and AI analysis.

### Base Configuration

```python
# src/protoscribe/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ProtoScribe API",
    description="Clinical Trial Protocol AI Optimizer",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://protoscribe.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Documentation

**Interactive Documentation:**
- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **OpenAPI Spec**: Available at `/openapi.json`

## Core Endpoints

### Protocol Management

#### Create Protocol
```http
POST /api/protocols/
Content-Type: multipart/form-data

file: protocol.pdf
title: "Phase II Oncology Trial"
description: "Randomized controlled trial for new cancer therapy"
```

**Response:**
```json
{
  "id": "proto_123",
  "title": "Phase II Oncology Trial",
  "description": "Randomized controlled trial for new cancer therapy",
  "status": "processing",
  "file_size": 2048576,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### List Protocols
```http
GET /api/protocols/
```

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100)
- `status`: Filter by status (`processing`, `ready`, `error`)

**Response:**
```json
{
  "protocols": [
    {
      "id": "proto_123",
      "title": "Phase II Oncology Trial",
      "status": "ready",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

#### Get Protocol
```http
GET /api/protocols/{protocol_id}
```

**Response:**
```json
{
  "id": "proto_123",
  "title": "Phase II Oncology Trial",
  "description": "Randomized controlled trial for new cancer therapy",
  "content": "Full protocol text content...",
  "status": "ready",
  "file_size": 2048576,
  "metadata": {
    "pages": 45,
    "words": 12500,
    "sections": 12
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Update Protocol
```http
PUT /api/protocols/{protocol_id}
Content-Type: application/json

{
  "title": "Updated Protocol Title",
  "description": "Updated description",
  "content": "Updated protocol content..."
}
```

#### Delete Protocol
```http
DELETE /api/protocols/{protocol_id}
```

### Analysis Endpoints

#### Comprehensive Analysis
```http
POST /api/protocols/{protocol_id}/analyze
Content-Type: application/json

{
  "analysis_type": "comprehensive",
  "provider": "openai",
  "guidelines": ["consort", "spirit"],
  "options": {
    "include_suggestions": true,
    "confidence_threshold": 0.7
  }
}
```

**Response:**
```json
{
  "analysis_id": "analysis_456",
  "status": "completed",
  "provider": "openai",
  "results": {
    "overall_score": 85,
    "consort_score": 88,
    "spirit_score": 82,
    "categories": {
      "study_design": {"score": 90, "status": "good"},
      "methodology": {"score": 85, "status": "good"},
      "ethics": {"score": 75, "status": "needs_improvement"}
    }
  },
  "suggestions": [
    {
      "id": "sugg_789",
      "section": "methodology",
      "type": "improvement",
      "content": "Add detailed randomization sequence description",
      "confidence": 0.92,
      "priority": "medium"
    }
  ],
  "created_at": "2024-01-15T10:35:00Z"
}
```

#### Clarity Analysis
```http
POST /api/protocols/{protocol_id}/analyze/clarity
```

**Response:**
```json
{
  "clarity_score": 78,
  "readability": {
    "flesch_score": 45.2,
    "grade_level": "graduate",
    "avg_sentence_length": 18.5
  },
  "language_issues": [
    {
      "section": "introduction",
      "issue": "passive_voice_overuse",
      "suggestion": "Use more active voice constructions"
    }
  ],
  "terminology": {
    "consistency_score": 85,
    "undefined_terms": ["biomarker", "PFS"],
    "inconsistent_usage": []
  }
}
```

#### Consistency Analysis
```http
POST /api/protocols/{protocol_id}/analyze/consistency
```

#### Executive Summary
```http
GET /api/protocols/{protocol_id}/summary
```

**Response:**
```json
{
  "protocol_id": "proto_123",
  "title": "Phase II Oncology Trial",
  "summary": {
    "study_type": "Randomized Controlled Trial",
    "phase": "II",
    "population": "Advanced cancer patients",
    "intervention": "Novel targeted therapy",
    "primary_endpoint": "Progression-free survival",
    "sample_size": 200,
    "duration": "24 months"
  },
  "compliance_overview": {
    "overall_score": 85,
    "strengths": [
      "Well-defined primary endpoint",
      "Appropriate statistical methods",
      "Clear inclusion/exclusion criteria"
    ],
    "areas_for_improvement": [
      "Missing sample size justification details",
      "Incomplete safety monitoring plan"
    ],
    "critical_issues": []
  }
}
```

#### Provider Comparison
```http
POST /api/protocols/{protocol_id}/compare-providers
Content-Type: application/json

{
  "providers": ["openai", "anthropic"],
  "analysis_type": "comprehensive"
}
```

### Suggestion Management

#### Get Suggestions
```http
GET /api/protocols/{protocol_id}/suggestions
```

**Query Parameters:**
- `section`: Filter by protocol section
- `type`: Filter by suggestion type (`critical`, `improvement`, `style`)
- `status`: Filter by status (`pending`, `accepted`, `rejected`)

#### Update Suggestion Status
```http
PUT /api/suggestions/{suggestion_id}
Content-Type: application/json

{
  "status": "accepted",
  "user_comment": "Good suggestion, implementing as recommended",
  "modified_content": "Alternative implementation text..."
}
```

### Export Endpoints

#### Export Protocol
```http
POST /api/protocols/{protocol_id}/export
Content-Type: application/json

{
  "format": "pdf",
  "include_changes": true,
  "include_suggestions": false,
  "template": "regulatory_submission"
}
```

**Response:**
```json
{
  "export_id": "export_321",
  "download_url": "/api/downloads/export_321",
  "format": "pdf",
  "file_size": 1024000,
  "created_at": "2024-01-15T11:00:00Z",
  "expires_at": "2024-01-16T11:00:00Z"
}
```

#### Download Export
```http
GET /api/downloads/{export_id}
```

## Data Models

### Core Models

#### Protocol Model
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class Protocol(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    content: str
    status: str  # "processing", "ready", "error"
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

class ProtocolCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ProtocolUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
```

#### Analysis Model
```python
class AnalysisResult(BaseModel):
    analysis_id: str
    protocol_id: str
    provider: str
    analysis_type: str
    status: str  # "pending", "running", "completed", "failed"
    results: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

class AnalysisRequest(BaseModel):
    analysis_type: str = "comprehensive"
    provider: Optional[str] = None
    guidelines: List[str] = ["consort", "spirit"]
    options: Optional[Dict[str, Any]] = None
```

#### Suggestion Model
```python
class Suggestion(BaseModel):
    id: str
    analysis_id: str
    section: str
    type: str  # "critical", "improvement", "style"
    content: str
    confidence: float
    priority: str  # "high", "medium", "low"
    status: str  # "pending", "accepted", "rejected", "modified"
    user_comment: Optional[str] = None
    modified_content: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
```

### Validation Models

#### File Upload Validation
```python
from fastapi import UploadFile, HTTPException

async def validate_protocol_file(file: UploadFile) -> None:
    # Check file size (50MB limit)
    if file.size and file.size > 50 * 1024 * 1024:
        raise HTTPException(400, "File too large (max 50MB)")
    
    # Check file type
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "text/markdown"
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(400, f"Unsupported file type: {file.content_type}")
```

## Error Handling

### Standard Error Responses

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class APIError(Exception):
    def __init__(self, status_code: int, message: str, details: Optional[Dict] = None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )
```

### Common Error Codes

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | Bad Request | Invalid request data or parameters |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict (duplicate, etc.) |
| 413 | Payload Too Large | File upload too large |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | External service unavailable |

## Authentication & Security

### API Key Authentication (Future)

```python
from fastapi import Depends, HTTPException, Header

async def verify_api_key(x_api_key: str = Header(...)) -> str:
    if not x_api_key or not is_valid_api_key(x_api_key):
        raise HTTPException(401, "Invalid API key")
    return x_api_key

@app.get("/api/protocols/", dependencies=[Depends(verify_api_key)])
async def list_protocols():
    # Protected endpoint
    pass
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/protocols/{protocol_id}/analyze")
@limiter.limit("5/minute")  # Limit expensive operations
async def analyze_protocol(request: Request, protocol_id: str):
    # Rate-limited endpoint
    pass
```

## Testing

### Test Structure

```python
import pytest
from fastapi.testclient import TestClient
from src.protoscribe.main import app

client = TestClient(app)

class TestProtocols:
    def test_create_protocol(self):
        response = client.post(
            "/api/protocols/",
            files={"file": ("test.txt", "Protocol content", "text/plain")},
            data={"title": "Test Protocol"}
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Test Protocol"
    
    def test_list_protocols(self):
        response = client.get("/api/protocols/")
        assert response.status_code == 200
        assert "protocols" in response.json()
    
    def test_protocol_not_found(self):
        response = client.get("/api/protocols/nonexistent")
        assert response.status_code == 404
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_analysis_workflow():
    # Upload protocol
    upload_response = client.post(
        "/api/protocols/",
        files={"file": ("protocol.txt", SAMPLE_PROTOCOL, "text/plain")},
        data={"title": "Integration Test Protocol"}
    )
    protocol_id = upload_response.json()["id"]
    
    # Start analysis
    analysis_response = client.post(
        f"/api/protocols/{protocol_id}/analyze",
        json={"analysis_type": "comprehensive"}
    )
    analysis_id = analysis_response.json()["analysis_id"]
    
    # Check results
    results_response = client.get(f"/api/protocols/{protocol_id}/results")
    assert results_response.status_code == 200
    assert results_response.json()["status"] == "completed"
```

## Performance Optimization

### Async Operations

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Background task processing
executor = ThreadPoolExecutor(max_workers=4)

@app.post("/api/protocols/{protocol_id}/analyze")
async def analyze_protocol(protocol_id: str, request: AnalysisRequest):
    # Start analysis in background
    task = asyncio.create_task(
        run_analysis_background(protocol_id, request)
    )
    
    # Return immediately with task ID
    return {
        "analysis_id": generate_analysis_id(),
        "status": "started",
        "message": "Analysis started, check back for results"
    }
```

### Caching

```python
from functools import lru_cache
import aioredis

# In-memory caching for frequently accessed data
@lru_cache(maxsize=100)
def get_guideline_content(guideline_name: str) -> str:
    return load_guideline_from_file(guideline_name)

# Redis caching for analysis results
async def cache_analysis_result(analysis_id: str, result: dict):
    redis = await aioredis.from_url("redis://localhost")
    await redis.setex(f"analysis:{analysis_id}", 3600, json.dumps(result))
```

!!! tip "API Best Practices"
    - Use consistent naming conventions
    - Implement proper pagination for list endpoints
    - Return appropriate HTTP status codes
    - Include comprehensive error messages
    - Add request/response examples in documentation

!!! warning "Security Considerations"
    - Validate all input data
    - Implement rate limiting for expensive operations
    - Log security-relevant events
    - Never expose internal error details to clients

!!! info "Performance Tips"
    - Use async/await for I/O operations
    - Implement caching for expensive computations
    - Add database indexes for frequently queried fields
    - Monitor and optimize slow endpoints
