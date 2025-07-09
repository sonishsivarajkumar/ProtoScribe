from fastapi import APIRouter

# Import all route modules
from .protocols import router as protocols_router
from .analysis import router as analysis_router
from .guidelines import router as guidelines_router

# Create main router
router = APIRouter()

# Include all route modules
router.include_router(protocols_router, prefix="/protocols", tags=["protocols"])
router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
router.include_router(guidelines_router, prefix="/guidelines", tags=["guidelines"])


@router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "ProtoScribe API v1",
        "endpoints": {
            "protocols": "/api/v1/protocols",
            "analysis": "/api/v1/analysis",
            "guidelines": "/api/v1/guidelines"
        }
    }
