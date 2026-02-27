#  YouTube AI Assistant - Telegram Bot

A production-ready Telegram bot that summarizes YouTube videos and answers questions about their content using AI. Built with **Python**, **FastAPI**, **Google Gemini**, and **SQLite**.

**Status:**  Production Ready (Student-Friendly) | Tested & Documented

---

##  Features

-  **Video Summarization** - Automatically generates concise summaries of YouTube videos
-  **Q&A Engine** - Answer questions based on video transcript content
-  **Multi-language Support** - Translate summaries to any language
-  **Rate Limiting** - Prevents abuse with configurable request limits
-  **Persistent Storage** - SQLite database for session management
-  **Error Handling** - Comprehensive error management and logging
-  **Async Support** - Built on asyncio for non-blocking operations
-  **Production Logging** - File and console logging with configurable levels

---

##  Architecture

```
youtube-telegram-bot/
├── bot/                    
│   ├── commands.py        
│   ├── handlers.py        
│   ├── rate_limiter.py    
│   └── telegram_bot.py   
├── core/                   
│   ├── qa_engine.py       
│   ├── summarizer.py      
│   ├── transcript.py      
│   ├── chunking.py       
│   ├── language.py       
│   └── prompts.py         
├── services/              
│   ├── youtube_service.py 
│   ├── llm_service.py     
│   └── cache.py           
├── config/                
│   └── settings.py        
├── utils/                 
│   ├── logger.py          
│   ├── validators.py      
│   ├── exceptions.py      
│   └── helpers.py        
├── data/                 
│   ├── bot.db           
│   └── embeddings/      
├── logs/           
├── app.py             
├── main.py             
├── requirements.txt    
├── .env        
└── README.md           
```

---

##  Quick Start (Installation & Setup)

### Prerequisites

- Python 3.10+
- pip or conda
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd youtube-telegram-bot
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Get from: https://telegram.dev/bots
TELEGRAM_TOKEN=YOUR_BOT_TOKEN_HERE

# Get from: https://ai.google.dev/
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE

# Optional settings
LOG_LEVEL=INFO
MAX_REQUESTS_PER_MINUTE=30
REQUEST_TIMEOUT=60
DATABASE_URL=sqlite:///./data/bot.db
```

### Step 5: Run the Bot

```bash
python main.py
```

You should see:
```
2024-02-27 10:30:45 | INFO | ... | Configuration: {...}
2024-02-27 10:30:45 | INFO | ... | Starting Telegram Bot...
2024-02-27 10:30:45 | INFO | ... | Bot is running...
```

---

##  Getting API Keys

### Telegram Bot Token

1. Open Telegram and find **@BotFather**
2. Send `/newbot`
3. Follow the prompts
4. Copy the token (format: `123456:ABC-DEF...`)

### Google Gemini API Key

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click **"Get API Key"**
3. Choose/create a project
4. Copy the API key
5. Paste in `.env` file

---

##  Usage Guide

### For Users

#### 1. **Start the Bot**
Send `/start` to the bot in Telegram

#### 2. **Send YouTube Link**
```
https://youtube.com/watch?v=... 
or
https://youtu.be/...
```

The bot will:
- Fetch the video transcript
- Generate a summary
- Save for future queries

#### 3. **Ask Questions**
```
"What is the main topic?"
"Explain the pricing model"
"Who is speaking?"
```

#### 4. **Translate Summary**
```
"Summarize in Spanish"
"Summarize in Hindi"
"Summarize in French"
```

#### 5. **Available Commands**
- `/start` - Start the bot
- `/help` - Get detailed help
- `/summary` - View last summary
- `/clear` - Delete saved data

---

##  Configuration

### Environment Variables (`.env`)

```env
# REQUIRED
TELEGRAM_TOKEN=your_bot_token
GOOGLE_API_KEY=your_api_key
LLM_PROVIDER=google              # or "openai"
MODEL_NAME=gemini-2.5-flash      # Google model

# OPTIONAL
LOG_LEVEL=INFO                   # DEBUG, INFO, WARNING, ERROR
MAX_WORKERS=4                    # Concurrent workers
REQUEST_TIMEOUT=60               # Seconds
DATABASE_URL=sqlite:///./data/bot.db
TOKEN_EXPIRY_HOURS=24            # Session expiration
MAX_REQUESTS_PER_MINUTE=30       # Rate limit
```

### Logging

Logs are stored in:
- **Console:** Real-time output
- **File:** `logs/bot.log` - Persistent logs

Check logs for debugging:
```bash
tail -f logs/bot.log
```

---

##  Database Schema

### user_sessions Table

```sql
CREATE TABLE user_sessions (
    user_id INTEGER PRIMARY KEY,
    summary TEXT,
    chunks TEXT (JSON),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    expires_at TIMESTAMP
)
```

**Automatic Features:**
- Session expiration (24 hours default)
- Automatic cleanup of expired sessions
- JSON storage of chunks

---

##  Security Features

 **Implementation:**
- Configuration validation on startup
- Input validation for all user inputs
- API key isolation in environment
- Rate limiting (30 requests/minute)
- Session expiration after 24 hours
- Secure error messages (no sensitive data in responses)
- Logging without sensitive information

**Best Practices:**
1. Never commit `.env` file
2. Use strong Telegram bot tokens
3. Keep API keys confidential
4. Regularly review logs
5. Monitor rate limit patterns

---

##  Error Handling

The bot handles various error scenarios:

| Error | Cause | Solution |
|-------|-------|----------|
| `TranscriptError` | Video has no captions | Enable captions or choose another video |
| `ModelError` | LLM API failure | Check API key and quota |
| `RateLimitError` | Too many requests | Wait and try again |
| `ConfigurationError` | Missing API keys | Update `.env` file |
| `DatabaseError` | Database connection issue | Check database file permissions |
| `ValidationError` | Invalid input | Review input format |

---

##  Deployment

### Option 1: VPS/Server

```bash
sudo apt update && sudo apt install python3.10 python3-pip

