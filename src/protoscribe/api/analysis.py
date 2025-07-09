from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from ..models.database import get_db
from ..services.compliance_checker import ComplianceChecker
from ..services.advanced_llm_analyzer import AdvancedLLMAnalyzer
from ..services.llm_analyzer import LLMAnalyzer
from ..core.config import settings

router = APIRouter()

# Mock protocol storage (replace with actual database)
MOCK_PROTOCOLS = {
    "protocol_123": {
        "id": "protocol_123",
        "title": "Hypertension Treatment Study",
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
        },
        "created_at": "2025-01-08T09:00:00Z"
    }
}

# Sync with protocols API
from .protocols import MOCK_PROTOCOLS_STORE
MOCK_PROTOCOLS.update(MOCK_PROTOCOLS_STORE)

def get_protocol_by_id(protocol_id: str) -> Optional[Dict]:
    """Get protocol by ID (mock implementation)"""
    return MOCK_PROTOCOLS.get(protocol_id)


@router.post("/{protocol_id}/comprehensive")
async def comprehensive_analysis(
    protocol_id: str,
    background_tasks: BackgroundTasks,
    provider: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Run comprehensive AI-powered analysis of a protocol"""
    
    try:
        # Get protocol from mock storage
        protocol = get_protocol_by_id(protocol_id)
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocol not found")
        
        protocol_content = protocol["content"]
        protocol_sections = protocol["sections"]
        
        # Run compliance check first
        checker = ComplianceChecker()
        compliance_results = await checker.check_compliance(protocol_content, protocol_sections)
        
        # Initialize advanced analyzer
        analyzer = AdvancedLLMAnalyzer(provider=provider)
        
        # Check if LLM service is available
        if not analyzer.client:
            # Return compliance-only results if LLM not available
            return {
                "protocol_id": protocol_id,
                "compliance_analysis": compliance_results,
                "ai_analysis": {"note": "LLM service not available - compliance analysis only"},
                "overall_score": compliance_results.get("score", 0),
                "analysis_provider": "rule_based_only",
                "recommendations_count": len(compliance_results.get("failed_items", [])),
                "status": "partial_complete"
            }
        
        # Run comprehensive analysis
        analysis_results = await analyzer.analyze_protocol_comprehensive(
            content=protocol_content,
            sections=protocol_sections,
            missing_items=compliance_results.get("failed_items", [])
        )
        
        # Combine results
        comprehensive_results = {
            "protocol_id": protocol_id,
            "compliance_analysis": compliance_results,
            "ai_analysis": analysis_results,
            "overall_score": compliance_results.get("score", 0),
            "analysis_provider": provider or settings.DEFAULT_LLM_PROVIDER,
            "recommendations_count": len(analysis_results.get("missing_items_analysis", [])) + 
                                   len(analysis_results.get("clarity_analysis", [])),
            "status": "complete",
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        return comprehensive_results
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Comprehensive analysis failed: {str(e)}"
        )


@router.get("/{protocol_id}/formatted-analysis")
async def get_formatted_analysis(
    protocol_id: str,
    provider: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get analysis formatted for the frontend UI"""
    
    try:
        # Get protocol from mock storage
        protocol = get_protocol_by_id(protocol_id)
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocol not found")
        
        # Mock analysis data formatted for frontend
        formatted_analysis = {
            "protocol_id": protocol_id,
            "overall_score": 85.5,
            "component_scores": {
                "consort_compliance": 88.0,
                "spirit_compliance": 83.0,
                "clarity_score": 82.5,
                "consistency_score": 89.0
            },
            "suggestions": [
                {
                    "id": "sug_1",
                    "type": "missing_item",
                    "section": "Methods",
                    "issue": "Missing primary outcome definition",
                    "suggested_text": "The primary outcome is the change in systolic blood pressure from baseline to 12 weeks, measured using a standardized sphygmomanometer in the seated position after 5 minutes of rest.",
                    "explanation": "CONSORT guidelines require a clear definition of primary outcomes with specific measurement methods and timing.",
                    "confidence": 0.92,
                    "status": "pending",
                    "guideline": "CONSORT 6a"
                },
                {
                    "id": "sug_2",
                    "type": "clarity",
                    "section": "Participants",
                    "issue": "Inclusion criteria could be more specific",
                    "suggested_text": "Adults aged 18-65 years with hypertension (systolic BP ≥140 mmHg or diastolic BP ≥90 mmHg on two separate occasions) who are not currently taking antihypertensive medications.",
                    "explanation": "More specific criteria help ensure consistent participant selection and improve reproducibility.",
                    "confidence": 0.78,
                    "status": "pending"
                },
                {
                    "id": "sug_3",
                    "type": "consistency",
                    "section": "Statistical Analysis",
                    "issue": "Sample size calculation inconsistent with stated power",
                    "suggested_text": "Based on a two-sided alpha of 0.05, power of 80%, and expected difference of 10 mmHg (SD=15), we require 36 participants per group. Accounting for 20% dropout, we will recruit 45 participants per group (total N=90).",
                    "explanation": "The current sample size calculation shows 90% power but the methods section mentions 80% power.",
                    "confidence": 0.85,
                    "status": "pending"
                }
            ],
            "executive_summary": "This protocol demonstrates good overall compliance with CONSORT/SPIRIT guidelines with a score of 85.5%. Key strengths include well-defined study design and comprehensive statistical analysis plan. Primary areas for improvement include more specific outcome definitions and consistency in power calculations.",
            "analysis_provider": provider or settings.DEFAULT_LLM_PROVIDER,
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        return formatted_analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting formatted analysis: {str(e)}")


@router.post("/{protocol_id}/compliance")
async def analyze_compliance(
    protocol_id: str,
    db: Session = Depends(get_db)
):
    """Analyze protocol compliance against CONSORT/SPIRIT guidelines"""
    
    try:
        # Get protocol from database
        # protocol = get_protocol_by_id(db, protocol_id)
        # if not protocol:
        #     raise HTTPException(status_code=404, detail="Protocol not found")
        
        # Run compliance check
        checker = ComplianceChecker()
        compliance_results = await checker.check_compliance("sample_content")  # Replace with actual protocol content
        
        return {
            "protocol_id": protocol_id,
            "compliance_score": compliance_results.get("score", 0),
            "total_items": compliance_results.get("total_items", 0),
            "passed_items": compliance_results.get("passed_items", 0),
            "failed_items": compliance_results.get("failed_items", []),
            "warnings": compliance_results.get("warnings", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing compliance: {str(e)}")


@router.post("/{protocol_id}/suggestions")
async def generate_suggestions(
    protocol_id: str,
    provider: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Generate AI-powered suggestions for protocol improvement"""
    
    try:
        # Get protocol from database
        # protocol = get_protocol_by_id(db, protocol_id)
        # if not protocol:
        #     raise HTTPException(status_code=404, detail="Protocol not found")
        
        # Generate suggestions using advanced LLM
        analyzer = AdvancedLLMAnalyzer(provider=provider)
        suggestions = await analyzer._analyze_missing_items(
            "sample_content", 
            {"Methods": "sample methods"}, 
            []
        )
        
        return {
            "protocol_id": protocol_id,
            "suggestions": suggestions,
            "total_suggestions": len(suggestions),
            "provider": provider or settings.DEFAULT_LLM_PROVIDER
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")


@router.post("/{protocol_id}/clarity-check")
async def analyze_clarity(
    protocol_id: str,
    provider: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Analyze protocol for clarity and readability issues"""
    
    try:
        analyzer = AdvancedLLMAnalyzer(provider=provider)
        clarity_results = await analyzer._analyze_clarity_and_completeness(
            "sample_content",
            {"Methods": "sample methods", "Introduction": "sample intro"}
        )
        
        return {
            "protocol_id": protocol_id,
            "clarity_issues": clarity_results,
            "issues_count": len(clarity_results),
            "provider": provider or settings.DEFAULT_LLM_PROVIDER
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing clarity: {str(e)}")


@router.post("/{protocol_id}/consistency-check")
async def analyze_consistency(
    protocol_id: str,
    provider: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Check protocol for internal consistency issues"""
    
    try:
        analyzer = AdvancedLLMAnalyzer(provider=provider)
        consistency_results = await analyzer._analyze_consistency(
            "sample_content",
            {"Methods": "sample methods", "Introduction": "sample intro"}
        )
        
        return {
            "protocol_id": protocol_id,
            "consistency_issues": consistency_results,
            "issues_count": len(consistency_results),
            "provider": provider or settings.DEFAULT_LLM_PROVIDER
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing consistency: {str(e)}")


@router.get("/{protocol_id}/executive-summary")
async def get_executive_summary(
    protocol_id: str,
    provider: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get executive summary of protocol analysis"""
    
    try:
        analyzer = AdvancedLLMAnalyzer(provider=provider)
        summary = await analyzer._generate_executive_summary(
            "sample_content",
            {"Methods": "sample methods", "Introduction": "sample intro"}
        )
        
        return {
            "protocol_id": protocol_id,
            "executive_summary": summary,
            "provider": provider or settings.DEFAULT_LLM_PROVIDER,
            "generated_at": "2025-01-08T10:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


@router.get("/{protocol_id}/analysis-history")
async def get_analysis_history(
    protocol_id: str,
    db: Session = Depends(get_db)
):
    """Get history of all analyses for a protocol"""
    
    try:
        # Mock implementation - replace with actual database query
        history = [
            {
                "analysis_id": "analysis_1",
                "analysis_type": "comprehensive",
                "timestamp": "2025-01-08T09:30:00Z",
                "score": 85.5,
                "provider": "openai",
                "suggestions_count": 12
            },
            {
                "analysis_id": "analysis_2", 
                "analysis_type": "compliance",
                "timestamp": "2025-01-08T09:00:00Z",
                "score": 82.0,
                "provider": "rule_based",
                "suggestions_count": 8
            }
        ]
        
        return {
            "protocol_id": protocol_id,
            "analysis_history": history,
            "total_analyses": len(history)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving analysis history: {str(e)}")


@router.post("/{protocol_id}/compare-providers")
async def compare_providers(
    protocol_id: str,
    providers: List[str] = ["openai", "anthropic"],
    db: Session = Depends(get_db)
):
    """Compare analysis results from different AI providers"""
    
    try:
        results = {}
        
        for provider in providers:
            try:
                analyzer = AdvancedLLMAnalyzer(provider=provider)
                if analyzer.client:  # Only run if provider is available
                    analysis = await analyzer.analyze_protocol_comprehensive(
                        "sample_content",
                        {"Methods": "sample methods"},
                        []
                    )
                    results[provider] = {
                        "status": "success",
                        "analysis": analysis,
                        "summary": analysis.get("executive_summary", "")[:200] + "..."
                    }
                else:
                    results[provider] = {
                        "status": "unavailable",
                        "error": "Provider not configured or unavailable"
                    }
            except Exception as e:
                results[provider] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return {
            "protocol_id": protocol_id,
            "provider_comparison": results,
            "comparison_timestamp": "2025-01-08T10:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing providers: {str(e)}")


@router.get("/{protocol_id}/score")
async def get_protocol_score(
    protocol_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed protocol completeness score"""
    
    try:
        # Mock implementation - replace with actual database query
        return {
            "protocol_id": protocol_id,
            "overall_score": 85.5,
            "component_scores": {
                "consort_compliance": 88.0,
                "spirit_compliance": 83.0,
                "clarity_score": 82.5,
                "consistency_score": 89.0,
                "completeness_score": 86.0
            },
            "score_breakdown": {
                "administrative_info": 95.0,
                "introduction": 88.0,
                "methods": 82.0,
                "statistical_analysis": 85.0,
                "ethics": 90.0
            },
            "improvement_potential": 12.5,
            "last_analyzed": "2025-01-08T10:00:00Z",
            "analysis_count": 3
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving score: {str(e)}")
