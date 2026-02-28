"""
Main Entry Point for YouTube Telegram Bot
Initializes and starts the bot with comprehensive error handling
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import Config
from utils.logger import logger
from utils.exceptions import ConfigurationError
from bot.telegram_bot import start_bot
def main():
    """
    Main function with initialization and error handling
    """
    try:
        logger.info("=" * 60)
        logger.info(" Starting YouTube Telegram Bot...")
        logger.info("=" * 60)
    
        logger.info("Validating configuration...")
        Config.validate()
        logger.info(" Configuration validated")
        
        logger.info("Setting up directories...")
        Path("logs").mkdir(exist_ok=True)
        Path("data").mkdir(exist_ok=True)
        logger.info(" Directories ready")
        
        logger.info("Starting bot")
        start_bot()
        
    except ConfigurationError as e:
        logger.error(f" Configuration Error: {e}", exc_info=True)
        print(f" Configuration Error:\n{e}\n")
        print("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info(" Bot stopped by user (Ctrl+C)")
        print("\n Bot stopped gracefully")
        sys.exit(0)
        
    except Exception as e:
        logger.critical(f" Fatal Error: {e}", exc_info=True)
        print(f" Fatal Error: {e}\n")
        print("Check logs/bot.log for more details")
        sys.exit(1)

if __name__ == "__main__":
    main()