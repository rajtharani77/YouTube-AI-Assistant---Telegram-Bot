"""
YouTube Transcript Module - Extracts video transcripts
"""

from youtube_transcript_api import YouTubeTranscriptApi
import re
from utils.logger import logger
from utils.exceptions import TranscriptError


def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID from various URL formats
    
    Args:
        url: YouTube URL
        
    Returns:
        Video ID string
        
    Raises:
        TranscriptError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise TranscriptError("URL must be a non-empty string")
    
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([0-9A-Za-z_-]{11})",
        r"youtube\.com\/watch\?.*v=([0-9A-Za-z_-]{11})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise TranscriptError(f"Invalid YouTube URL format: {url}")


def fetch_transcript(url: str, language_codes: list = None) -> tuple:
    """
    Fetch transcript from YouTube video
    
    Args:
        url: YouTube video URL
        language_codes: List of language codes to try (default: auto-detect)
        
    Returns:
        Tuple of (full_transcript_text, raw_transcript_list)
        
    Raises:
        TranscriptError: If transcript cannot be fetched
    """
    try:
        video_id = extract_video_id(url)
        logger.info(f"Extracted video ID: {video_id}")
        
        try:
            # Try to fetch with specified languages or auto-detect
            if language_codes:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=language_codes)
            else:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            logger.info(f"Successfully fetched transcript ({len(transcript)} entries)")
            
        except Exception as e:
            # Fallback: try to get any available transcript
            logger.warning(f"Could not fetch preferred transcript: {e}")
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_manually_created_transcript().fetch()
                logger.info("Using manually created transcript as fallback")
            except Exception:
                # Last resort: get any available transcript
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_generated_transcript().fetch()
                logger.info("Using auto-generated transcript as fallback")
        
        # Combine transcript entries into single text
        full_text = " ".join([t["text"] for t in transcript])
        
        if not full_text or len(full_text.strip()) < 10:
            raise TranscriptError("Transcript is empty or too short")
        
        logger.info(f"Transcript length: {len(full_text)} characters")
        return full_text, transcript
        
    except TranscriptError:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch transcript: {e}")
        raise TranscriptError(f"Failed to fetch transcript: {str(e)}")