git clone <repo-url>
cd youtube-telegram-bot
pip install -r requirements.txt
nohup python main.py > bot.log 2>&1 &
sudo nano /etc/systemd/system/yt-bot.service
```

### Option 2: Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t yt-bot .
docker run -d --name yt-bot --env-file .env yt-bot
```

### Option 3: Cloud Deployment

- **Heroku:** Use `Procfile` and `.env` config vars
- **Railway:** Connect GitHub repo, set env vars
- **PythonAnywhere:** Upload files, set WSGI config
- **Replit:** Clone repo, install, run

---

##  Project Structure Explanation

### bot/ - Telegram Bot Logic
- **commands.py**: Handles `/start`, `/help`, `/summary`, `/clear`
- **handlers.py**: Routes messages to appropriate processors
- **rate_limiter.py**: Prevents abuse with request limits
- **telegram_bot.py**: Bot initialization and polling

### core/ - Processing Pipeline
- **transcript.py**: Extracts transcripts from YouTube videos
- **chunking.py**: Splits text into manageable pieces
- **summarizer.py**: Generates summaries using LLM
- **qa_engine.py**: Answers questions based on content
- **language.py**: Translates summaries to other languages
- **prompts.py**: LLM prompt templates

### services/ - External Integrations
- **youtube_service.py**: YouTube API handling
- **llm_service.py**: Google Gemini API integration
- **cache.py**: User session storage (SQLite + in-memory)

### utils/ - Utilities
- **logger.py**: Logging configuration
- **validators.py**: Input validation
- **exceptions.py**: Custom exception classes
- **helpers.py**: Helper functions

---

##  Testing (Manual)

Test specific scenarios:

```bash
DEBUG=1 python main.py

python -c "from core.transcript import fetch_transcript; print(fetch_transcript('https://youtube.com/watch?v=...'))"

python -c "from services.llm_service import ask_llm; print(ask_llm('Hello'))"

sqlite3 data/bot.db
> SELECT COUNT(*) FROM user_sessions;
```

---

##  Learning Path (For Students)

1. **Start with:** `bot/commands.py` - Simple command handling
2. **Then:** `bot/handlers.py` - Message routing logic
3. **Then:** `services/cache.py` - SQLite database usage
4. **Then:** `core/summarizer.py` - LLM integration
5. **Finally:** `bot/rate_limiter.py` - Advanced rate limiting

Each module is documented with:
- Clear docstrings
- Type hints
- Comments for complex logic
- Error handling examples

---

##  Troubleshooting

### Issue: "TELEGRAM_TOKEN is required"
**Solution:** Check `.env` file has correct token format

### Issue: "GOOGLE_API_KEY is not configured"
**Solution:** Verify API key in `.env` and enable Gemini API [here](https://ai.google.dev/)

### Issue: "Invalid YouTube URL"
**Solution:** Ensure URL format is correct:
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

### Issue: "Video has no transcript"
**Solution:** Video must have:
- Closed captions (CC) OR
- Auto-generated captions

### Issue: "Database is locked"
**Solution:** Close other connections to `data/bot.db`

### Issue: Rate limit exceeded
**Solution:** Wait 60 seconds or increase `MAX_REQUESTS_PER_MINUTE`

---

##  Performance Optimizations

 **Implemented:**
- In-memory caching for active sessions
- SQLite for lightweight persistence
- Text chunking for better QA
- Async message handling
- Lazy loading of modules
- Prompt optimization

 **Future Improvements:**
- Vector embeddings for semantic search
- Redis for distributed caching
- Batch processing for multiple videos
- Query caching for repeated questions

---

##  License

MIT License - Feel free to use for learning and projects

---

##  For Students

This project is designed for **computer science students** learning:
-  Python async programming
-  API integration (REST, WebSockets)
-  Database design (SQLite)
-  Error handling & logging
-  Environment configuration
-  Code organization & architecture
-  Production-ready practices

**Learning Resources:**
- [Python docs](https://docs.python.org/3/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Google Gemini API](https://ai.google.dev/tutorials)
- [FastAPI](https://fastapi.tiangolo.com/)

---

##  Contributing

To improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make changes with clear commit messages
4. Test thoroughly
5. Submit a pull request

---

##  Support

- **Issues:** Open an issue on GitHub
- **Email:** rajtharani77@gmail.com
- **Documentation:** Check README and code comments

---

##  Production Checklist

Before deploying to production:

- [ ] All environment variables configured
- [ ] Database backup strategy in place
- [ ] Logging configured for production level
- [ ] Rate limits tuned for expected load
- [ ] Error messages sanitized
- [ ] API keys rotated periodically
- [ ] Database indexed for common queries
- [ ] Monitoring alerts configured
- [ ] Graceful shutdown implemented
- [ ] Documentation up to date

---

**Happy coding!**

Last Updated: February 27, 2026
Version: 1.0.0
