#  YouTube AI Assistant — Telegram Bot

An AI-powered **YouTube Knowledge Assistant** built using **Google Gemini 2.5 Flash** and deployed as a **Telegram Bot**.

The system converts long YouTube videos into an **interactive AI assistant** capable of:
- Generating structured summaries
- Answering contextual questions
- Retrieving knowledge directly from video transcripts

This project demonstrates a **Retrieval-Augmented Generation (RAG)** architecture integrated with real-world APIs and scalable backend design.

---

#  Project Overview

Modern video content is long and difficult to revisit for specific information.

This system transforms YouTube videos into searchable knowledge by:

1. Extracting transcripts
2. Processing content using LLMs
3. Structuring summaries
4. Enabling intelligent Q&A interaction

Users simply send a YouTube link to Telegram and interact with the video conversationally.

---

#  System Architecture

## High-Level Architecture


User (Telegram)
│
▼
Telegram Bot Interface
│
▼
Message Handler Layer
│
▼
Processing Pipeline
├── URL Validation
├── Video ID Extraction
├── Transcript Fetching
├── Chunk Generation
├── AI Summarization
└── Context Retrieval
│
▼
Gemini 2.5 Flash LLM
│
▼
MongoDB Storage
│
▼
AI Response → Telegram User


---

# ⚙️ Core Architecture Design

The project follows a **modular layered architecture**.


Interface Layer
↓
Controller Layer
↓
Core AI Engine
↓
Service Integrations
↓
Data Storage


---

#  Repository Structure


YouTube-AI-Assistant---Telegram-Bot/
│
├── bot/
│ ├── telegram_bot.py 
│ ├── handlers.py
│ └── commands.py 
│
├── core/
│ ├── transcript.py
│ ├── summarizer.py 
│ ├── qa_engine.py 
│ └── prompts.py
│
├── services/
│ ├── llm_service.py
│ └── youtube_service.py
├── data/
│ └── mongo.py
├── utils/
│ ├── logger.py
│ ├── helpers.py
│ ├── validators.py
│ └── exceptions.py
│
├── config/
│ └── settings.py 
│
├── logs/
├── main.py 
├── requirements.txt
└── README.md

---

#  Complete Processing Pipeline

## Step 1 — User Interaction
User sends a YouTube link through Telegram.


https://youtu.be/video_id


---

## Step 2 — Video Processing
System performs:

- URL validation
- Video ID extraction
- Transcript retrieval

Using:

youtube-transcript-api


---

## Step 3 — Transcript Processing

Transcript is divided into chunks to optimize LLM reasoning.

Why chunking?

✔ Prevent token overflow  
✔ Faster inference  
✔ Better summarization quality  

---

## Step 4 — AI Summarization (Gemini 2.5 Flash)

Hierarchical summarization pipeline:


Transcript
↓
Chunk Summaries
↓
Merged Context
↓
Final Structured Summary


Gemini Flash enables:
- Long context reasoning
- Fast responses
- Cost-efficient processing

---

## Step 5 — Storage Layer

Processed data stored in MongoDB:


Video ID
Transcript
Summary
User Session


Benefits:
- Faster repeated queries
- Persistent memory
- Multi-user scalability

---

## Step 6 — Question Answering (RAG)

When a user asks a question:


User Question
↓
Relevant Transcript Retrieval
↓
Context Injection
↓
Gemini Reasoning
↓
Grounded Answer


The model answers **strictly from transcript context**, reducing hallucinations.

---

#  AI Model Architecture

## Model Used

Google Gemini 2.5 Flash


### Why Gemini Flash?
- Large context window
- High reasoning speed
- Ideal for transcript analysis
- Efficient summarization

---

## Prompt Engineering Strategy

The system uses structured prompts:

- Summary Prompt
- Context QA Prompt
- Instruction-based grounding

Ensures:
 factual responses  
 contextual accuracy  
 controlled outputs  

---

# Technology Stack

| Layer | Technology |
|------|------------|
| Interface | Telegram Bot API |
| Backend | Python |
| LLM | Google Gemini 2.5 Flash |
| Database | MongoDB Atlas |
| Transcript Engine | youtube-transcript-api |
| API Framework | FastAPI |
| Logging | Python Logging |
| Retrieval | Chunk-based RAG |

---

#  Environment Setup

Create `.env`


TELEGRAM_TOKEN=
GOOGLE_API_KEY=
LLM_PROVIDER=google
MODEL_NAME=gemini-2.5-flash
MONGO_URI=
LOG_LEVEL=INFO


---

#  Installation Guide

## 1 Clone Repository

```bash
git clone https://github.com/rajtharani77/YouTube-AI-Assistant---Telegram-Bot.git
cd YouTube-AI-Assistant---Telegram-Bot
2 Create Virtual Environment
python -m venv .venv

Activate:

Windows

.venv\Scripts\activate

Linux/Mac

source .venv/bin/activate
3 Install Dependencies
pip install -r requirements.txt
4 Run Application
python main.py
5 Start Using Bot

Open Telegram → search your bot → send a YouTube link.

 Example Workflow
Input
https://youtu.be/example
Bot Output

Video Summary

Key Insights

Ask Questions
Q. What is constant time complexity?
A. Bot answers using video knowledge.

Engineering Highlights

Modular backend architecture
Retrieval-Augmented Generation
Hierarchical summarization
API abstraction layer
Poduction-ready logging
Scalable database integration

Future Improvements

Vector embeddings (FAISS)
Multi-video knowledge base
Web dashboard

 Author
Raj Tharani
GitHub: https://github.com/rajtharani77

 License

MIT License
