# Code Quality & Best Practices Guide

This guide explains the production-ready code practices used in this project.

## 🎯 Code Organization

### 1. **Separation of Concerns**
Each module has a single responsibility:
- `bot/` - Telegram bot logic only
- `core/` - Processing pipeline
- `services/` - External API integrations
- `utils/` - Reusable utilities

**Why:** Easy to test, maintain, and extend

### 2. **Configuration Management**
All settings in `config/settings.py`:
```python
from config.settings import Config
print(Config.TELEGRAM_TOKEN)
```

**Why:** Never hardcode secrets, easy to change per environment

### 3. **Error Handling**
Specific exceptions for different failures:
```python
from utils.exceptions import TranscriptError, ModelError

try:
    transcript = fetch_transcript(url)
except TranscriptError as e:
    logger.error(f"Transcript failed: {e}")
```

**Why:** Better debugging, specific error messages

---

## 📝 Code Standards

### Type Hints (Always Use)

```python
# ✅ GOOD
def fetch_transcript(url: str) -> tuple:
    """Fetch transcript from URL"""
    pass

# ❌ BAD
def fetch_transcript(url):
    pass
```

**Why:** IDE autocomplete, early error detection, documentation

### Docstrings (Required)

```python
def answer_question(question: str, chunks: list) -> str:
    """
    Answer a question based on transcript chunks.
    
    Args:
        question: User's question
        chunks: List of transcript chunks
        
    Returns:
        Answer string
        
    Raises:
        ModelError: If answer generation fails
    """
```

**Why:** Auto-generated documentation, IDE help

### Comments (For Complex Logic)

```python
# Find most relevant chunk using keyword matching
# (In future: update to use embeddings for semantic search)
context = _find_relevant_chunk(question, chunks)
```

**Why:** Explains "why", not "what"

---

## 🔐 Security Best Practices

### 1. **Never Expose Secrets**

```python
# ✅ GOOD
logger.info(f"Connected to {Config.LLM_PROVIDER} API")

# ❌ BAD
logger.info(f"API Key: {Config.GOOGLE_API_KEY}")
```

### 2. **Validate All Input**

```python
# ✅ GOOD
from utils.validators import is_youtube_url, is_empty

if is_empty(url):
    raise ValidationError("URL cannot be empty")

if not is_youtube_url(url):
    raise ValidationError("Invalid YouTube URL format")

# ❌ BAD
if url:  # Doesn't check format
    process(url)
```

### 3. **Handle Exceptions Gracefully**

```python
# ✅ GOOD
try:
    result = ask_llm(prompt)
except Exception as e:
    logger.error(f"LLM error: {e}")
    return "Sorry, I couldn't generate a response"

# ❌ BAD
try:
    result = ask_llm(prompt)
except:
    pass  # Silent failure!
```

---

## 📊 Performance Optimizations

### 1. **Caching**

```python
# In-memory cache for quick access
self.in_memory_cache = {}

# Database for persistence
sqlite3.connect(self.db_path)

# Use in-memory first, fallback to DB
if user_id in self.in_memory_cache:
    return self.in_memory_cache[user_id]
```

### 2. **Lazy Loading**

```python
# Only load when needed
def _init_llm():
    """Initialize on first use"""
    genai.configure(api_key=Config.GOOGLE_API_KEY)
    return genai.GenerativeModel(Config.MODEL_NAME)

model = _init_llm()
```

### 3. **Async Operations**

```python
# Non-blocking message handling
async def handle_message(update, context):
    await update.message.reply_text("Processing...")
    ```

---

## 🧪 Testing Patterns

### Unit Tests (Mock External APIs)

```python
# tests/test_validators.py
def test_is_youtube_url():
    assert is_youtube_url("https://youtube.com/watch?v=abc")
    assert is_youtube_url("https://youtu.be/abc")
    assert not is_youtube_url("https://google.com")
```

### Integration Tests

```python
# tests/test_handlers.py
async def test_youtube_url_handler():
    update = Mock()
    context = Mock()
    await handle_message(update, context)
    # Verify update.message.reply_text was called
```

---

## 📋 Logging Standards

### Log Levels

```python
logger.critical("System failure")      # Shutdown required
logger.error("Operation failed")       # Fix needed
logger.warning("Rate limit hit")       # Monitor
logger.info("Bot started")             # Normal info
logger.debug("Processing chunk 5/10")  # Detailed debug
```

### Log Format

```
2024-02-27 10:30:45 | INFO | yt-bot | Starting bot...
2024-02-27 10:30:46 | ERROR | yt-bot | Configuration error
```

**What to log:**
- ✅ Configuration initialization
- ✅ External API calls (success/failure)
- ✅ User actions (with ID, not content)
- ✅ Errors with full context
- ✅ Performance metrics

**What NOT to log:**
- ❌ API keys or tokens
- ❌ User personal information
- ❌ Full error traces on success

---

## 🔄 Git & Version Control

### Commit Messages

```
✅ Good:
- "Add rate limiting to prevent abuse"
- "Fix YouTube URL regex for shortened URLs"
- "Refactor cache manager for SQLite"

❌ Bad:
- "fix bug"
- "update code"
- "changes"
```

### Gitignore

```gitignore
.env                    # Secrets
.venv/                  # Virtual env
__pycache__/            # Python cache
*.pyc                   # Compiled files
logs/                   # Runtime logs
data/bot.db            # User data
.DS_Store              # Mac files
```

---

## 📚 Code Review Checklist

Before pushing code:

- [ ] All functions have docstrings
- [ ] All inputs validated
- [ ] Error handling added
- [ ] Logging added for debugging
- [ ] No hardcoded secrets
- [ ] Type hints complete
- [ ] Tests pass
- [ ] Comments explain "why"
- [ ] Code follows PEP 8
- [ ] Commit messages clear

---

## 🚀 Deployment & Production

### Pre-Production

```python
# Ensure config validation
Config.validate()

# Ensure logging configured
logger.info("Starting bot")

# Ensure database ready
session_manager._init_database()

# Ensure error handling complete
try:
    ...
except SpecificError as e:
    logger.error(f"...")
```

### Environment-Specific Config

```python
# development
LOG_LEVEL=DEBUG
REQUEST_TIMEOUT=5

# staging
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30

# production
LOG_LEVEL=WARNING
REQUEST_TIMEOUT=60
```

---

## 💡 Learning Resources

### Python Best Practices
- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Real Python](https://realpython.com/)

### Design Patterns
- [Refactoring.Guru](https://refactoring.guru/design-patterns)
- Single Responsibility Principle (SRP)
- Don't Repeat Yourself (DRY)

### Testing
- [pytest Documentation](https://pytest.org/)
- [unittest for Python](https://docs.python.org/3/library/unittest.html)

### Code Quality Tools
```bash
# Install tools
pip install flake8 black pylint mypy

# Check code quality
flake8 bot/
black --check bot/
pylint bot/
mypy bot/ --ignore-missing-imports
```

---

## 🎓 Interview Questions (For Learning)

1. **Why do we use type hints?**
   - Answer: IDE support, early error detection, documentation

2. **Why separate concerns into modules?**
   - Answer: Testability, maintainability, reusability

3. **When should we log vs print?**
   - Answer: Log for production, print for debug

4. **What's the difference between error and exception?**
   - Answer: Exceptions are caught, errors may not be recoverable

5. **How do we prevent API key leaks?**
   - Answer: Environment variables, .env file in gitignore

---

**Remember: Write code that others (or future you) can understand! 🧠**
