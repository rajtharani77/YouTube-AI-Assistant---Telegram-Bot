"""
Q&A Engine - Answers questions about video content
"""

from services.llm_service import ask_llm
from core.prompts import QA_PROMPT
from utils.logger import logger
from utils.exceptions import ModelError


def answer_question(question: str, chunks: list) -> str:
    """
    Answer a question based on video transcript chunks
    Uses semantic search to find relevant context
    
    Args:
        question: User's question
        chunks: List of transcript chunks
        
    Returns:
        Answer based on transcript context
        
    Raises:
        ModelError: If QA fails
    """
    try:
        if not question or not isinstance(question, str):
            raise ValueError("Question must be a non-empty string")
        
        if not chunks or not isinstance(chunks, list):
            return "No transcript available. Please process a video first."
        
        logger.info(f"Answering question: {question[:50]}...")
        
        # Find most relevant chunk using keyword matching
        context = _find_relevant_chunk(question, chunks)
        
        if not context:
            logger.warning("No relevant context found for question")
            return "This topic is not covered in the video."
        
        # Generate answer using LLM
        prompt = QA_PROMPT.format(context=context, question=question)
        answer = ask_llm(prompt)
        
        logger.info("Question answered successfully")
        return answer
        
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        raise ModelError(str(e))
    except Exception as e:
        logger.error(f"QA failed: {e}")
        raise ModelError(f"Failed to answer question: {str(e)}")


def _find_relevant_chunk(question: str, chunks: list) -> str:
    """
    Find the most relevant chunk for a question
    Uses keyword matching - can be improved with embeddings
    
    Args:
        question: User question
        chunks: List of text chunks
        
    Returns:
        Most relevant chunk or None
    """
    keywords = question.lower().split()
    
    # Score chunks by keyword matches
    chunk_scores = []
    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for keyword in keywords if keyword in chunk_lower)
        chunk_scores.append((score, chunk))
    
    # Return chunk with highest score
    if chunk_scores:
        chunk_scores.sort(reverse=True, key=lambda x: x[0])
        return chunk_scores[0][1] if chunk_scores[0][0] > 0 else None
    
    return None