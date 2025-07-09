"""
Enhanced LLM service with support for multiple providers and advanced analysis
"""
import asyncio
import json
import re
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from enum import Enum

try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None

from ..core.config import settings


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    async def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate text completion"""
        pass
    
    @abstractmethod
    async def generate_chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate chat completion"""
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI client implementation"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        if not openai:
            raise ImportError("OpenAI package not installed")
        
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate text completion using OpenAI"""
        try:
            response = await self.client.completions.create(
                model=self.model if "gpt-3.5" in self.model else "gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=kwargs.get("max_tokens", settings.LLM_MAX_TOKENS),
                temperature=kwargs.get("temperature", settings.LLM_TEMPERATURE),
                timeout=settings.LLM_TIMEOUT
            )
            return response.choices[0].text.strip()
        except Exception as e:
            raise Exception(f"OpenAI completion error: {str(e)}")
    
    async def generate_chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate chat completion using OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=kwargs.get("max_tokens", settings.LLM_MAX_TOKENS),
                temperature=kwargs.get("temperature", settings.LLM_TEMPERATURE),
                timeout=settings.LLM_TIMEOUT
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI chat completion error: {str(e)}")


class AnthropicClient(BaseLLMClient):
    """Anthropic client implementation"""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        if not anthropic:
            raise ImportError("Anthropic package not installed")
        
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model
    
    async def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate text completion using Anthropic"""
        messages = [{"role": "user", "content": prompt}]
        return await self.generate_chat_completion(messages, **kwargs)
    
    async def generate_chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate chat completion using Anthropic"""
        try:
            response = await self.client.messages.create(
                model=self.model,
                messages=messages,
                max_tokens=kwargs.get("max_tokens", settings.LLM_MAX_TOKENS),
                temperature=kwargs.get("temperature", settings.LLM_TEMPERATURE),
                timeout=settings.LLM_TIMEOUT
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise Exception(f"Anthropic completion error: {str(e)}")


class AdvancedLLMAnalyzer:
    """Advanced LLM analyzer with multiple providers and enhanced capabilities"""
    
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or settings.DEFAULT_LLM_PROVIDER
        self.client = self._initialize_client()
    
    def _initialize_client(self) -> Optional[BaseLLMClient]:
        """Initialize the appropriate LLM client"""
        try:
            if self.provider == LLMProvider.OPENAI.value:
                if settings.OPENAI_API_KEY:
                    return OpenAIClient(settings.OPENAI_API_KEY, settings.DEFAULT_MODEL)
            elif self.provider == LLMProvider.ANTHROPIC.value:
                if settings.ANTHROPIC_API_KEY:
                    return AnthropicClient(settings.ANTHROPIC_API_KEY)
            return None
        except Exception as e:
            print(f"Failed to initialize LLM client: {e}")
            return None
    
    async def analyze_protocol_comprehensive(
        self,
        content: str,
        sections: Dict[str, str],
        missing_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Comprehensive protocol analysis"""
        
        if not self.client:
            return self._get_fallback_analysis()
        
        # Run multiple analysis tasks in parallel
        tasks = [
            self._analyze_missing_items(content, sections, missing_items),
            self._analyze_clarity_and_completeness(content, sections),
            self._analyze_consistency(content, sections),
            self._generate_executive_summary(content, sections)
        ]
        
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                "missing_items_analysis": results[0] if not isinstance(results[0], Exception) else [],
                "clarity_analysis": results[1] if not isinstance(results[1], Exception) else [],
                "consistency_analysis": results[2] if not isinstance(results[2], Exception) else [],
                "executive_summary": results[3] if not isinstance(results[3], Exception) else "",
                "provider": self.provider,
                "analysis_timestamp": "2025-01-08T10:00:00Z"  # Replace with actual timestamp
            }
        except Exception as e:
            print(f"Comprehensive analysis failed: {e}")
            return self._get_fallback_analysis()
    
    async def _analyze_missing_items(
        self,
        content: str,
        sections: Dict[str, str],
        missing_items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze and provide suggestions for missing items"""
        
        suggestions = []
        
        for item in missing_items[:5]:  # Limit to 5 items to avoid rate limits
            try:
                suggestion = await self._generate_item_suggestion(content, sections, item)
                if suggestion:
                    suggestions.append(suggestion)
            except Exception as e:
                print(f"Error analyzing item {item.get('item_id', 'unknown')}: {e}")
                continue
        
        return suggestions
    
    async def _analyze_clarity_and_completeness(
        self,
        content: str,
        sections: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """Analyze protocol for clarity and completeness issues"""
        
        prompt = self._create_clarity_analysis_prompt(content, sections)
        
        try:
            response = await self.client.generate_chat_completion([
                {"role": "system", "content": "You are an expert clinical trial protocol reviewer."},
                {"role": "user", "content": prompt}
            ])
            
            return self._parse_clarity_analysis(response)
        except Exception as e:
            print(f"Clarity analysis failed: {e}")
            return []
    
    async def _analyze_consistency(
        self,
        content: str,
        sections: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """Check for internal consistency issues"""
        
        prompt = self._create_consistency_check_prompt(content, sections)
        
        try:
            response = await self.client.generate_chat_completion([
                {"role": "system", "content": "You are an expert at identifying inconsistencies in clinical trial protocols."},
                {"role": "user", "content": prompt}
            ])
            
            return self._parse_consistency_analysis(response)
        except Exception as e:
            print(f"Consistency analysis failed: {e}")
            return []
    
    async def _generate_executive_summary(
        self,
        content: str,
        sections: Dict[str, str]
    ) -> str:
        """Generate an executive summary of the protocol quality"""
        
        prompt = f"""
        Analyze this clinical trial protocol and provide a concise executive summary of its overall quality and readiness.

        Protocol content (first 2000 chars): {content[:2000]}

        Provide a 2-3 paragraph executive summary covering:
        1. Overall protocol quality assessment
        2. Key strengths and major weaknesses
        3. Priority recommendations for improvement
        4. Estimated readiness level for regulatory submission

        Keep the response professional and actionable.
        """
        
        try:
            response = await self.client.generate_chat_completion([
                {"role": "system", "content": "You are a senior clinical research expert providing executive-level protocol assessments."},
                {"role": "user", "content": prompt}
            ])
            
            return response
        except Exception as e:
            print(f"Executive summary generation failed: {e}")
            return "Executive summary could not be generated due to technical issues."
    
    async def _generate_item_suggestion(
        self,
        content: str,
        sections: Dict[str, str],
        missing_item: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Generate detailed suggestion for a missing item"""
        
        prompt = f"""
        You are an expert clinical trial protocol writer. A protocol is missing this required element:

        Item: {missing_item.get('item_id', 'Unknown')} - {missing_item.get('description', '')}
        Guideline: {missing_item.get('guideline', '')}
        Section: {missing_item.get('section', '')}

        Context from protocol: {content[:1500]}

        Provide a JSON response with:
        {{
            "suggested_text": "Specific text to add that addresses this requirement",
            "placement_guidance": "Where in the protocol this should be placed",
            "explanation": "Why this element is important and how it improves the protocol",
            "confidence": 0.8,
            "alternative_approaches": ["Alternative way 1", "Alternative way 2"],
            "regulatory_context": "How this relates to regulatory requirements"
        }}
        """
        
        try:
            response = await self.client.generate_chat_completion([
                {"role": "system", "content": "You are an expert clinical trial protocol writer and regulatory affairs specialist."},
                {"role": "user", "content": prompt}
            ])
            
            # Parse JSON response
            suggestion_data = json.loads(response)
            
            return {
                "item_id": missing_item.get("item_id", "unknown"),
                "type": "missing_item",
                "section": missing_item.get("section", ""),
                "issue": f"Missing: {missing_item.get('description', '')}",
                "suggested_text": suggestion_data.get("suggested_text", ""),
                "placement_guidance": suggestion_data.get("placement_guidance", ""),
                "explanation": suggestion_data.get("explanation", ""),
                "confidence": suggestion_data.get("confidence", 0.5),
                "alternative_approaches": suggestion_data.get("alternative_approaches", []),
                "regulatory_context": suggestion_data.get("regulatory_context", ""),
                "guideline": missing_item.get("guideline", "")
            }
            
        except json.JSONDecodeError:
            # Fallback parsing for non-JSON responses
            return self._parse_non_json_suggestion(response, missing_item)
        except Exception as e:
            print(f"Error generating suggestion for {missing_item.get('item_id', 'unknown')}: {e}")
            return None
    
    def _create_clarity_analysis_prompt(self, content: str, sections: Dict[str, str]) -> str:
        """Create prompt for clarity analysis"""
        return f"""
        Analyze this clinical trial protocol for clarity and completeness issues.

        Protocol sections:
        {json.dumps({k: v[:300] + "..." if len(v) > 300 else v for k, v in sections.items()}, indent=2)}

        Identify 3-5 specific areas where the protocol could be clearer or more complete. For each issue, provide:
        1. The specific problem
        2. The impact on protocol quality
        3. A concrete suggestion for improvement

        Format as JSON array:
        [
            {{
                "issue_type": "clarity|completeness|specificity",
                "section": "section name",
                "problem": "specific issue description",
                "impact": "how this affects the protocol",
                "suggestion": "concrete improvement recommendation",
                "priority": "high|medium|low"
            }}
        ]
        """
    
    def _create_consistency_check_prompt(self, content: str, sections: Dict[str, str]) -> str:
        """Create prompt for consistency analysis"""
        return f"""
        Check this clinical trial protocol for internal consistency issues.

        Look for conflicts between:
        - Primary/secondary endpoints and outcome measures
        - Sample size calculations and stated objectives
        - Inclusion/exclusion criteria and study population
        - Timeline and procedure descriptions
        - Statistical methods and study design

        Protocol sections:
        {json.dumps({k: v[:300] + "..." if len(v) > 300 else v for k, v in sections.items()}, indent=2)}

        Return findings as JSON array:
        [
            {{
                "consistency_issue": "description of the conflict",
                "affected_sections": ["section1", "section2"],
                "severity": "high|medium|low",
                "recommendation": "how to resolve the inconsistency"
            }}
        ]
        """
    
    def _parse_clarity_analysis(self, response: str) -> List[Dict[str, Any]]:
        """Parse clarity analysis response"""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Extract structured data from text response
            return self._extract_analysis_from_text(response, "clarity")
    
    def _parse_consistency_analysis(self, response: str) -> List[Dict[str, Any]]:
        """Parse consistency analysis response"""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return self._extract_analysis_from_text(response, "consistency")
    
    def _extract_analysis_from_text(self, text: str, analysis_type: str) -> List[Dict[str, Any]]:
        """Extract analysis points from unstructured text"""
        issues = []
        
        # Look for numbered points or bullet points
        patterns = [
            r'(\d+)\.\s*(.+?)(?=\n\d+\.|\n\n|\Z)',
            r'[-\*]\s*(.+?)(?=\n[-\*]|\n\n|\Z)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for i, match in enumerate(matches):
                content = match[1] if len(match) > 1 else match[0]
                issues.append({
                    "issue_type": analysis_type,
                    "section": "General",
                    "problem": content.strip()[:200],
                    "impact": "Affects protocol quality",
                    "suggestion": "Review and revise as needed",
                    "priority": "medium"
                })
        
        return issues[:5]  # Limit to 5 issues
    
    def _parse_non_json_suggestion(self, response: str, missing_item: Dict[str, Any]) -> Dict[str, Any]:
        """Parse non-JSON suggestion response"""
        return {
            "item_id": missing_item.get("item_id", "unknown"),
            "type": "missing_item",
            "section": missing_item.get("section", ""),
            "issue": f"Missing: {missing_item.get('description', '')}",
            "suggested_text": response[:500] if response else "No suggestion available",
            "explanation": "AI-generated suggestion",
            "confidence": 0.6,
            "guideline": missing_item.get("guideline", "")
        }
    
    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Provide fallback analysis when LLM is unavailable"""
        return {
            "missing_items_analysis": [],
            "clarity_analysis": [{
                "issue_type": "system",
                "section": "General",
                "problem": "AI analysis unavailable",
                "impact": "Manual review required",
                "suggestion": "Configure API keys for AI-powered analysis",
                "priority": "low"
            }],
            "consistency_analysis": [],
            "executive_summary": "AI analysis is currently unavailable. Please ensure your API keys are properly configured for enhanced analysis capabilities.",
            "provider": "fallback",
            "analysis_timestamp": "2025-01-08T10:00:00Z"
        }
