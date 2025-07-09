import re
import json
import os
from typing import Dict, List, Any
from pathlib import Path

from ..core.config import settings


class ComplianceChecker:
    """Check protocol compliance against CONSORT/SPIRIT guidelines"""
    
    def __init__(self):
        self.consort_guidelines = self._load_guidelines("consort")
        self.spirit_guidelines = self._load_guidelines("spirit")
    
    def _load_guidelines(self, guideline_type: str) -> Dict[str, Any]:
        """Load guidelines from JSON file"""
        guidelines_path = Path(settings.GUIDELINES_DIR) / f"{guideline_type}.json"
        
        if guidelines_path.exists():
            with open(guidelines_path, 'r') as f:
                return json.load(f)
        else:
            # Return default guidelines if file doesn't exist
            if guideline_type == "consort":
                return self._get_default_consort()
            elif guideline_type == "spirit":
                return self._get_default_spirit()
        
        return {"items": []}
    
    async def check_compliance(self, content: str, sections: Dict[str, str] = None) -> Dict[str, Any]:
        """Check compliance against both CONSORT and SPIRIT guidelines"""
        
        if sections is None:
            sections = {"content": content}
        
        consort_results = await self._check_guideline_compliance(
            content, sections, self.consort_guidelines, "CONSORT"
        )
        
        spirit_results = await self._check_guideline_compliance(
            content, sections, self.spirit_guidelines, "SPIRIT"
        )
        
        # Calculate overall score
        total_items = len(consort_results["items"]) + len(spirit_results["items"])
        passed_items = len([item for item in consort_results["items"] if item["status"] == "pass"]) + \
                      len([item for item in spirit_results["items"] if item["status"] == "pass"])
        
        overall_score = (passed_items / total_items * 100) if total_items > 0 else 0
        
        return {
            "score": round(overall_score, 1),
            "consort_score": consort_results["score"],
            "spirit_score": spirit_results["score"],
            "total_items": total_items,
            "passed_items": passed_items,
            "failed_items": consort_results["failed_items"] + spirit_results["failed_items"],
            "warnings": consort_results["warnings"] + spirit_results["warnings"],
            "consort_details": consort_results,
            "spirit_details": spirit_results
        }
    
    async def _check_guideline_compliance(
        self, 
        content: str, 
        sections: Dict[str, str], 
        guidelines: Dict[str, Any], 
        guideline_type: str
    ) -> Dict[str, Any]:
        """Check compliance against a specific guideline"""
        
        results = []
        failed_items = []
        warnings = []
        
        for item in guidelines.get("items", []):
            check_result = self._check_item(content, sections, item)
            results.append(check_result)
            
            if check_result["status"] == "fail":
                failed_items.append({
                    "item_id": item["id"],
                    "description": item["description"],
                    "section": item.get("section", ""),
                    "guideline": guideline_type
                })
            elif check_result["status"] == "warning":
                warnings.append({
                    "item_id": item["id"],
                    "description": item["description"],
                    "issue": check_result.get("issue", ""),
                    "guideline": guideline_type
                })
        
        passed_count = len([r for r in results if r["status"] == "pass"])
        score = (passed_count / len(results) * 100) if results else 0
        
        return {
            "guideline": guideline_type,
            "score": round(score, 1),
            "items": results,
            "failed_items": failed_items,
            "warnings": warnings
        }
    
    def _check_item(self, content: str, sections: Dict[str, str], item: Dict[str, Any]) -> Dict[str, Any]:
        """Check a specific guideline item"""
        
        item_id = item["id"]
        description = item["description"]
        section_hint = item.get("section", "").lower()
        
        # Keywords to look for based on the item description
        keywords = self._extract_keywords(description)
        
        # Look in relevant sections first
        relevant_sections = self._find_relevant_sections(sections, section_hint)
        
        found_text = None
        confidence = 0.0
        
        # Check relevant sections
        for section_name, section_content in relevant_sections.items():
            result = self._search_for_keywords(section_content, keywords)
            if result["found"]:
                found_text = result["text"]
                confidence = result["confidence"]
                break
        
        # If not found in relevant sections, check entire content
        if not found_text:
            result = self._search_for_keywords(content, keywords)
            if result["found"]:
                found_text = result["text"]
                confidence = result["confidence"] * 0.7  # Lower confidence for general search
        
        # Determine status
        if confidence >= 0.8:
            status = "pass"
        elif confidence >= 0.4:
            status = "warning"
            issue = "Item may be present but could be more explicit"
        else:
            status = "fail"
            issue = "Item not found or not adequately addressed"
        
        return {
            "item_id": item_id,
            "description": description,
            "status": status,
            "confidence": confidence,
            "found_text": found_text[:200] + "..." if found_text and len(found_text) > 200 else found_text,
            "issue": issue if status != "pass" else None
        }
    
    def _extract_keywords(self, description: str) -> List[str]:
        """Extract keywords from item description"""
        
        # Common keyword patterns for different types of items
        keyword_patterns = {
            r'randomis?ed|randomization': ['random', 'randomized', 'randomisation'],
            r'blind|blinding|masking': ['blind', 'blinding', 'masked', 'masking'],
            r'sample size|power': ['sample size', 'power', 'participants', 'subjects'],
            r'primary outcome|endpoint': ['primary outcome', 'primary endpoint', 'main outcome'],
            r'secondary outcome': ['secondary outcome', 'secondary endpoint'],
            r'inclusion criteria|eligibility': ['inclusion', 'eligible', 'eligibility criteria'],
            r'exclusion criteria': ['exclusion', 'excluded'],
            r'statistical analysis': ['statistical', 'analysis', 'statistics'],
            r'adverse events?': ['adverse', 'side effect', 'safety'],
            r'consent|informed consent': ['consent', 'informed consent'],
            r'ethics|ethical': ['ethics', 'ethical', 'IRB', 'ethics committee']
        }
        
        keywords = []
        description_lower = description.lower()
        
        for pattern, words in keyword_patterns.items():
            if re.search(pattern, description_lower):
                keywords.extend(words)
        
        # Add words from the description itself
        important_words = re.findall(r'\b[a-zA-Z]{4,}\b', description_lower)
        keywords.extend([word for word in important_words if word not in ['with', 'that', 'this', 'they', 'were', 'been']])
        
        return list(set(keywords))
    
    def _find_relevant_sections(self, sections: Dict[str, str], section_hint: str) -> Dict[str, str]:
        """Find sections relevant to the guideline item"""
        
        relevant = {}
        
        # Direct match
        for section_name, content in sections.items():
            if section_hint in section_name.lower():
                relevant[section_name] = content
        
        # Pattern matching for common section types
        section_patterns = {
            'method': ['method', 'design', 'procedure'],
            'participant': ['participant', 'subject', 'population', 'eligibility'],
            'outcome': ['outcome', 'endpoint', 'measure'],
            'statistical': ['statistical', 'analysis', 'sample'],
            'abstract': ['abstract', 'summary'],
            'introduction': ['introduction', 'background'],
            'ethics': ['ethics', 'ethical', 'consent']
        }
        
        for pattern_key, patterns in section_patterns.items():
            if any(p in section_hint for p in patterns):
                for section_name, content in sections.items():
                    if any(p in section_name.lower() for p in patterns):
                        relevant[section_name] = content
        
        return relevant if relevant else sections
    
    def _search_for_keywords(self, text: str, keywords: List[str]) -> Dict[str, Any]:
        """Search for keywords in text"""
        
        text_lower = text.lower()
        found_keywords = []
        found_text = None
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
                
                # Extract surrounding context
                if not found_text:
                    start_idx = text_lower.find(keyword.lower())
                    start = max(0, start_idx - 100)
                    end = min(len(text), start_idx + len(keyword) + 100)
                    found_text = text[start:end].strip()
        
        confidence = len(found_keywords) / len(keywords) if keywords else 0
        
        return {
            "found": len(found_keywords) > 0,
            "confidence": confidence,
            "text": found_text,
            "keywords_found": found_keywords
        }
    
    def _get_default_consort(self) -> Dict[str, Any]:
        """Default CONSORT guidelines"""
        return {
            "items": [
                {
                    "id": "1a",
                    "section": "Title and abstract",
                    "description": "Identification as a randomised trial in the title"
                },
                {
                    "id": "1b",
                    "section": "Title and abstract", 
                    "description": "Structured summary of trial design, methods, results, and conclusions"
                },
                {
                    "id": "2a",
                    "section": "Introduction",
                    "description": "Scientific background and explanation of rationale"
                },
                {
                    "id": "2b",
                    "section": "Introduction",
                    "description": "Specific objectives or hypotheses"
                }
            ]
        }
    
    def _get_default_spirit(self) -> Dict[str, Any]:
        """Default SPIRIT guidelines"""
        return {
            "items": [
                {
                    "id": "1",
                    "section": "Administrative information",
                    "description": "Descriptive title identifying the study design, population, interventions"
                },
                {
                    "id": "2a",
                    "section": "Administrative information",
                    "description": "Trial identifier and registry name"
                },
                {
                    "id": "3",
                    "section": "Administrative information",
                    "description": "Protocol version and date"
                }
            ]
        }
