# Free Fire Game Automation Bot

A sophisticated **Free Fire game bot** with an integrated **Flask web dashboard** for squad management, player waitlist handling, and administrative controls.

**Status**: ✅ Production-Ready (with proper configuration)  
**Version**: 2.0.0  
**Language**: Python (94.5%) + HTML (5.2%) + Shell (0.3%)

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features & Capabilities](#-features--capabilities)
3. [Project Architecture](#-project-architecture)
4. [Prerequisites & Installation](#-prerequisites--installation)
5. [Configuration Guide](#-configuration-guide)
6. [Running the Bot](#-running-the-bot)
7. [Web Dashboard Guide](#-web-dashboard-guide)
8. [API Reference](#-api-reference)
9. [Security Features](#-security-features)
10. [Testing & Debugging](#-testing--debugging)
11. [Deployment Options](#-deployment-options)
12. [Troubleshooting](#-troubleshooting)
13. [Contributing & Support](#-contributing--support)
14. [Legal & License](#-legal--license)
15. [FAQ](#-faq)

---

## 📋 Project Overview

### What is ISMAIL-BOT?

**ISMAIL-BOT** is an automated game bot for **Free Fire** (mobile battle royale game) with the following components:

| Component | Purpose |
|-----------|---------|
| **Game Bot** | Automates gameplay, squad management, messaging, and player interactions |
| **Web Dashboard** | Flask-based interface for managing players, waitlists, and bot statistics |
| **Instagram API** | Scrapes public Instagram user profiles for verification |
| **PostgreSQL Database** | Stores player data, bot accounts, and activity logs |
| **Encryption Layer** | AES-256 encryption for secure network communication |

### Project Goals

✅ **Automate repetitive gameplay tasks** for Free Fire  
✅ **Manage multiple players** through a unified waitlist system  
✅ **Provide admin controls** via intuitive web interface  
✅ **Maintain security** with encrypted communications  
✅ **Enable portability** across Windows, Linux, macOS, and Docker

---

## 🚀 Features & Capabilities

### Game Bot Features

| Feature | Description |
|---------|-------------|
| **Squad Management** | Auto-join squads, manage teammates, send messages |
| **Emote Control** | Send automated emotes during gameplay |
| **Player Profiles** | Fetch and display player statistics and profiles |
| **Token Refresh** | Auto-refresh authentication tokens every 5 hours |
| **Multi-Server Support** | Supports BD (Bangladesh), IND (India), US servers |
| **Encrypted Communication** | All packets encrypted with AES-256 |

### Web Dashboard Features

| Feature | Description |
|---------|-------------|
| **Player Waitlist** | Submit and track player join requests |
| **Admin Panel** | Accept/reject players, manage bot accounts |
| **Statistics** | View bot usage metrics and performance logs |
| **Secure Access** | Two-tier authentication (main user + admin) |
| **Activity Logs** | Track all administrative actions |

---

## 📊 Project Architecture

### Directory Structure

```
ISMAILdz13/FF-bot/
│
├── README.md                          # This file - project documentation
├── main.py                            # Entry point wrapper
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
├── pyproject.toml                     # Python project metadata
├── run_bot.sh                         # Shell script to run bot (with auto-restart)
├── run_website.sh                     # Shell script to run website (with auto-restart)
│
├── ISMAIL_BOT/                        # 🤖 Core Bot Application Package (94.5% of code)
│   ├── __init__.py
│   ├── main.py                        # Bot logic: squad management, messaging, game interactions
│   ├── config.py                      # Environment-based configuration loader
│   ├── crypto.py                      # AES-256 encryption & protobuf packet building
│   ├── helpers.py                     # API calls, player info fetching (de-obfuscated)
│   ├── accounts.json                  # Bot account credentials (KEEP SECURE!)
│   ├── requirements.txt               # Python dependencies for bot
│   ├── install.sh                     # Automated installation script
│   ├── package.json                   # Node.js dependencies (legacy, optional)
│   │
│   ├── APIS/                          # External Service Integrations
│   │   ├── __init__.py
│   │   └── insta.py                   # Instagram profile scraper (public profiles only)
│   │
│   └── Pb2/                           # Protobuf Message Definitions (auto-generated)
│       ├── DEcwHisPErMsG_pb2.py        # Event/message protocol buffers
│       ├── MajoRLoGinrEs_pb2.py        # Login response protocol buffers
│       ├── Team_msg_pb2.py             # Team/squad message protocol buffers
│       └── ... (additional protobuf files)
│
├── website/                           # 🌐 Flask Web Application (5.2% of code)
│   ├── app.py                         # Flask routes, database logic, authentication
│   ├── requirements.txt               # Flask & web dependencies
│   │
│   ├── static/                        # Frontend Assets
│   │   ├── style.css                  # Main stylesheet
│   │   ├── script.js                  # JavaScript functionality
│   │   └── images/                    # UI images and logos
│   │
│   └── templates/                     # Jinja2 HTML Templates
│       ├── base.html                  # Base layout template (header, nav, footer)
│       ├── login.html                 # Player login page
│       ├── start.html                 # Player waitlist submission form
│       ├── dev_area.html              # Admin dashboard (main interface)
│       └── dev_stats.html             # Statistics and logs page
│
└── docs/                              # 📚 Additional Documentation (optional)
    ├── API.md                         # Detailed API documentation
    ├── ARCHITECTURE.md                # System architecture deep-dive
    └── TROUBLESHOOTING.md             # Common issues and solutions
```

### Component Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│                    Free Fire Game Servers                    │
│                    (Garena BD/IND/US)                        │
│                                                               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                ┌──────────▼──────────┐
                │                     │
         ┌──────▼──────┐      ┌───────▼────────┐
         │  Game Bot   │      │  Web Dashboard │
         │ (main.py)   │      │   (Flask app)  │
         └──────┬──────┘      └───────┬────────┘
                │                     │
         ┌──────▼──────┐      ┌───────▼────────┐
         │  Encryption │      │  Web Server    │
         │  (AES-256)  │      │   Port 5000    │
         └──────┬──────┘      └───────┬────────┘
                │                     │
                └──────────┬──────────┘
                           │
                ┌──────────▼──────────┐
                │                     │
           ┌────▼───┐         ┌──────▼────┐
           │Database │         │Auth Layer │
           │PostgreSQL        │(Access     │
           │          │       │ Codes)    │
           └──────────┘       └───────────┘
```

---

## ⚙️ Configuration Guide

### Step 1: Prerequisites

Before installation, ensure you have:

- **Python 3.9+** - Download from [python.org](https://www.python.org)
- **PostgreSQL 12+** - Download from [postgresql.org](https://www.postgresql.org)
- **pip or poetry** - Python package managers (pip comes with Python)
- **Git** - For version control (optional but recommended)
- **4GB+ RAM** - For bot and database operations
- **Internet connection** - For Free Fire server communication

### Step 2: Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
nano .env  # Edit with your values
```

**Complete `.env` Configuration:**

```env
# ========== 🎮 BOT CONFIGURATION ==========
BOT_NAME=ISMAIL-BOT™                # Display name for the bot
ADMIN_UID=<your_admin_uid>          # Your Free Fire admin account ID
BOT_UID=<your_bot_uid>              # Bot's Free Fire account ID
BOT_SERVER=BD                       # Server region: BD, IND, or US
BOT_KEY=<your_bot_key>              # Garena API key for bot
BYPASS_TOKEN=<bypass_token>         # Token to bypass certain restrictions

# ========== ⏱️ TIMING SETTINGS ==========
START_SPAM_DURATION=18              # How long to perform actions (seconds)
WAIT_AFTER_MATCH=20                 # Wait time after match ends (seconds)
START_SPAM_DELAY=0.2                # Delay between actions (seconds)

# ========== 📝 LOGGING ==========
LOG_LEVEL=INFO                      # Log levels: DEBUG, INFO, WARNING, ERROR
                                    # DEBUG = most verbose, ERROR = least

# ========== 🌐 FLASK WEB CONFIGURATION ==========
FLASK_SECRET_KEY=<generate_strong_key>  # See: python -c "import secrets; print(secrets.token_hex(32))"
FLASK_HOST=0.0.0.0                      # Listen on all network interfaces
FLASK_PORT=5000                         # Web dashboard port
FLASK_DEBUG=False                       # Never set to True in production!
FLASK_ENV=production                    # production or development

# ========== 🗄️ DATABASE CONFIGURATION ==========
DATABASE_URL=postgresql://user:password@localhost:5432/ismail_bot
# Format: postgresql://username:password@host:port/database_name

# ========== 🔐 SECURITY ACCESS CODES ==========
MAIN_ACCESS_CODE=<15_digit_code>    # Required to access player waitlist
DEV_ACCESS_CODE=<15_digit_code>     # Required to access admin dashboard
```

**How to Generate a Strong Secret Key:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output to your `.env` file.

### Step 3: Database Setup

#### Option A: PostgreSQL Local Installation

**Linux/macOS:**
```bash
# Install PostgreSQL
brew install postgresql@15  # macOS
sudo apt-get install postgresql postgresql-contrib  # Ubuntu/Debian

# Start PostgreSQL
brew services start postgresql@15  # macOS
sudo systemctl start postgresql  # Linux

# Create database
createdb ismail_bot

# Create tables (see below)
psql ismail_bot < database.sql
```

**Windows:**
1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer and remember your password
3. Open pgAdmin 4 (comes with PostgreSQL)
4. Create new database named `ismail_bot`
5. Run the SQL script in Query Tool

#### Option B: Remote Database

If using a cloud database (AWS RDS, Azure Database, etc.):

```env
DATABASE_URL=postgresql://username:password@your-host:5432/ismail_bot
```

#### Create Database Tables

**Execute this SQL in your PostgreSQL client:**

```sql
-- 👥 Player Waitlist Table
CREATE TABLE IF NOT EXISTS waitlist (
    id SERIAL PRIMARY KEY,
    player_id VARCHAR(20) NOT NULL UNIQUE,
    player_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, accepted, rejected
    discord_id VARCHAR(20),                 -- Optional: Discord ID for notifications
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 🤖 Bot Accounts Table
CREATE TABLE IF NOT EXISTS bot_accounts (
    id SERIAL PRIMARY KEY,
    bot_uid VARCHAR(20) NOT NULL UNIQUE,
    bot_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',   -- active, inactive, banned
    server VARCHAR(10) DEFAULT 'BD',       -- BD, IND, US
    last_login TIMESTAMP,
    login_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 📋 Admin Activity Logs
CREATE TABLE IF NOT EXISTS admin_logs (
    id SERIAL PRIMARY KEY,
    admin_id VARCHAR(20),
    action VARCHAR(100),                    -- action type: accept, reject, delete, etc.
    player_id VARCHAR(20),
    details TEXT,                           -- JSON or plain text details
    ip_address VARCHAR(45),                 -- IPv4 or IPv6
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX idx_waitlist_status ON waitlist(status);
CREATE INDEX idx_admin_logs_created ON admin_logs(created_at);
CREATE INDEX idx_bot_accounts_status ON bot_accounts(status);
```

---

## 🚀 Prerequisites & Installation

### Quick Install (Automated)

```bash
# 1. Clone repository
git clone https://github.com/ISMAILdz13/FF-bot.git
cd FF-bot

# 2. Run installation script
bash ISMAIL_BOT/install.sh

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with your values

# 4. Setup database
psql -U postgres -d ismail_bot -f database.sql

# 5. Start bot
python ISMAIL_BOT/main.py &
python website/app.py &
```

### Manual Install (Step-by-Step)

#### Step 1: Create Virtual Environment

```bash
# Using venv (recommended)
python -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows
```

#### Step 2: Install Dependencies

```bash
# Install bot dependencies
pip install -r ISMAIL_BOT/requirements.txt

# Install web dependencies
pip install -r website/requirements.txt

# Verify installation
python -c "import flask; import psycopg2; print('✅ Dependencies installed!')"
```

#### Step 3: Verify Setup

```bash
# Test bot can start
python -m ISMAIL_BOT.main --test

# Test web dashboard
python website/app.py
# Visit http://localhost:5000
```

---

## 🎮 Running the Bot

### Option 1: Direct Python Execution

**Terminal 1 - Start Bot:**
```bash
cd FF-bot
source venv/bin/activate  # or: venv\Scripts\activate on Windows
python ISMAIL_BOT/main.py
```

**Terminal 2 - Start Dashboard:**
```bash
cd FF-bot
source venv/bin/activate
python website/app.py
```

**Output should show:**
```
Bot: Connected to Free Fire servers ✅
Web: Running on http://0.0.0.0:5000
```

### Option 2: Using Shell Scripts (Auto-Restart)

```bash
# Make scripts executable
chmod +x run_bot.sh run_website.sh

# Run in background with auto-restart
bash run_bot.sh &
bash run_website.sh &

# Check status
ps aux | grep python

# Stop services
pkill -f "python ISMAIL_BOT/main.py"
pkill -f "python website/app.py"
```

### Option 3: Docker Deployment

**Requirements:** Docker Desktop installed

```bash
# Build image
docker build -t ismail-bot:latest .

# Run container
docker run \
  --name ff-bot \
  --env-file .env \
  -p 5000:5000 \
  -d \
  ismail-bot:latest

# View logs
docker logs -f ff-bot

# Stop container
docker stop ff-bot
docker rm ff-bot
```

**Using Docker Compose:**

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Option 4: Production with systemd (Linux)

**Create service file:** `/etc/systemd/system/ismail-bot.service`

```ini
[Unit]
Description=ISMAIL-BOT Game Bot
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=ismail                                    # Run as unprivileged user
Group=ismail
WorkingDirectory=/opt/ismail-bot
Environment="PATH=/opt/ismail-bot/venv/bin"
ExecStart=/opt/ismail-bot/venv/bin/python ISMAIL_BOT/main.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Enable and start:**

```bash
# Create user
sudo useradd -m ismail

# Copy files
sudo cp -r FF-bot /opt/ismail-bot
sudo chown -R ismail:ismail /opt/ismail-bot

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable ismail-bot
sudo systemctl start ismail-bot

# Monitor
sudo systemctl status ismail-bot
sudo journalctl -u ismail-bot -f
```

---

## 🌐 Web Dashboard Guide

### Accessing the Dashboard

**URL:** `http://localhost:5000`

### Dashboard Pages

#### 1. **Main Login Page** (`/`)

- Players enter their **Free Fire player ID**
- Click "Submit" to join the waitlist
- **Required:** `MAIN_ACCESS_CODE` (from `.env`)

#### 2. **Player Status Page** (`/start`)

- Check if player is **pending**, **accepted**, or **rejected**
- Shows last update time
- Auto-refreshes every 30 seconds

#### 3. **Admin Dashboard** (`/dev`)

- **Required:** `DEV_ACCESS_CODE` (from `.env`)
- View all players in waitlist
- **Actions:**
  - ✅ Accept player (moves to squad)
  - ❌ Reject player (removes from queue)
  - 👤 View player profile
  - 📊 View statistics

#### 4. **Statistics Page** (`/dev/stats`)

- Bot activity logs
- Player acceptance/rejection rates
- Server status
- Performance metrics

### Dashboard Features Deep Dive

| Feature | Location | What It Does |
|---------|----------|--------------|
| **Waitlist** | Dashboard home | Lists all players waiting to join |
| **Search** | Top of waitlist | Find player by ID or name |
| **Bulk Actions** | Dashboard toolbar | Accept/reject multiple players |
| **Export** | Admin menu | Download waitlist as CSV |
| **Logs** | Admin panel | View all actions taken |
| **Settings** | Admin menu | Manage bot behavior, timings |

---

## 🔑 API Endpoints

### Public Endpoints (No Authentication)

```
GET /
  Purpose: Render main login page
  
POST /
  Purpose: Submit player to waitlist
  Body: { "player_id": "12345678", "access_code": "MAIN_ACCESS_CODE" }
  Response: { "status": "success", "player_id": "12345678" }

GET /start
  Purpose: Check player status
  Query: ?player_id=12345678
  Response: { "status": "pending|accepted|rejected", "created_at": "2026-03-17" }
```

### Admin Endpoints (Requires DEV_ACCESS_CODE)

```
GET /dev
  Purpose: Render admin dashboard
  Header: Authorization: Bearer <DEV_ACCESS_CODE>

GET /dev/stats
  Purpose: Get statistics page
  
POST /api/status/<player_id>
  Purpose: Get detailed player status
  Response: { "player_id": "...", "status": "...", "created_at": "..." }

POST /api/accept/<player_id>
  Purpose: Accept player into bot squad
  Body: { "access_code": "DEV_ACCESS_CODE" }
  Response: { "message": "Player accepted", "player_id": "..." }

POST /api/reject/<player_id>
  Purpose: Reject player from waitlist
  Body: { "access_code": "DEV_ACCESS_CODE", "reason": "..." }
  Response: { "message": "Player rejected" }

GET /api/logs
  Purpose: Get admin activity logs
  Query: ?limit=50&offset=0
  Response: [ { "admin_id": "...", "action": "...", "created_at": "..." } ]

POST /api/bot/restart
  Purpose: Gracefully restart bot (server-side)
  Body: { "access_code": "DEV_ACCESS_CODE" }
```

### Using the API with cURL

```bash
# Check player status
curl -X GET "http://localhost:5000/start?player_id=12345678"

# Submit to waitlist
curl -X POST "http://localhost:5000/" \
  -H "Content-Type: application/json" \
  -d '{"player_id":"12345678","access_code":"YOUR_MAIN_CODE"}'

# Accept player (admin)
curl -X POST "http://localhost:5000/api/accept/12345678" \
  -H "Content-Type: application/json" \
  -d '{"access_code":"YOUR_DEV_CODE"}'
```

---

## 🛡️ Security Features

### Built-in Security

✅ **AES-256 Encryption** - All Free Fire packets encrypted  
✅ **Environment Variables** - Secrets never hardcoded  
✅ **Parameterized SQL** - Prevents SQL injection  
✅ **HttpOnly Cookies** - CSRF/XSS protection  
✅ **Connection Pooling** - Efficient DB connection management  
✅ **Admin Logging** - All admin actions tracked  
✅ **Rate Limiting** - Prevents bot abuse  

### Security Best Practices

#### For Development:

```env
FLASK_DEBUG=False         # Always disable in production
LOG_LEVEL=INFO            # Show important events only
DATABASE_URL=...          # Use local PostgreSQL
```

#### For Production:

1. **Enable HTTPS:**
   ```env
   FLASK_SESSION_SECURE=True
   ```
   (Requires SSL certificate - use Let's Encrypt)

2. **Rotate Secret Keys:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Implement Rate Limiting:**
   ```bash
   pip install flask-limiter
   ```

4. **Add CSRF Protection:**
   ```bash
   pip install flask-talisman
   ```

5. **Database Backup:**
   ```bash
   pg_dump -U postgres ismail_bot > backup.sql
   ```

6. **Monitor Access Logs:**
   ```bash
   tail -f /var/log/ismail-bot.log
   ```

### Passwords & Credentials

⚠️ **NEVER commit these to Git:**
- `.env` file
- `accounts.json`
- Database passwords
- API keys

**Add to `.gitignore`:**
```
.env
.env.local
accounts.json
*.log
venv/
__pycache__/
```

---

## 🧪 Testing & Debugging

### Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_crypto.py -v

# Run with coverage
pytest --cov=ISMAIL_BOT tests/
```

### Integration Tests

```bash
# Test bot + database interaction
pytest tests/integration/ -v

# Test web API endpoints
pytest tests/test_api.py -v
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load test
locust -f tests/locustfile.py --host=http://localhost:5000

# Visit http://localhost:8089 in browser
```

### Debugging

**Enable Debug Mode (Development Only):**

```env
LOG_LEVEL=DEBUG
FLASK_DEBUG=True  # NEVER in production!
```

**Check Bot Status:**

```bash
# See if bot is running
ps aux | grep python

# View bot logs
tail -f bot.log

# Test bot connection
python -c "from ISMAIL_BOT.main import bot; bot.test_connection()"
```

**Database Debugging:**

```bash
# Connect to database
psql -U postgres -d ismail_bot

# List tables
\dt

# View player count
SELECT COUNT(*) FROM waitlist;

# Clear test data
DELETE FROM waitlist WHERE created_at < NOW() - INTERVAL '7 days';
```

---

## 📤 Deployment Options

### Cloud Deployment

#### Heroku
```bash
heroku create ismail-bot
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set $(cat .env | tr '\n' ' ')
git push heroku main
```

#### AWS
- EC2 for bot (t3.medium)
- RDS for PostgreSQL
- ALB for load balancing
- CloudWatch for monitoring

#### Google Cloud
- Compute Engine for bot
- Cloud SQL for PostgreSQL
- Load Balancer
- Stackdriver Logging

### On-Premise Deployment

```bash
# Server requirements: Ubuntu 20.04 LTS, 4GB RAM, 100GB SSD

# 1. Setup server
sudo apt update && sudo apt upgrade -y
sudo apt install python3.9 postgresql postgresql-contrib git -y

# 2. Clone repo
git clone https://github.com/ISMAILdz13/FF-bot.git
cd FF-bot

# 3. Install
python3.9 -m venv venv
source venv/bin/activate
pip install -r ISMAIL_BOT/requirements.txt
pip install -r website/requirements.txt

# 4. Configure
cp .env.example .env
nano .env

# 5. Setup systemd
sudo cp ismail-bot.service /etc/systemd/system/
sudo systemctl enable ismail-bot
sudo systemctl start ismail-bot

# 6. Monitor
sudo journalctl -u ismail-bot -f
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `psycopg2.OperationalError` | Database not running | `sudo systemctl start postgresql` |
| `ModuleNotFoundError: No module named 'flask'` | Dependencies not installed | `pip install -r website/requirements.txt` |
| `Address already in use` | Port 5000 in use | `lsof -i :5000` then `kill -9 <PID>` |
| `SSL certificate verification failed` | Self-signed certificate | Set `REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt` |
| `Bot won't connect` | Token expired | Token auto-refreshes; check `LOG_LEVEL=DEBUG` |
| `Dashboard won't load` | Flask not started | Run `python website/app.py` in separate terminal |

### Getting Logs

**Bot Logs:**
```bash
# Real-time
python ISMAIL_BOT/main.py | tee bot.log

# View existing
cat bot.log | tail -50
```

**Web Logs:**
```bash
# View Flask logs
python website/app.py 2>&1 | grep -i error
```

**Database Logs:**
```bash
# PostgreSQL
sudo tail -f /var/log/postgresql/postgresql.log
```

---

## 🤝 Contributing & Support

### How to Contribute

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/FF-bot.git
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make changes & test**
   ```bash
   pytest tests/ -v
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "feat: add new feature" 
   # Use: feat, fix, docs, style, refactor, test, chore
   ```

5. **Push & create Pull Request**
   ```bash
   git push origin feature/your-feature
   ```

### Getting Help

| Type | How | Where |
|------|-----|-------|
| **Bugs** | Create Issue | [GitHub Issues](https://github.com/ISMAILdz13/FF-bot/issues) |
| **Features** | Discussion | [GitHub Discussions](https://github.com/ISMAILdz13/FF-bot/discussions) |
| **Security** | Private Report | [Security Policy](./SECURITY.md) |

---

## 📄 Legal & License

### ⚠️ Legal Disclaimer

This bot is designed for automated gameplay in Free Fire. **Usage must comply with:**

- ✅ Free Fire Terms of Service
- ✅ Garena's API usage policies  
- ✅ Local gaming regulations
- ✅ No cheating or unfair advantages

**Risks:**
- ⚠️ Account may be banned by Garena/Free Fire
- ⚠️ Penalties may apply per TOS
- ⚠️ Authors not responsible for consequences

**Fair Use Policy:**
This tool is for:
- Educational purposes
- Personal use
- Testing game mechanics

**NOT for:**
- Commercial profit
- Selling accounts/items
- Competitive advantage in tournaments

### License

```
MIT License

Copyright (c) 2026 ISMAIL-BOT Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND...
```

**Full License:** See [LICENSE.md](./LICENSE.md)

---

## 📊 Version History

### v2.0.0 (Current - March 2026)

✅ Removed all Replit-specific configuration  
✅ De-obfuscated code for better maintainability  
✅ Enhanced security with AES-256 encryption  
✅ Portable shell scripts (cross-platform)  
✅ Comprehensive documentation  
✅ Docker support  
✅ Systemd service configuration  

### v1.0.0 (Initial - January 2026)

- Replit-based release
- Basic bot functionality
- Simple Flask dashboard
- PostgreSQL integration

---

## ❓ FAQ

<details>
<summary><strong>Q: Why was the code de-obfuscated?</strong></summary>

**A:** Improved maintainability, easier security auditing, and simpler debugging for contributors.
</details>

<details>
<summary><strong>Q: Is this safe to use?</strong></summary>

**A:** The bot itself is secure (AES-256 encryption), but usage against Garena's Terms of Service may result in account bans. Not recommended for your main account.
</details>

<details>
<summary><strong>Q: Can I run this without PostgreSQL?</strong></summary>

**A:** Currently no - PostgreSQL is required for the waitlist database. SQLite support could be added if needed. Submit a feature request!
</details>

<details>
<summary><strong>Q: How often do tokens refresh?</strong></summary>

**A:** Automatically every 5 hours via the `fetch_tokens()` background task. No manual action needed.
</details>

<details>
<summary><strong>Q: What if I see "SSL certificate verification failed"?</strong></summary>

**A:** Expected in development. For production: use verified SSL certificates or run behind a proxy (nginx, Apache). Development: Set `REQUESTS_CA_BUNDLE` environment variable.
</details>

<details>
<summary><strong>Q: Can I run multiple bots simultaneously?</strong></summary>

**A:** Yes! Each bot needs unique credentials in `accounts.json` and its own config. Use separate ports for web dashboards (5000, 5001, 5002, etc.).
</details>

<details>
<summary><strong>Q: How do I update the bot?</strong></summary>

**A:** 
```bash
git pull origin main
pip install -r ISMAIL_BOT/requirements.txt --upgrade
systemctl restart ismail-bot
```
</details>

<details>
<summary><strong>Q: Is there a Windows version?</strong></summary>

**A:** Yes! All features work on Windows. Use Python 3.9+ and PostgreSQL for Windows. Run scripts with PowerShell instead of Bash.
</details>

---

## 👤 Credits

| Role | Contributor |
|------|-------------|
| **Original Developer** | AbdeeLkarim BesTo (@ISMAIL_FF) |
| **Collaborators** | DAJAL FF, C4 Team |
| **De-obfuscation & Modernization** | 2026 Improvements |
| **Documentation** | Community Contributors |

---

## 📞 Contact & Social

- 🐙 **GitHub**: [ISMAILdz13/FF-bot](https://github.com/ISMAILdz13/FF-bot)
- ⭐ **Stars**: Help by starring the repo!
- 🐛 **Issues**: Report bugs or request features
- 💬 **Discussions**: Join the community

---

**Last Updated:** March 2026  
**Latest Version:** 2.0.0  
**Status:** ✅ Production-Ready (with proper configuration)

```
    ╔═══════════════════════════════════╗
    ║   ISMAIL-BOT™ - Free Fire Bot     ║
    ║   Version 2.0.0                   ║
    ║   © 2026 - All Rights Reserved    ║
    ╚═══════════════════════════════════╝
```
