"""
Custom exception classes for the YouTube Telegram Bot
Provides specific error handling for different failure scenarios
"""


class BotException(Exception):
    """Base exception for all bot-related errors"""
    pass


class TranscriptError(BotException):
    """Raised when transcript fetching or parsing fails"""
    pass


class ModelError(BotException):
    """Raised when LLM API call fails"""
    pass


class ValidationError(BotException):
    """Raised when input validation fails"""
    pass


class ConfigurationError(BotException):
    """Raised when configuration is invalid or missing"""
    pass


class DatabaseError(BotException):
    """Raised when database operation fails"""
    pass


class RateLimitError(BotException):
    """Raised when user exceeds rate limit"""
    pass


class TimeoutError(BotException):
    """Raised when an operation exceeds timeout"""
    pass