"""
LLM Service - Handles calls to AI models (Google Gemini or OpenAI)
Supports multiple providers with fallback mechanisms
"""

import google.generativeai as genai
from config.settings import Config
from utils.logger import logger
from utils.exceptions import ModelError, ConfigurationError

def _init_llm():
    """Initialize LLM provider based on configuration"""
    try:
        if Config.LLM_PROVIDER == "google":
            if not Config.GOOGLE_API_KEY:
                raise ConfigurationError("Google API key not configured")
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            logger.info(f"Using Google Gemini API - Model: {Config.MODEL_NAME}")
            return genai.GenerativeModel(Config.MODEL_NAME)
        else:
            raise ConfigurationError(f"Unsupported LLM provider: {Config.LLM_PROVIDER}")
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise


model = _init_llm()


def ask_llm(prompt: str, temperature: float = 0.3, max_tokens: int = 2048) -> str:
    """
    Query the LLM with a prompt
    
    Args:
        prompt: The prompt to send to the model
        temperature: Controls randomness (0.0-1.0)
        max_tokens: Maximum response length
        
    Returns:
        The model's response text
        
    Raises:
        ModelError: If the API call fails
    """
    try:
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string")
        
        logger.info("Sending prompt to LLM")
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": min(max(temperature, 0.0), 1.0),  # Clamp between 0-1
                "max_output_tokens": max_tokens
            }
        )
        
        if not response.text:
            raise ModelError("Empty response from model")
        
        logger.info("Successfully received response from LLM")
        return response.text
        
    except AttributeError as e:
        logger.error(f"API configuration error: {e}")
        raise ModelError("LLM API is not properly configured")
    except Exception as e:
        logger.error(f"LLM API error: {e}")
        raise ModelError(f"Failed to get response from LLM: {str(e)}")