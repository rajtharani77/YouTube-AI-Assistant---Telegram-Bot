"""
Rate Limiting - Prevents abuse and manages request frequency
Student-friendly implementation using simple counter
"""

from datetime import datetime, timedelta
from config.settings import Config
from utils.logger import logger
from utils.exceptions import RateLimitError


class RateLimiter:
    """Simple rate limiter for per-user requests"""
    
    def __init__(self):
        self.user_requests = {}  
        self.max_requests = Config.MAX_REQUESTS_PER_MINUTE
        self.window_minutes = 1
    
    def is_allowed(self, user_id: int) -> bool:
        """
        Check if user is allowed to make a request
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if request is allowed, False otherwise
        """
        now = datetime.now()
        window_start = now - timedelta(minutes=self.window_minutes)
        user_id_str = str(user_id)
        if user_id_str not in self.user_requests:
            self.user_requests[user_id_str] = []
        
        self.user_requests[user_id_str] = [
            ts for ts in self.user_requests[user_id_str]
            if ts > window_start
        ]
        
        if len(self.user_requests[user_id_str]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for user {user_id}")
            return False
        self.user_requests[user_id_str].append(now)
        return True
    
    def get_remaining(self, user_id: int) -> int:
        """Get remaining requests for user"""
        user_id_str = str(user_id)
        requests = self.user_requests.get(user_id_str, [])
        remaining = max(0, self.max_requests - len(requests))
        return remaining

rate_limiter = RateLimiter()


def check_rate_limit(user_id: int) -> None:
    """
    Check if user has exceeded rate limit
    
    Raises:
        RateLimitError: If user exceeds limit
    """
    if not rate_limiter.is_allowed(user_id):
        remaining_time = int(Config.MAX_REQUESTS_PER_MINUTE / 60 * 30) or 1
        raise RateLimitError(
            f"Too many requests. Try again in {remaining_time} seconds."
        )
