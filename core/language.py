"""
Language Module - Handles translation of summaries
"""

from services.llm_service import ask_llm
from core.prompts import TRANSLATE_PROMPT
from utils.logger import logger
from utils.exceptions import ModelError


def translate(text: str, language: str) -> str:
    """
    Translate text to specified language
    
    Args:
        text: Text to translate
        language: Target language name
        
    Returns:
        Translated text
        
    Raises:
        ModelError: If translation fails
    """
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        if not language or not isinstance(language, str):
            raise ValueError("Language must be a non-empty string")

        logger.info(f"Translating to {language}")     
        prompt = TRANSLATE_PROMPT.format(language=language, text=text)
        translated = ask_llm(prompt)
        logger.info(f"Translation to {language} completed")
        return translated
        
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        raise ModelError(str(e))
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise ModelError(f"Failed to translate to {language}: {str(e)}")