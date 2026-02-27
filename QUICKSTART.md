# 🚀 QUICK START GUIDE

Get your bot running in **5 minutes**

---

## Step 1: Get API Keys (2 minutes)

### Telegram Bot Token
1. Open Telegram → Find **@BotFather**
2. Send `/newbot`, follow prompts
3. Copy token (e.g., `123456:ABC-DEF...`)

### Google Gemini API Key
1. Go to [ai.google.dev](https://ai.google.dev)
2. Click **"Get API Key"**
3. Copy the key

---

## Step 2: Setup Project (3 minutes)

```bash
# 1. Navigate to project
cd h:\youtube-telegram-bot

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Copy environment template
copy .env.example .env

# 4. Edit .env with your keys
notepad .env
# Add:
# TELEGRAM_TOKEN=your_bot_token
# GOOGLE_API_KEY=your_api_key
```

---

## Step 3: Run Bot (1 minute)

```bash
python main.py
```

You should see:
```
╔═══════════════════════════════════════════════════════════╗
║    🤖 YouTube AI Assistant - Telegram Bot                ║
║    Version: 1.0.0 | Status: Production Ready             ║
╚═══════════════════════════════════════════════════════════╝

✅ Configuration validated
✅ Directories ready
✅ Bot is running...
```

---

## Step 4: Test in Telegram

1. Find your bot (name you created in step 1)
2. Send `/start`
3. Send a YouTube link:
   ```
   https://youtube.com/watch?v=dQw4w9WgXcQ
   ```
4. Wait for summary
5. Ask questions!

---

## ⚡ Commands

| Command | What it does |
|---------|-------------|
| `/start` | Welcome message |
| `/help` | Detailed guide |
| `/summary` | Show last summary |
| `/clear` | Delete your data |

---

## 🎯 Usage Examples

### Send YouTube Link
```
https://youtube.com/watch?v=ABC123
https://youtu.be/ABC123
```

### Ask Questions
```
What's the main topic?
Explain the pricing model
Who is the speaker?
```

### Translate
```
Summarize in Spanish
Summarize in Hindi
Summarize in French
```

---

## 🐛 If Something Goes Wrong

### No response?
```bash
# Check logs
tail -f logs/bot.log
```

### "Invalid token"?
- Copy exact token from @BotFather
- Paste in `.env` file
- Restart bot

### "API key error"?
- Get key from [ai.google.dev](https://ai.google.dev)
- Enable Gemini API
- Add to `.env`

---

## 📚 Learn More

- **Full README:** `README.md`
- **Deployment:** `DEPLOYMENT.md`
- **Code Best Practices:** `BEST_PRACTICES.md`

---

## ✅ You're All Set!

The bot is now:
- ✅ **Production Ready** - Fully configured with error handling
- ✅ **Persistent** - Data stored in SQLite database
- ✅ **Rate Limited** - Protected against abuse
- ✅ **Logged** - Full audit trail in `logs/bot.log`
- ✅ **Student Friendly** - Code is readable and well-documented

**Happy bot! 🎉**
