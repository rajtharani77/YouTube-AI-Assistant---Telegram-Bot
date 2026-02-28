"""
Q&A Engine - Intelligent video question answering
Optimized for Gemini Flash models
"""

from services.llm_service import ask_llm
from utils.logger import logger
from utils.exceptions import ModelError

MAX_CONTEXT_CHUNKS = 3

def answer_question(question: str, chunks: list) -> str:
    """
    Answer question using transcript context
    """
    try:
        if not question or not isinstance(question, str):
            raise ValueError("Question must be valid")

        if not chunks:
            return "No transcript available. Process a video first."

        logger.info(f"Answering question: {question[:60]}")

        contexts = _retrieve_relevant_chunks(question, chunks)
        context_text = "\n\n".join(contexts)

        prompt = f"""
You are answering questions about a YouTube video.

Use ONLY the provided transcript context.

If the topic appears even partially, explain it clearly.
Only say "This topic is not covered in the video"
if absolutely no related information exists.

Transcript Context:
{context_text}

Question:
{question}

Answer clearly and concisely:
"""
        answer = ask_llm(prompt, temperature=0.2)

        logger.info("Answer generated successfully")

        return answer.strip()

    except Exception as e:
        logger.error(f"QA failed: {e}")
        raise ModelError(str(e))

def _retrieve_relevant_chunks(question: str, chunks: list):
    """
    Improved relevance search
    """
    question_words = set(question.lower().split())

    scored_chunks = []

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        overlap = len(question_words.intersection(chunk_words))
        phrase_bonus = 1 if question.lower() in chunk.lower() else 0

        score = overlap + phrase_bonus

        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    selected = [
        chunk for score, chunk in scored_chunks[:MAX_CONTEXT_CHUNKS]
    ]

    logger.info(f"Selected {len(selected)} context chunks")

    return selected