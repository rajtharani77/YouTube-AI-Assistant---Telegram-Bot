# 🚀 Deployment Guide - YouTube Telegram Bot

Complete production deployment guide for students

---

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Local Testing](#local-testing)
3. [Deployment Options](#deployment-options)
4. [Post-Deployment](#post-deployment)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## ✅ Pre-Deployment Checklist

Before deploying, verify:

```bash
# 1. Check Python version (3.10+)
python --version

# 2. Verify all dependencies installed
pip list | grep -E "python-telegram-bot|google-generativeai|fastapi"

# 3. Test environment configuration
python -c "from config.settings import Config; Config.validate(); print('✅ Config OK')"

# 4. Test database
python -c "from services.cache import session_manager; print('✅ Database OK')"

# 5. Test LLM connection
python -c "from services.llm_service import ask_llm; print(ask_llm('test'))"

# 6. Check logs directory
mkdir -p logs
ls -la logs/

# 7. Verify .env file exists and has all required keys
grep -E "TELEGRAM_TOKEN|GOOGLE_API_KEY" .env
```

---

## 🧪 Local Testing

### Test 1: Bot Startup

```bash
python main.py
# Expected: Bot running message
# Press Ctrl+C to stop
```

### Test 2: API Connection

```bash
# Start bot in background
nohup python main.py > test.log 2>&1 &

# Get the process ID
ps aux | grep main.py

# Send a test message via Telegram (use your bot)
# Check logs
tail -f logs/bot.log

# Kill the background process
kill <PID>
```

### Test 3: Rate Limiting

```bash
# Modify MAX_REQUESTS_PER_MINUTE=2 in .env for testing
# Send 3 messages quickly
# Should see rate limit error on 3rd message
```

### Test 4: Database Persistence

```bash
# Run bot and process a video
python main.py

# Check database
sqlite3 data/bot.db
> SELECT COUNT(*) FROM user_sessions;
> SELECT * FROM user_sessions LIMIT 1;
> .exit

# Verify data persists across restarts
```

---

## 🌐 Deployment Options

### Option 1: VPS/Server (Ubuntu/Debian)

**Cost:** $5-20/month | **Difficulty:** Medium | **Best for:** Production use

#### Step 1: Server Setup

```bash
# Connect to VPS via SSH
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Python
apt install python3.10 python3.10-venv python3-pip git -y

# Create app directory
mkdir -p /apps/yt-bot
cd /apps/yt-bot
```

#### Step 2: Clone & Install

```bash
# Clone repository
git clone <your-repo-url> .

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
# Paste your configuration

# Create logs directory
mkdir -p logs data
chmod 755 logs data
```

#### Step 3: Option A - Run with Systemd (Recommended)

Create service file:

```bash
sudo nano /etc/systemd/system/yt-bot.service
```

Paste:

```ini
[Unit]
Description=YouTube Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/apps/yt-bot
Environment="PATH=/apps/yt-bot/venv/bin"
ExecStart=/apps/yt-bot/venv/bin/python main.py
Restart=always
RestartSec=10

StandardOutput=append:/apps/yt-bot/logs/bot.log
StandardError=append:/apps/yt-bot/logs/bot_error.log

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable yt-bot
sudo systemctl start yt-bot
sudo systemctl status yt-bot

# View logs
sudo journalctl -u yt-bot -f
```

#### Step 4: Option B - Run with Screen (Simple Alternative)

```bash
# Install screen
apt install screen -y

# Create persistent session
screen -S yt-bot

# Inside screen session
cd /apps/yt-bot
source venv/bin/activate
python main.py

# Detach: Press Ctrl+A then D
# Reattach: screen -r yt-bot
```

#### Step 5: Firewall Configuration (Optional)

```bash
# Allow SSH
ufw allow 22/tcp

# Enable firewall
ufw enable

# Check status
ufw status
```

---

### Option 2: Heroku Deployment

**Cost:** Free tier available | **Difficulty:** Easy | **Best for:** Learning/Light use

#### Step 1: Create Heroku App

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL (optional)
heroku addons:create heroku-postgresql:hobby-dev
```

#### Step 2: Add Files

Create `Procfile`:

```
web: gunicorn app:app
worker: python main.py
```

Create `runtime.txt`:

```
python-3.10.13
```

#### Step 3: Deploy

```bash
# Add files
git add .
git commit -m "Heroku deployment"

# Deploy
git push heroku main

# Set environment variables
heroku config:set TELEGRAM_TOKEN=your_token
heroku config:set GOOGLE_API_KEY=your_key

# View logs
heroku logs -t

# Scale worker
heroku ps:scale worker=1
```

---

### Option 3: Railway Deployment

**Cost:** Free tier available | **Difficulty:** Very Easy | **Best for:** Getting started

#### Step 1: Connect Repository

1. Go to [railway.app](https://railway.app)
2. Sign up/Login
3. Create new project → GitHub repo
4. Authorize GitHub
5. Select repository

#### Step 2: Configure

Railway automatically installs from `requirements.txt`

Add environment variables:
- Go to Variables tab
- Add `TELEGRAM_TOKEN`, `GOOGLE_API_KEY`, etc.

#### Step 3: Deploy

1. Go to Deployments tab
2. Click "Deploy"
3. Wait for build & deployment
4. Monitor logs in real-time

---

### Option 4: Docker Deployment

**Cost:** Varies | **Difficulty:** Hard | **Best for:** Advanced users

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p logs data

# Run bot
CMD ["python", "main.py"]
```

Create `.dockerignore`:

```
.env
logs/
data/
.git
__pycache__
*.pyc
.venv
```

Build & run locally:

```bash
# Build
docker build -t yt-bot .

# Run
docker run -d \
  --name yt-bot \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  yt-bot

# View logs
docker logs -f yt-bot

# Stop
docker stop yt-bot
docker rm yt-bot
```

---

## 🔧 Post-Deployment

### Verify Deployment

```bash
# Check if service started
systemctl status yt-bot

# Send test message to Telegram bot
# Verify response

# Check logs
tail -f /apps/yt-bot/logs/bot.log

# Test rate limiting
# Send 31 messages in 60 seconds
# Should block 31st message
```

### Database Backup

```bash
# Create backup
cp data/bot.db data/bot.db.backup.$(date +%Y%m%d_%H%M%S)

# Or automated daily backup
0 3 * * * cp /apps/yt-bot/data/bot.db /apps/yt-bot/backups/bot.db.$(date +\%Y\%m\%d)
```

### Log Rotation

Create `/etc/logrotate.d/yt-bot`:

```
/apps/yt-bot/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 root root
    restart
}
```

---

## 📊 Monitoring & Maintenance

### Monitor Bot Health

```bash
# Create health check script
nano /apps/yt-bot/check_health.sh
```

```bash
#!/bin/bash
BOT_PID=$(systemctl show -p MainPID --value yt-bot)
if [ "$BOT_PID" -eq 0 ]; then
    echo "Bot is not running!"
    systemctl restart yt-bot
    echo "Bot restarted"
fi
```

Add to crontab:

```bash
crontab -e
# Add: */5 * * * * /apps/yt-bot/check_health.sh
```

### Monitor Logs

```bash
# Check for errors
grep ERROR /apps/yt-bot/logs/bot.log | tail -20

# Check database size
du -sh /apps/yt-bot/data/

# Clean old sessions
sqlite3 data/bot.db "DELETE FROM user_sessions WHERE expires_at < datetime('now');"
```

### Performance Monitoring

```bash
# Check memory usage
ps aux | grep python

# Check disk space
df -h

# Check open connections
netstat -an | grep ESTABLISHED | wc -l
```

---

## 🆘 Troubleshooting Deployment

### Issue: "Bot not responding"

```bash
# Check service status
systemctl status yt-bot

# Check logs for errors
tail -100 /apps/yt-bot/logs/bot.log

# Restart service
systemctl restart yt-bot

# Check metrics
journalctl -u yt-bot -n 50
```

### Issue: "Out of disk space"

```bash
# Check disk
df -h

# Find large files
du -sh /apps/yt-bot/*

# Clean logs
rm /apps/yt-bot/logs/bot.log.*
truncate -s 0 /apps/yt-bot/logs/bot.log
```

### Issue: "API key invalid"

```bash
# Update .env
nano /apps/yt-bot/.env

# Restart bot
systemctl restart yt-bot

# Verify
grep GOOGLE_API_KEY /apps/yt-bot/.env
```

---

## 📈 Scaling (Advanced)

For handling more users:

1. **Increase rate limit:**
   ```env
   MAX_REQUESTS_PER_MINUTE=100
   ```

2. **Use production LLM:**
   - Switch to OpenAI GPT-4 (better)
   - Or use Claude API

3. **Implement caching:**
   - Redis for session cache
   - Query cache for common questions

4. **Database optimization:**
   - Add indexes to SQLite
   - Archive old sessions
   - Consider PostgreSQL

5. **Load balancing:**
   - Run multiple bot instances
   - Use message queue (RabbitMQ)
   - API gateway (Nginx)

---

## 📋 Final Checklist

- [ ] All environment variables set
- [ ] Database initialized
- [ ] Logs directory created
- [ ] Service/systemd configured
- [ ] Firewall configured (if needed)
- [ ] Backup strategy in place
- [ ] Log rotation configured
- [ ] Health checks set up
- [ ] Error alerts enabled
- [ ] Documentation updated

---

## 📞 Help & Support

**Common Issues:**
- Check logs: `tail -f logs/bot.log`
- Verify config: `python -c "from config.settings import Config; Config.validate()"`
- Test API: `python -c "from services.llm_service import ask_llm; print(ask_llm('test'))"`

**Resources:**
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Google Gemini API](https://ai.google.dev/)
- [Python Documentation](https://docs.python.org/3/)

---

**Good luck with your deployment! 🚀**
