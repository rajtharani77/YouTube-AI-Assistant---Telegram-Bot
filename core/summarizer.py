"""
Summarizer Module - Generates concise summaries of transcripts
"""

from services.llm_service import ask_llm
from core.prompts import SUMMARY_PROMPT
from utils.helpers import safe_truncate
from utils.logger import logger
from utils.exceptions import ModelError


def generate_summary(text: str) -> str:
    """
    Generate a concise summary of the given text
    
    Args:
        text: Transcript text to summarize
        
    Returns:
        Summary string
        
    Raises:
        ModelError: If summarization fails
    """
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        
        logger.info("Starting summary generation")
        
        # Truncate to avoid token limits
        truncated_text = safe_truncate(text)
        
        prompt = SUMMARY_PROMPT.format(transcript=truncated_text)
        
        summary = ask_llm(prompt)
        
        logger.info(f"Summary generated successfully ({len(summary)} characters)")
        return summary
        
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        raise ModelError(str(e))
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        raise ModelError(f"Failed to generate summary: {str(e)}")