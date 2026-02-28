"""
Logging Configuration Module
Centralized logging setup for the entire application
"""

import logging
import sys
from pathlib import Path
from config.settings import Config

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_format = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger("yt-bot")
logger.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))

file_handler = logging.FileHandler(log_dir / "bot.log")
file_handler.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))
file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))
console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info(f"Logging initialized - Level: {Config.LOG_LEVEL}")
logger.info(f"Log file: {log_dir / 'bot.log'}")