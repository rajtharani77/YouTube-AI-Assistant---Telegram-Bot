"""
Logging Configuration Module
Centralized logging setup for the entire application
"""

import logging
import sys
from pathlib import Path
from config.settings import Config

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging format
log_format = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# Create logger
logger = logging.getLogger("yt-bot")
logger.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))

# File handler - logs to file
file_handler = logging.FileHandler(log_dir / "bot.log")
file_handler.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))
file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

# Console handler - logs to terminal
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))
console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info(f"Logging initialized - Level: {Config.LOG_LEVEL}")
logger.info(f"Log file: {log_dir / 'bot.log'}")