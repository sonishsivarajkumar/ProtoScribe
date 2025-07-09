#!/usr/bin/env python3
"""
Simple ProtoScribe startup script
"""
import uvicorn
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    print("Starting ProtoScribe Backend Server...")
    print("Visit http://localhost:8000/docs for API documentation")
    
    uvicorn.run(
        "protoscribe.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
