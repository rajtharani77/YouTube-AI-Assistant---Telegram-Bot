"""
Telegram Bot Initialization and Polling
Main entry point for the bot
"""

from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ConversationHandler,
)

from config.settings import Config
from utils.logger import logger
from utils.exceptions import ConfigurationError
from bot.handlers import handle_message
from bot.commands import (
    start_command,
    help_command,
    summary_command,
    clear_command,
)

def start_bot():
    """
    Initialize and start the Telegram bot
    """
    try:
        logger.info("Starting Telegram Bot...")
        if not Config.TELEGRAM_TOKEN:
            raise ConfigurationError("TELEGRAM_TOKEN not found in environment variables")
        logger.info(f"Configuration: {Config.to_dict()}")
        
        app = ApplicationBuilder().token(Config.TELEGRAM_TOKEN).build()
        logger.info("Registering command handlers...")
        
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("summary", summary_command))
        app.add_handler(CommandHandler("clear", clear_command))
        
        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        )
        
        logger.info("All handlers registered successfully")
        logger.info("Bot is running and ready to receive messages...")
        
        app.run_polling(drop_pending_updates=True)
        
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    try:
        start_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise