from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import json
import os

from ..core.config import settings

router = APIRouter()


@router.get("/consort")
async def get_consort_guidelines():
    """Get CONSORT guidelines checklist"""
    
    try:
        guidelines_path = os.path.join(settings.GUIDELINES_DIR, "consort.json")
        if os.path.exists(guidelines_path):
            with open(guidelines_path, 'r') as f:
                guidelines = json.load(f)
        else:
            # Return default CONSORT guidelines if file doesn't exist
            guidelines = get_default_consort_guidelines()
        
        return {
            "guideline_type": "CONSORT",
            "version": "2010",
            "items": guidelines.get("items", []),
            "total_items": len(guidelines.get("items", []))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading CONSORT guidelines: {str(e)}")


@router.get("/spirit")
async def get_spirit_guidelines():
    """Get SPIRIT guidelines checklist"""
    
    try:
        guidelines_path = os.path.join(settings.GUIDELINES_DIR, "spirit.json")
        if os.path.exists(guidelines_path):
            with open(guidelines_path, 'r') as f:
                guidelines = json.load(f)
        else:
            # Return default SPIRIT guidelines if file doesn't exist
            guidelines = get_default_spirit_guidelines()
        
        return {
            "guideline_type": "SPIRIT",
            "version": "2013",
            "items": guidelines.get("items", []),
            "total_items": len(guidelines.get("items", []))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading SPIRIT guidelines: {str(e)}")


@router.get("/")
async def list_guidelines():
    """List all available guidelines"""
    
    return {
        "available_guidelines": [
            {
                "name": "CONSORT",
                "description": "Consolidated Standards of Reporting Trials",
                "version": "2010",
                "endpoint": "/api/v1/guidelines/consort"
            },
            {
                "name": "SPIRIT",
                "description": "Standard Protocol Items: Recommendations for Interventional Trials",
                "version": "2013",
                "endpoint": "/api/v1/guidelines/spirit"
            }
        ]
    }


def get_default_consort_guidelines():
    """Return default CONSORT guidelines structure"""
    return {
        "items": [
            {
                "id": "1a",
                "section": "Title and abstract",
                "item": "Title",
                "description": "Identification as a randomised trial in the title",
                "example": "A randomised controlled trial of..."
            },
            {
                "id": "1b", 
                "section": "Title and abstract",
                "item": "Abstract",
                "description": "Structured summary of trial design, methods, results, and conclusions",
                "example": "Background: ... Methods: ... Results: ... Conclusions: ..."
            },
            {
                "id": "2a",
                "section": "Introduction",
                "item": "Background",
                "description": "Scientific background and explanation of rationale",
                "example": "Previous studies have shown..."
            },
            {
                "id": "2b",
                "section": "Introduction", 
                "item": "Objectives",
                "description": "Specific objectives or hypotheses",
                "example": "The primary objective is to determine..."
            }
            # Add more CONSORT items as needed
        ]
    }


def get_default_spirit_guidelines():
    """Return default SPIRIT guidelines structure"""
    return {
        "items": [
            {
                "id": "1",
                "section": "Administrative information",
                "item": "Title",
                "description": "Descriptive title identifying the study design, population, interventions, and, if applicable, trial acronym",
                "example": "A randomised, double-blind, placebo-controlled trial of..."
            },
            {
                "id": "2a",
                "section": "Administrative information",
                "item": "Trial registration",
                "description": "Trial identifier and registry name. If not yet registered, name of intended registry",
                "example": "ClinicalTrials.gov identifier: NCT12345678"
            },
            {
                "id": "3",
                "section": "Administrative information",
                "item": "Protocol version",
                "description": "Date and version identifier",
                "example": "Protocol version 2.0, dated 15 March 2023"
            }
            # Add more SPIRIT items as needed
        ]
    }
