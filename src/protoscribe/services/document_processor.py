import os
import re
from typing import Dict, Any, List
from pathlib import Path
import asyncio

try:
    from docx import Document
except ImportError:
    Document = None

try:
    from pdfminer.high_level import extract_text as extract_pdf_text
except ImportError:
    extract_pdf_text = None

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except (ImportError, OSError):
    nlp = None


class DocumentProcessor:
    """Process uploaded documents and extract structured content"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt']
    
    async def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process a document and extract structured content"""
        
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            content = await self._extract_pdf_content(file_path)
        elif file_extension == '.docx':
            content = await self._extract_docx_content(file_path)
        elif file_extension == '.txt':
            content = await self._extract_text_content(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Extract title
        title = self._extract_title(content)
        
        # Segment into sections
        sections = self._segment_sections(content)
        
        return {
            "title": title,
            "content": content,
            "sections": sections,
            "word_count": len(content.split()),
            "file_type": file_extension
        }
    
    async def _extract_pdf_content(self, file_path: str) -> str:
        """Extract text from PDF file"""
        if extract_pdf_text is None:
            raise ImportError("pdfminer.six is required for PDF processing")
        
        try:
            # Run PDF extraction in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            content = await loop.run_in_executor(None, extract_pdf_text, file_path)
            return content
        except Exception as e:
            raise ValueError(f"Error extracting PDF content: {str(e)}")
    
    async def _extract_docx_content(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        if Document is None:
            raise ImportError("python-docx is required for DOCX processing")
        
        try:
            doc = Document(file_path)
            paragraphs = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(paragraph.text)
            return "\n".join(paragraphs)
        except Exception as e:
            raise ValueError(f"Error extracting DOCX content: {str(e)}")
    
    async def _extract_text_content(self, file_path: str) -> str:
        """Extract text from plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Error reading text file: {str(e)}")
    
    def _extract_title(self, content: str) -> str:
        """Extract title from document content"""
        lines = content.split('\n')
        
        # Look for title patterns
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line) < 200:  # Reasonable title length
                # Check if it looks like a title
                if any(keyword in line.lower() for keyword in ['trial', 'study', 'protocol', 'research']):
                    return line
                # If it's the first substantial line, use it
                if len(line) > 10:
                    return line
        
        # Fallback to first non-empty line
        for line in lines:
            line = line.strip()
            if line:
                return line[:100] + "..." if len(line) > 100 else line
        
        return "Untitled Protocol"
    
    def _segment_sections(self, content: str) -> Dict[str, str]:
        """Segment document into sections based on headings"""
        
        sections = {}
        current_section = "Introduction"
        current_content = []
        
        # Common section patterns for clinical trial protocols
        section_patterns = [
            r'^(abstract|summary)$',
            r'^(introduction|background)$',
            r'^(objectives?|aims?)$',
            r'^(methods?|methodology)$',
            r'^(study\s+design)$',
            r'^(participants?|subjects?|population)$',
            r'^(eligibility\s+criteria|inclusion\s+criteria|exclusion\s+criteria)$',
            r'^(interventions?|treatments?)$',
            r'^(outcomes?|endpoints?)$',
            r'^(sample\s+size|statistical\s+analysis)$',
            r'^(data\s+collection|data\s+management)$',
            r'^(ethics?|ethical\s+considerations)$',
            r'^(discussion|limitations)$',
            r'^(conclusions?)$',
            r'^(references?|bibliography)$'
        ]
        
        lines = content.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            
            # Check if line is a section heading
            is_heading = False
            for pattern in section_patterns:
                if re.match(pattern, line_stripped.lower()):
                    # Save previous section
                    if current_content:
                        sections[current_section] = '\n'.join(current_content).strip()
                    
                    # Start new section
                    current_section = line_stripped.title()
                    current_content = []
                    is_heading = True
                    break
            
            # Also check for numbered headings (1. Introduction, 2. Methods, etc.)
            if not is_heading and re.match(r'^\d+\.?\s+[A-Z]', line_stripped):
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = re.sub(r'^\d+\.?\s+', '', line_stripped)
                current_content = []
                is_heading = True
            
            if not is_heading:
                current_content.append(line)
        
        # Save final section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # Remove empty sections
        sections = {k: v for k, v in sections.items() if v.strip()}
        
        return sections
