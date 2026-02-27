"""
Telegram Bot Commands - /start, /help, /summary, etc.
"""

from telegram import Update
from telegram.ext import ContextTypes
from services.cache import get_user_data
from utils.logger import logger


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start command - Welcome message
    """
    try:
        user = update.message.from_user
        logger.info(f"User {user.username} ({user.id}) started the bot")
        
        message = """👋 **Welcome to YouTube AI Assistant!**

I can:
✅ Summarize YouTube videos
✅ Answer questions about video content
✅ Translate summaries to other languages

**How to use:**
1️⃣ Send a YouTube link
2️⃣ Wait for the summary
3️⃣ Ask questions or translate

**Available Commands:**
/help - Detailed guide
/summary - View last summary
/clear - Delete saved data

**Example:**
• Send: `https://youtube.com/watch?v=...`
• Ask: "What is the main topic?"
• Translate: "Summarize in Hindi"

Let's get started! 🚀"""
        
        await update.message.reply_text(message, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /help command - Detailed usage guide
    """
    try:
        logger.info(f"User {update.message.from_user.id} requested help")
        
        help_text = """📖 **How to Use This Bot:**

**Step 1: Send a Video Link**
Send any YouTube link in one of these formats:
• `https://youtube.com/watch?v=...`
• `https://youtu.be/...`

The bot will automatically:
1. Fetch the video transcript
2. Generate a summary
3. Create text chunks for Q&A

**Step 2: Ask Questions**
After processing, ask any question about the video:
• "What is the main topic?"
• "Explain the pricing model"
• "Who is the speaker?"

**Step 3: Translate (Optional)**
Translate the summary to any language:
• `Summarize in Spanish`
• `Summarize in Hindi`
• `Summarize in French`

**Available Commands:**
/start - Show welcome message
/help - This help message
/summary - View the last summary
/clear - Delete your saved data

**⏱️ Rate Limiting:**
Max 30 requests per minute per user

**⚠️ Note:**
Videos must have transcripts available
(Subtitles or auto-generated captions work)

**💡 Tips:**
• Ask specific questions for better answers
• Long videos take longer to process
• Summaries are saved for 24 hours

Need more help? Check the video transcript details!"""
        
        await update.message.reply_text(help_text, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Error in help command: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again.")


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /summary command - Show last saved summary
    """
    try:
        user_id = update.message.from_user.id
        logger.info(f"User {user_id} requested summary")
        
        data = get_user_data(user_id)
        
        if not data or not data.get("summary"):
            await update.message.reply_text(
                "❌ No video processed yet.\n\n"
                "Send a YouTube URL first using:\n"
                "`https://youtube.com/watch?v=...`"
            )
            return
        
        summary = data.get("summary")
        url = data.get("url", "Unknown")
        
        message = f"""📝 **Your Last Summary:**

**Source:** {url}

{summary}

Use `/help` for other options or send another YouTube link."""
        
        await update.message.reply_text(message, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Error in summary command: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again.")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /clear command - Delete saved user data
    """
    try:
        user_id = update.message.from_user.id
        logger.info(f"User {user_id} cleared their data")
        
        # Delete from cache
        from services.cache import session_manager
        session_manager.delete_user_data(user_id)
        
        await update.message.reply_text(
            "✅ Your data has been deleted.\n\n"
            "Send a new YouTube link to get started again."
        )
        
    except Exception as e:
        logger.error(f"Error in clear command: {e}")
        await update.message.reply_text("❌ Failed to clear data. Please try again.")