"""
YouTube Service - Handles video transcript fetching and processing
"""

from core.transcript import fetch_transcript
from core.chunking import chunk_text
from utils.logger import logger
from utils.exceptions import TranscriptError

def process_youtube_video(url: str) -> dict:
    """
    Fetch transcript and prepare chunks for a YouTube video
    
    Args:
        url: YouTube video URL
        
    Returns:
        Dictionary with transcript text and chunks
        
    Raises:
        TranscriptError: If transcript cannot be fetched
    """
    try:
        logger.info(f"Processing YouTube video: {url}")
        
        transcript_text, raw_transcript = fetch_transcript(url)
        logger.info("Transcript fetched successfully")
        
        chunks = chunk_text(transcript_text)
        logger.info(f"Split transcript into {len(chunks)} chunks")
        
        return {
            "text": transcript_text,
            "chunks": chunks,
            "raw": raw_transcript,
            "status": "success"
        }
        
    except TranscriptError as e:
        logger.error(f"Transcript error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing video: {e}")
        raise TranscriptError(f"Failed to process video: {str(e)}")