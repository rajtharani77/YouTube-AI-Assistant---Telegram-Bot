"""
User session cache management with database persistence
Stores video processing results and user sessions
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from config.settings import Config
from utils.logger import logger
from utils.exceptions import DatabaseError


class SessionManager:
    """Manages user sessions with SQLite persistence"""
    
    def __init__(self):
        self.db_path = Config.DATABASE_URL.replace("sqlite:///./", "")
        self.in_memory_cache = {}  # Fallback in-memory cache
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database schema"""
        try:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        user_id INTEGER PRIMARY KEY,
                        summary TEXT,
                        chunks TEXT,
                        created_at TIMESTAMP,
                        updated_at TIMESTAMP,
                        expires_at TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            raise DatabaseError(f"Failed to initialize database: {e}")
    
    def save_user_data(self, user_id: int, data: dict):
        """
        Save user session data with expiration
        
        Args:
            user_id: Telegram user ID
            data: Dictionary containing summary and chunks
        """
        try:
            # Also keep in-memory copy for quick access
            self.in_memory_cache[user_id] = data
            
            # Persist to database
            expiration = datetime.now() + timedelta(hours=Config.TOKEN_EXPIRY_HOURS)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO user_sessions 
                    (user_id, summary, chunks, created_at, updated_at, expires_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    data.get("summary", ""),
                    json.dumps(data.get("chunks", [])),
                    datetime.now(),
                    datetime.now(),
                    expiration
                ))
                conn.commit()
            
            logger.info(f"Saved data for user {user_id}")
            
        except sqlite3.Error as e:
            logger.error(f"Failed to save user data: {e}")
            # Fall back to in-memory storage
            self.in_memory_cache[user_id] = data
    
    def get_user_data(self, user_id: int) -> dict:
        """
        Retrieve user session data
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Dictionary with user data or None if expired/not found
        """
        try:
            # Check in-memory first
            if user_id in self.in_memory_cache:
                return self.in_memory_cache[user_id]
            
            # Fetch from database
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM user_sessions 
                    WHERE user_id = ? AND expires_at > ?
                """, (user_id, datetime.now()))
                
                row = cursor.fetchone()
                if row:
                    data = {
                        "summary": row["summary"],
                        "chunks": json.loads(row["chunks"]),
                    }
                    # Cache in memory
                    self.in_memory_cache[user_id] = data
                    return data
            
            return None
            
        except sqlite3.Error as e:
            logger.error(f"Failed to retrieve user data: {e}")
            return self.in_memory_cache.get(user_id)
    
    def delete_user_data(self, user_id: int):
        """Delete user session data"""
        try:
            if user_id in self.in_memory_cache:
                del self.in_memory_cache[user_id]
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM user_sessions WHERE user_id = ?", (user_id,))
                conn.commit()
            
            logger.info(f"Deleted data for user {user_id}")
        except sqlite3.Error as e:
            logger.error(f"Failed to delete user data: {e}")
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM user_sessions WHERE expires_at < ?",
                    (datetime.now(),)
                )
                deleted = cursor.rowcount
                conn.commit()
            
            if deleted > 0:
                logger.info(f"Cleaned up {deleted} expired sessions")
        except sqlite3.Error as e:
            logger.error(f"Failed to cleanup expired sessions: {e}")


# Global session manager
session_manager = SessionManager()


# Backward compatibility functions
def save_user_data(user_id: int, data: dict):
    """Backward compatible save function"""
    session_manager.save_user_data(user_id, data)


def get_user_data(user_id: int) -> dict:
    """Backward compatible get function"""
    return session_manager.get_user_data(user_id)