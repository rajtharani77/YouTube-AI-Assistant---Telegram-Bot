"""
Helper Functions
General utility functions
"""

from utils.logger import logger
def safe_truncate(text: str, limit: int = 12000) -> str:
    """
    Safely truncate text to specified character limit
    
    Args:
        text: Text to truncate
        limit: Maximum characters
        
    Returns:
        Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= limit:
        return text

    truncated = text[:limit]
    logger.warning(f"Text truncated from {len(text)} to {limit} characters")
    return truncated + "\n\n[... truncated ...]"
def format_list(items: list) -> str:
    """
    Format list items with numbering
    
    Args:
        items: List of items to format
        
    Returns:
        Formatted string
    """
    if not items or not isinstance(items, list):
        return ""
    
    return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])
def chunk_by_sentences(text: str, max_length: int = 500) -> list:
    """
    Split text by sentences rather than just words
    Useful for better context preservation
    
    Args:
        text: Text to split
        max_length: Max characters per chunk
        
    Returns:
        List of text chunks
    """
    if not text:
        return []
    
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks