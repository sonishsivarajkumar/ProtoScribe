import asyncio
from typing import Dict, List, Any, Optional
import json
import re

try:
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.prompts import PromptTemplate
except ImportError:
    OpenAI = None
    ChatOpenAI = None
    HumanMessage = None
    SystemMessage = None
    PromptTemplate = None

from ..core.config import settings


class LLMAnalyzer:
    """LLM-powered analysis for protocol improvement suggestions"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.DEFAULT_MODEL
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the LLM client"""
        if not self.api_key:
            return None
        
        if ChatOpenAI is None:
            return None
        
        try:
            return ChatOpenAI(
                openai_api_key=self.api_key,
                model_name=self.model,
                temperature=0.3
            )
        except Exception:
            return None
    
    async def generate_suggestions(
        self, 
        content: str, 
        sections: Dict[str, str] = None,
        missing_items: List[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Generate AI-powered suggestions for protocol improvement"""
        
        if self.llm is None:
            return self._get_fallback_suggestions()
        
        suggestions = []
        
        # Generate suggestions for missing items
        if missing_items:
            for item in missing_items:
                suggestion = await self._generate_item_suggestion(content, sections, item)
                if suggestion:
                    suggestions.append(suggestion)
        
        # Generate general improvement suggestions
        general_suggestions = await self._generate_general_suggestions(content, sections)
        suggestions.extend(general_suggestions)
        
        return suggestions
    
    async def _generate_item_suggestion(
        self, 
        content: str, 
        sections: Dict[str, str], 
        missing_item: Dict
    ) -> Optional[Dict[str, Any]]:
        """Generate suggestion for a specific missing item"""
        
        prompt = self._create_item_suggestion_prompt(missing_item, content)
        
        try:
            # Run LLM call in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self._call_llm, prompt)
            
            suggestion = self._parse_suggestion_response(response, missing_item)
            return suggestion
            
        except Exception as e:
            print(f"Error generating suggestion for item {missing_item.get('item_id', 'unknown')}: {str(e)}")
            return None
    
    async def _generate_general_suggestions(
        self, 
        content: str, 
        sections: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """Generate general improvement suggestions"""
        
        prompt = self._create_general_improvement_prompt(content)
        
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self._call_llm, prompt)
            
            suggestions = self._parse_general_suggestions_response(response)
            return suggestions
            
        except Exception as e:
            print(f"Error generating general suggestions: {str(e)}")
            return []
    
    def _create_item_suggestion_prompt(self, missing_item: Dict, content: str) -> str:
        """Create prompt for specific missing item"""
        
        return f"""
You are an expert in clinical trial protocol writing and regulatory guidelines (CONSORT/SPIRIT).

A clinical trial protocol is missing the following required element:

Item ID: {missing_item.get('item_id', 'Unknown')}
Guideline: {missing_item.get('guideline', 'Unknown')}
Section: {missing_item.get('section', 'Unknown')}
Description: {missing_item.get('description', 'Unknown')}

Current protocol content (first 2000 characters):
{content[:2000]}

Please provide:
1. A clear explanation of why this element is important
2. Suggested text that could be added to address this requirement
3. The specific section where this text should be placed
4. Confidence level (1-10) in your suggestion

Format your response as JSON:
{{
    "explanation": "Why this element is important...",
    "suggested_text": "Proposed text to add...",
    "target_section": "Section where this should be placed",
    "confidence": 8,
    "reasoning": "Explanation of the suggestion..."
}}
"""
    
    def _create_general_improvement_prompt(self, content: str) -> str:
        """Create prompt for general improvements"""
        
        return f"""
You are an expert in clinical trial protocol writing and regulatory guidelines (CONSORT/SPIRIT).

Please review this clinical trial protocol excerpt and suggest 3-5 specific improvements:

Protocol content (first 3000 characters):
{content[:3000]}

Focus on:
- Clarity and specificity of language
- Completeness of key elements
- Adherence to best practices
- Areas that could be more detailed or explicit

Format your response as JSON array:
[
    {{
        "type": "clarity|completeness|specificity|best_practice",
        "section": "Target section name",
        "issue": "Description of the issue",
        "suggestion": "Specific improvement suggestion",
        "confidence": 7
    }}
]
"""
    
    def _call_llm(self, prompt: str) -> str:
        """Call the LLM with the given prompt"""
        if self.llm is None:
            return ""
        
        messages = [
            SystemMessage(content="You are an expert clinical trial protocol reviewer."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm(messages)
        return response.content if hasattr(response, 'content') else str(response)
    
    def _parse_suggestion_response(self, response: str, missing_item: Dict) -> Dict[str, Any]:
        """Parse LLM response for item suggestion"""
        
        try:
            # Try to parse as JSON
            data = json.loads(response)
            
            return {
                "item_id": missing_item.get("item_id", "unknown"),
                "type": "missing_item",
                "section": data.get("target_section", missing_item.get("section", "")),
                "issue": f"Missing required element: {missing_item.get('description', '')}",
                "explanation": data.get("explanation", ""),
                "suggested_text": data.get("suggested_text", ""),
                "confidence": data.get("confidence", 5) / 10.0,  # Normalize to 0-1
                "reasoning": data.get("reasoning", ""),
                "guideline": missing_item.get("guideline", "")
            }
            
        except json.JSONDecodeError:
            # Fallback parsing
            return {
                "item_id": missing_item.get("item_id", "unknown"),
                "type": "missing_item",
                "section": missing_item.get("section", ""),
                "issue": f"Missing required element: {missing_item.get('description', '')}",
                "explanation": "AI-generated suggestion",
                "suggested_text": response[:500] if response else "No suggestion available",
                "confidence": 0.5,
                "reasoning": "Fallback suggestion due to parsing error",
                "guideline": missing_item.get("guideline", "")
            }
    
    def _parse_general_suggestions_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response for general suggestions"""
        
        try:
            # Try to parse as JSON array
            data = json.loads(response)
            
            suggestions = []
            for item in data:
                suggestions.append({
                    "item_id": f"general_{len(suggestions) + 1}",
                    "type": item.get("type", "general"),
                    "section": item.get("section", "General"),
                    "issue": item.get("issue", ""),
                    "explanation": item.get("issue", ""),
                    "suggested_text": item.get("suggestion", ""),
                    "confidence": item.get("confidence", 5) / 10.0,
                    "reasoning": item.get("suggestion", ""),
                    "guideline": "General"
                })
            
            return suggestions
            
        except json.JSONDecodeError:
            # Try to extract suggestions from text
            return self._extract_suggestions_from_text(response)
    
    def _extract_suggestions_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract suggestions from unstructured text"""
        
        suggestions = []
        
        # Look for numbered points or bullet points
        patterns = [
            r'(\d+)\.\s*(.+?)(?=\n\d+\.|\n\n|\Z)',
            r'[-\*]\s*(.+?)(?=\n[-\*]|\n\n|\Z)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for i, match in enumerate(matches):
                if isinstance(match, tuple):
                    content = match[1] if len(match) > 1 else match[0]
                else:
                    content = match
                
                suggestions.append({
                    "item_id": f"extracted_{i + 1}",
                    "type": "general",
                    "section": "General",
                    "issue": "General improvement opportunity",
                    "explanation": content.strip()[:200],
                    "suggested_text": content.strip(),
                    "confidence": 0.6,
                    "reasoning": "Extracted from LLM response",
                    "guideline": "General"
                })
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _get_fallback_suggestions(self) -> List[Dict[str, Any]]:
        """Provide fallback suggestions when LLM is not available"""
        
        return [
            {
                "item_id": "fallback_1",
                "type": "general",
                "section": "General",
                "issue": "LLM service unavailable",
                "explanation": "AI suggestions are currently unavailable. Please ensure your API key is configured.",
                "suggested_text": "Review protocol against CONSORT/SPIRIT guidelines manually.",
                "confidence": 0.1,
                "reasoning": "Fallback suggestion - LLM not available",
                "guideline": "General"
            }
        ]
