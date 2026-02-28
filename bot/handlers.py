"""
Message and Event Handlers - Core bot logic for processing user requests
"""

from services.youtube_service import process_youtube_video
from core.summarizer import generate_summary
from core.qa_engine import answer_question
from core.language import translate
from services.cache import save_user_data, get_user_data
from utils.validators import is_youtube_url, is_empty
from utils.logger import logger
from utils.exceptions import (
    BotException, TranscriptError, ModelError, ValidationError, RateLimitError
)
from bot.rate_limiter import check_rate_limit


async def handle_message(update, context):
    """
    Main message handler - Routes to appropriate function
    """
    try:
        user_id = update.message.from_user.id
        text = update.message.text
        username = update.message.from_user.first_name
        
        logger.info(f"Message from {username} (ID: {user_id}): {text[:50]}...")
    
        check_rate_limit(user_id)
        
        if is_youtube_url(text):
            await _handle_youtube_url(update, context, user_id, text)
            return
        if text.lower().startswith("summarize in"):
            await _handle_translation_request(update, context, user_id, text)
            return
    
        await _handle_qa_request(update, context, user_id, text)
        
    except RateLimitError as e:
        logger.warning(f"Rate limit error for user {user_id}")
        await update.message.reply_text(f"⏱️ {str(e)}")
    except BotException as e:
        logger.error(f"Bot error: {e}")
        await update.message.reply_text(f" {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in handler: {e}")
        await update.message.reply_text(
            " An unexpected error occurred. Please try again."
        )


async def _handle_youtube_url(update, context, user_id: int, url: str):
    """Handle YouTube URL submission - fetch and summarize"""
    try:
        if is_empty(url):
            await update.message.reply_text("❌ Please provide a valid YouTube URL")
            return
        
        processing_msg = await update.message.reply_text(
            " Processing video...\n(This may take a minute)"
        )
        
        logger.info(f"Processing YouTube URL: {url}")
        
        video_data = process_youtube_video(url)
        logger.info("Video processed successfully")
        
        summary = generate_summary(video_data["text"])
        
        save_user_data(user_id, {
            "chunks": video_data["chunks"],
            "summary": summary,
            "url": url
        })
        
        logger.info(f"Summary saved for user {user_id}")
        
        await processing_msg.edit_text(
            f" **Video Summary:**\n\n{summary}"
        )
        
        await update.message.reply_text(
            " You can now:\n"
            "• Ask questions about the video\n"
            "• Use `/summary` to see summary again\n"
            "• Use `Summarize in [language]` to translate"
        )
        
    except TranscriptError as e:
        logger.error(f"Transcript error: {e}")
        await update.message.reply_text(
            f" Could not fetch video transcript:\n{str(e)}\n\n"
            "Make sure the video has captions enabled."
        )
    except ModelError as e:
        logger.error(f"Model error: {e}")
        await update.message.reply_text(
            f" Error generating summary: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error processing YouTube URL: {e}")
        await update.message.reply_text(
            " Failed to process video. Please try another video."
        )

async def _handle_translation_request(update, context, user_id: int, text: str):
    """Handle translation requests"""
    try:
        data = get_user_data(user_id)
        
        if not data:
            await update.message.reply_text(
                " No video processed yet. Send a YouTube URL first."
            )
            return
        
        language = text.split("in")[-1].strip()
        
        if is_empty(language):
            await update.message.reply_text(
                " Please specify a language. Example: 'Summarize in Spanish'"
            )
            return
        
        trans_msg = await update.message.reply_text(
            f" Translating to {language}...\n(Please wait)"
        )
        
        logger.info(f"Translating to {language} for user {user_id}")
        translated = translate(data["summary"], language)
        
        logger.info(f"Translation completed for user {user_id}")
        await trans_msg.edit_text(
            f" **Summary in {language}:**\n\n{translated}"
        )
        
    except ModelError as e:
        logger.error(f"Translation error: {e}")
        await update.message.reply_text(
            f" Translation failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error handling translation: {e}")
        await update.message.reply_text(
            " Failed to translate summary."
        )


async def _handle_qa_request(update, context, user_id: int, question: str):
    """Handle Q&A requests"""
    try:
        data = get_user_data(user_id)
        
        if not data:
            await update.message.reply_text(" No video processed yet. Send a YouTube URL first.")
            return
        
        if is_empty(question):
            await update.message.reply_text(" Please ask a valid question.")
            return
        
        logger.info(f"Answering question for user {user_id}: {question[:50]}...")
        
        answer = answer_question(question, data["chunks"])
        
        logger.info(f"Question answered for user {user_id}")
        
        await update.message.reply_text(
            f" **Q:** {question}\n\n"
            f" **A:** {answer}"
        )
        
    except ModelError as e:
        logger.error(f"QA error: {e}")
        await update.message.reply_text(
            f" Error answering question: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error handling Q&A: {e}")
        await update.message.reply_text(
            " Failed to answer question. Try again."
        )