"""Tests for compliance checker service"""
import pytest
import asyncio

from src.protoscribe.services.compliance_checker import ComplianceChecker


class TestComplianceChecker:
    """Test cases for ComplianceChecker"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.checker = ComplianceChecker()
    
    @pytest.mark.asyncio
    async def test_check_compliance(self, sample_protocol_content, sample_sections):
        """Test compliance checking"""
        result = await self.checker.check_compliance(sample_protocol_content, sample_sections)
        
        assert result is not None
        assert "score" in result
        assert "consort_score" in result
        assert "spirit_score" in result
        assert "total_items" in result
        assert "passed_items" in result
        assert "failed_items" in result
        assert "warnings" in result
        
        assert isinstance(result["score"], (int, float))
        assert 0 <= result["score"] <= 100
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        description = "Identification as a randomised trial in the title"
        keywords = self.checker._extract_keywords(description)
        
        assert len(keywords) > 0
        assert any("random" in keyword for keyword in keywords)
    
    def test_check_item_found(self, sample_protocol_content):
        """Test checking an item that should be found"""
        item = {
            "id": "1a",
            "description": "Identification as a randomised trial in the title",
            "section": "Title"
        }
        
        result = self.checker._check_item(sample_protocol_content, {}, item)
        
        assert result["item_id"] == "1a"
        assert result["status"] in ["pass", "warning", "fail"]
        assert "confidence" in result
    
    def test_find_relevant_sections(self, sample_sections):
        """Test finding relevant sections"""
        relevant = self.checker._find_relevant_sections(sample_sections, "method")
        
        assert len(relevant) > 0
        assert any("method" in section.lower() for section in relevant.keys())
    
    def test_search_for_keywords(self):
        """Test keyword search in text"""
        text = "This is a randomized controlled trial of intervention X versus placebo"
        keywords = ["randomized", "trial", "placebo"]
        
        result = self.checker._search_for_keywords(text, keywords)
        
        assert result["found"] is True
        assert result["confidence"] > 0
        assert len(result["keywords_found"]) > 0
    
    def test_normalize_section_name(self):
        """Test section name normalization"""
        from src.protoscribe.utils.text_processing import normalize_section_name
        
        assert normalize_section_name("1. Introduction") == "introduction"
        assert normalize_section_name("Methods (Participants)") == "methods"
        assert normalize_section_name("  Statistical Analysis  ") == "statistical analysis"
