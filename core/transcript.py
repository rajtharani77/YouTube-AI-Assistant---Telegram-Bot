"""
YouTube Transcript Module
Robust transcript extraction with fallback handling
Optimized for LLM processing (Gemini Flash / RAG pipelines)
"""

import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from utils.logger import logger
from utils.exceptions import TranscriptError


# ---------------------------------------------------
# VIDEO ID EXTRACTION
# ---------------------------------------------------

def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""

    if not url or not isinstance(url, str):
        raise TranscriptError("Invalid YouTube URL")

    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"youtube\.com\/embed\/([0-9A-Za-z_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            logger.info(f"Extracted video ID: {video_id}")
            return video_id

    raise TranscriptError("Could not extract video ID")


# ---------------------------------------------------
# TRANSCRIPT FETCHING
# ---------------------------------------------------

def fetch_transcript(
    url: str,
    language_codes=None
):
    """
    Fetch transcript with intelligent fallback strategy

    Returns:
        (formatted_text, raw_transcript)
    """

    try:
        video_id = extract_video_id(url)

        api = YouTubeTranscriptApi()

        if language_codes is None:
            language_codes = ["en", "hi"]

        logger.info("Fetching transcript from YouTube")

        transcript = None

        # ---------------------------------------
        # Attempt 1: Preferred Languages
        # ---------------------------------------
        try:
            transcript = api.fetch(
                video_id,
                languages=language_codes
            )
            logger.info("Preferred transcript fetched")

        except Exception:
            logger.warning("Preferred transcript unavailable")

        # ---------------------------------------
        # Attempt 2: Manual captions
        # ---------------------------------------
        if transcript is None:
            try:
                transcripts = api.list(video_id)

                transcript = transcripts \
                    .find_manually_created_transcript(
                        language_codes
                    ).fetch()

                logger.info("Using manually created transcript")

            except Exception:
                logger.warning("Manual transcript unavailable")

        # ---------------------------------------
        # Attempt 3: Auto-generated captions
        # ---------------------------------------
        if transcript is None:
            try:
                transcripts = api.list(video_id)

                transcript = transcripts \
                    .find_generated_transcript(
                        language_codes
                    ).fetch()

                logger.info("Using auto-generated transcript")

            except Exception:
                raise TranscriptError(
                    "No transcript available for this video"
                )

        # ---------------------------------------
        # Format Transcript
        # ---------------------------------------
        formatter = TextFormatter()
        formatted_text = formatter.format_transcript(transcript)

        if not formatted_text or len(formatted_text.strip()) < 20:
            raise TranscriptError("Transcript too short")

        logger.info(
            f"Transcript fetched successfully "
            f"({len(formatted_text)} characters)"
        )

        return formatted_text, transcript

    except TranscriptError:
        raise

    except Exception as e:
        logger.error(f"Transcript fetch failed: {e}")
        raise TranscriptError(str(e))