"""
Text Chunking Module - Splits transcripts into manageable pieces
"""

from utils.logger import logger


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list:
    """
    Split text into overlapping chunks for better context in QA
    
    Args:
        text: Text to chunk
        chunk_size: Number of words per chunk
        overlap: Number of words to overlap between chunks
        
    Returns:
        List of text chunks
    """
    try:
        if not text or not isinstance(text, str):
            logger.warning("Empty text provided for chunking")
            return []
        
        words = text.split()
        
        if len(words) < chunk_size:
            logger.info(f"Text is smaller than chunk size ({len(words)} words)")
            return [text]
        
        chunks = []
        step = chunk_size - overlap
        
        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        logger.info(f"Chunked text into {len(chunks)} segments")
        return chunks
        
    except Exception as e:
        logger.error(f"Chunking failed: {e}")
        return [text]  