"""
Configuration management for the YouTube Telegram Bot
Loads and validates all environment variables
"""

import os
from dotenv import load_dotenv
from utils.exceptions import ConfigurationError

load_dotenv()


class Config:
    """Centralized configuration class"""
    
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google").lower()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
    
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/bot.db")
    
    TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", "24"))
    MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "30"))
    
    @classmethod
    def validate(cls):
        """
        Validate all required configuration variables
        Raises ConfigurationError if any critical setting is missing
        """
        errors = []
        if not cls.TELEGRAM_TOKEN:
            errors.append("TELEGRAM_TOKEN is required")
        
        if cls.LLM_PROVIDER == "google":
            if not cls.GOOGLE_API_KEY:
                errors.append("GOOGLE_API_KEY is required when using Google provider")
        elif cls.LLM_PROVIDER == "openai":
            if not cls.OPENAI_API_KEY:
                errors.append("OPENAI_API_KEY is required when using OpenAI provider")
        else:
            errors.append(f"Invalid LLM_PROVIDER: {cls.LLM_PROVIDER}")
        
        if errors:
            error_message = "\n".join(errors)
            raise ConfigurationError(
                f"Configuration validation failed:\n{error_message}\n"
                "Please check your .env file"
            )
    
    @classmethod
    def to_dict(cls):
        """Return configuration as dictionary (exclude sensitive data)"""
        return {
            "llm_provider": cls.LLM_PROVIDER,
            "model_name": cls.MODEL_NAME,
            "log_level": cls.LOG_LEVEL,
            "database_url": cls.DATABASE_URL,
            "request_timeout": cls.REQUEST_TIMEOUT,
        }


try:
    Config.validate()
except ConfigurationError as e:
    print(f" Configuration Error: {e}")
    raise