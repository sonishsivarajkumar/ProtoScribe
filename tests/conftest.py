"""Test configuration and fixtures"""
import pytest
import os
import tempfile
from pathlib import Path

# Set test environment
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["TESTING"] = "true"


@pytest.fixture
def temp_file():
    """Create a temporary file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("This is a test protocol document.\n\nIntroduction\nThis is the introduction section.\n\nMethods\nThis is the methods section.")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def sample_protocol_content():
    """Sample protocol content for testing"""
    return """
    A Randomized Controlled Trial of Intervention X versus Placebo in Patients with Condition Y
    
    Abstract
    Background: Previous studies have shown...
    Methods: This is a double-blind, placebo-controlled trial...
    Results: Will be reported after trial completion...
    Conclusions: To be determined...
    
    Introduction
    Scientific background and explanation of rationale...
    
    Objectives
    The primary objective is to determine whether intervention X is superior to placebo...
    
    Methods
    Study Design: This is a parallel-group, randomized controlled trial with 1:1 allocation.
    
    Participants: Participants will be recruited from outpatient clinics.
    
    Eligibility Criteria:
    Inclusion criteria: 1) Age 18-65 years, 2) Diagnosed with condition Y
    Exclusion criteria: 1) Pregnant women, 2) Severe comorbidities
    
    Interventions: 
    Experimental group: Participants will receive intervention X
    Control group: Participants will receive placebo
    
    Primary Outcome: Change in symptom severity score from baseline to 12 weeks
    
    Secondary Outcomes: Quality of life scores, adverse events
    
    Sample Size: A total of 200 participants will be enrolled
    
    Randomization: Computer-generated randomization sequence will be used
    
    Blinding: Participants, investigators, and outcome assessors will be blinded
    
    Statistical Analysis: Intention-to-treat analysis using mixed-effects models
    """


@pytest.fixture
def sample_sections():
    """Sample protocol sections for testing"""
    return {
        "Title": "A Randomized Controlled Trial of Intervention X versus Placebo",
        "Abstract": "Background: Previous studies... Methods: This is a trial... Results: TBD... Conclusions: TBD...",
        "Introduction": "Scientific background and explanation of rationale...",
        "Objectives": "The primary objective is to determine whether intervention X is superior to placebo...",
        "Methods": "Study Design: Parallel-group RCT. Participants: From clinics. Interventions: X vs placebo.",
        "Outcomes": "Primary: Symptom severity. Secondary: QoL, AEs.",
        "Statistical Analysis": "Intention-to-treat analysis using mixed-effects models"
    }
