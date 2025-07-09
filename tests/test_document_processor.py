"""Tests for document processor service"""
import pytest
import asyncio
from pathlib import Path

from src.protoscribe.services.document_processor import DocumentProcessor


class TestDocumentProcessor:
    """Test cases for DocumentProcessor"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.processor = DocumentProcessor()
    
    @pytest.mark.asyncio
    async def test_process_text_document(self, temp_file, sample_protocol_content):
        """Test processing a text document"""
        # Write sample content to temp file
        with open(temp_file, 'w') as f:
            f.write(sample_protocol_content)
        
        result = await self.processor.process_document(temp_file)
        
        assert result is not None
        assert "title" in result
        assert "content" in result
        assert "sections" in result
        assert "word_count" in result
        assert result["file_type"] == ".txt"
        assert len(result["sections"]) > 0
    
    def test_extract_title(self, sample_protocol_content):
        """Test title extraction"""
        title = self.processor._extract_title(sample_protocol_content)
        
        assert "Randomized Controlled Trial" in title
        assert "Intervention X" in title
    
    def test_segment_sections(self, sample_protocol_content):
        """Test section segmentation"""
        sections = self.processor._segment_sections(sample_protocol_content)
        
        assert len(sections) > 0
        assert any("Introduction" in section for section in sections.keys())
        assert any("Methods" in section for section in sections.keys())
        assert any("Objectives" in section for section in sections.keys())
    
    def test_unsupported_file_format(self):
        """Test handling of unsupported file formats"""
        with pytest.raises(ValueError, match="Unsupported file format"):
            asyncio.run(self.processor.process_document("test.xyz"))
    
    def test_supported_formats(self):
        """Test that all expected formats are supported"""
        expected_formats = ['.pdf', '.docx', '.txt']
        assert self.processor.supported_formats == expected_formats
