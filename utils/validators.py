"""
Input Validation Module
Validates user inputs and data formats
"""

import re
from utils.exceptions import ValidationError

def is_youtube_url(text: str) -> bool:
    """
    Validate if text is a YouTube URL
    
    Args:
        text: Text to validate
        
    Returns:
        True if valid YouTube URL, False otherwise
    """
    if not text or not isinstance(text, str):
        return False
    patterns = [
        r"(?:https?://)?(www\.)?youtu\.be/",
        r"(?:https?://)?(www\.)?youtube\.com/watch",
        r"(?:https?://)?(www\.)?youtube\.com/embed/",
    ]
    return any(re.search(pattern, text) for pattern in patterns)

def is_empty(text: str) -> bool:
    """
    Check if text is empty or whitespace only
    
    Args:
        text: Text to check
        
    Returns:
        True if empty or None, False otherwise
    """
    return text is None or (isinstance(text, str) and text.strip() == "")


def validate_question(question: str) -> bool:
    """
    Validate if text is a reasonable question
    Args:question: Question text
        
    Returns:True if valid, False otherwise
    """
    if not question or not isinstance(question, str):
        return False   
    question = question.strip()
    return len(question) >= 3

def validate_language(language: str) -> bool:
    """
    Validate language name
    
    Args:
        language: Language name
        
    Returns:
        True if valid, False otherwise
    """
    if not language or not isinstance(language, str):
        return False
    
    language = language.strip()
    return len(language) >= 2 and language.isalpha()