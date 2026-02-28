SUMMARY_PROMPT = """
You are an AI research assistant.
Create a structured YouTube summary.
Return format:

 Title
 Key Points (5)
 Important Timestamps
 Core Insight

Transcript:
{transcript}
"""

QA_PROMPT = """
Answer ONLY using provided transcript context.

If answer not present say:
"This topic is not covered in the video."

Context:
{context}

Question:
{question}
"""
TRANSLATE_PROMPT = """
Translate below content into {language}.
Keep formatting identical.

{text}
"""