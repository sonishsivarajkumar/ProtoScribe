import re
from typing import List, Dict, Any
from pathlib import Path


def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might interfere with processing
    text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
    
    return text.strip()


def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text"""
    if not text:
        return []
    
    # Simple keyword extraction (you might want to use more sophisticated NLP)
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    
    # Filter out common stop words
    stop_words = {
        'this', 'that', 'with', 'have', 'will', 'been', 'were', 'they', 'them',
        'from', 'into', 'would', 'could', 'should', 'about', 'other', 'which',
        'their', 'there', 'where', 'when', 'what', 'then', 'than', 'some',
        'more', 'very', 'also', 'each', 'such', 'only', 'many', 'most'
    }
    
    keywords = [word for word in words if word not in stop_words]
    
    # Return unique keywords
    return list(set(keywords))


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def validate_file_type(filename: str, allowed_types: List[str]) -> bool:
    """Validate if file type is allowed"""
    if not filename:
        return False
    
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_types


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to specified length"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def calculate_completeness_score(total_items: int, passed_items: int) -> float:
    """Calculate completeness score as percentage"""
    if total_items == 0:
        return 0.0
    
    return round((passed_items / total_items) * 100, 1)


def normalize_section_name(section_name: str) -> str:
    """Normalize section names for consistent matching"""
    if not section_name:
        return ""
    
    # Convert to lowercase and remove extra spaces
    normalized = re.sub(r'\s+', ' ', section_name.lower().strip())
    
    # Remove common prefixes/suffixes
    normalized = re.sub(r'^\d+\.?\s*', '', normalized)  # Remove numbering
    normalized = re.sub(r'\s*\([^)]*\)\s*', '', normalized)  # Remove parenthetical content
    
    return normalized


def extract_sentences(text: str) -> List[str]:
    """Extract sentences from text"""
    if not text:
        return []
    
    # Simple sentence splitting (you might want to use spaCy for better results)
    sentences = re.split(r'[.!?]+', text)
    
    # Clean and filter sentences
    cleaned_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 10:  # Filter out very short sentences
            cleaned_sentences.append(sentence)
    
    return cleaned_sentences


def find_similar_text(needle: str, haystack: str, min_similarity: float = 0.3) -> Dict[str, Any]:
    """Find similar text in a larger text body"""
    if not needle or not haystack:
        return {"found": False, "similarity": 0.0, "text": ""}
    
    needle_words = set(needle.lower().split())
    sentences = extract_sentences(haystack)
    
    best_match = {"found": False, "similarity": 0.0, "text": ""}
    
    for sentence in sentences:
        sentence_words = set(sentence.lower().split())
        
        if needle_words and sentence_words:
            # Calculate Jaccard similarity
            intersection = len(needle_words.intersection(sentence_words))
            union = len(needle_words.union(sentence_words))
            similarity = intersection / union if union > 0 else 0.0
            
            if similarity >= min_similarity and similarity > best_match["similarity"]:
                best_match = {
                    "found": True,
                    "similarity": similarity,
                    "text": sentence
                }
    
    return best_match
