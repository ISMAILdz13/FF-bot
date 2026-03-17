ISMAIL-BOT™ - Free Fire Game Automation Bot
A sophisticated Free Fire game bot with web-based squad management dashboard and support for various game automation features.

📋 Overview
ISMAIL-BOT is a Free Fire game automation tool featuring:

Game Bot: Automated gameplay with squad management, messaging, emotes, and player profile interactions
Web Dashboard: Flask-based interface for player waitlist management and administrator controls
Instagram API Module: Fetch public Instagram user profiles
PostgreSQL Backend: Persistent database for player management and statistics
Components
ISMAIL_BOT/
├── main.py           # Core bot logic and game client
├── config.py         # Configuration management (environment-based)
├── crypto.py         # AES encryption & protobuf packet building (de-obfuscated)
├── helpers.py        # API calls & player info fetching (de-obfuscated)
├── APIS/
│   └── insta.py     # Instagram profile data scraper
├── Pb2/             # Compiled protobuf message definitions
└── accounts.json    # Account credentials storage

website/
├── app.py           # Flask web application
├── static/          # CSS, JS, images
└── templates/       # HTML templates (login, waitlist, admin panel)
🚀 Quick Start
Prerequisites
Python 3.9 or higher
PostgreSQL 12+ (local or remote)
pip/poetry for dependency management
Installation
Clone/Extract the repository

cd ISMAILBOTzip
Create a Python virtual environment

# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using poetry
poetry install
Install dependencies

pip install -r ISMAIL_BOT/requirements.txt
Configure environment variables

# Copy template
cp .env.example .env

# Edit .env with your values
nano .env  # or your preferred editor
Set up PostgreSQL database

# Create database
createdb ismail_bot

# Run migrations (if available) or create tables manually
# See Database Schema section below
Test the installation

# Test bot module
python -m ISMAIL_BOT.main --test

# Test website
python website/app.py
⚙️ Configuration
Environment Variables
Create a .env file in the project root with the following variables:

# ========== BOT CONFIGURATION ==========
BOT_NAME=ISMAIL-BOT™
ADMIN_UID=your_admin_uid_here
BOT_UID=your_bot_uid_here
BOT_SERVER=BD                          # Server region (BD/IND/US)
BOT_KEY=your_bot_key_here
BYPASS_TOKEN=your_bypass_token_here

# ========== TIMING SETTINGS ==========
START_SPAM_DURATION=18                 # Seconds
WAIT_AFTER_MATCH=20                    # Seconds
START_SPAM_DELAY=0.2                   # Seconds

# ========== LOGGING ==========
LOG_LEVEL=INFO                         # DEBUG/INFO/WARNING/ERROR

# ========== FLASK WEB CONFIGURATION ==========
FLASK_SECRET_KEY=<generate_with_secrets.token_hex(32)>
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False                      # Never True in production

# ========== DATABASE CONFIGURATION ==========
DATABASE_URL=postgresql://user:password@localhost:5432/ismail_bot

# ========== SECURITY ACCESS CODES ==========
MAIN_ACCESS_CODE=your_main_code_here   # 15-digit code for main waitlist access
DEV_ACCESS_CODE=your_dev_code_here     # Code for developer dashboard access
Database Schema
Create the PostgreSQL tables:

CREATE TABLE IF NOT EXISTS waitlist (
    id SERIAL PRIMARY KEY,
    player_id VARCHAR(20) NOT NULL UNIQUE,
    player_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',  -- pending, accepted, rejected
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bot_accounts (
    id SERIAL PRIMARY KEY,
    bot_uid VARCHAR(20) NOT NULL UNIQUE,
    bot_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS admin_logs (
    id SERIAL PRIMARY KEY,
    action VARCHAR(100),
    player_id VARCHAR(20),
    details TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
🎮 Running the Bot
Option 1: Direct Execution
Start the Game Bot

cd ISMAILBOTzip
python ISMAIL_BOT/main.py
Start the Web Dashboard

cd ISMAILBOTzip
python website/app.py
Option 2: Using shell scripts (with auto-restart)
Start both services

# In separate terminals:
bash run_bot.sh      # Auto-restarts bot on crash
bash run_website.sh  # Auto-restarts website on crash
Option 3: Using Docker
# Build
docker build -t ismail-bot .

# Run
docker run --env-file .env -p 5000:5000 -p 5001:5001 ismail-bot
Option 4: Production with systemd
Create /etc/systemd/system/ismail-bot.service:

[Unit]
Description=ISMAIL-BOT Game Bot
After=network.target postgresql.service

[Service]
Type=simple
User=ismail
WorkingDirectory=/opt/ismail-bot
ExecStart=/usr/bin/python3 ISMAIL_BOT/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
Enable and start:

sudo systemctl enable ismail-bot
sudo systemctl start ismail-bot
🌐 Web Dashboard
Accessing the Dashboard
URL: http://localhost:5000
Main Waitlist: Use MAIN_ACCESS_CODE from .env
Developer Panel: Use DEV_ACCESS_CODE from .env
Features
Player Access

Enter Free Fire player ID
Get status updates
View acceptance/rejection status
Developer/Admin Panel

View all waitlist entries
Accept/reject player requests
Generate bot invites
View bot statistics and logs
🔑 API Endpoints
Public Endpoints
GET / - Main login page
POST / - Submit waitlist codes
GET /start - Player status page
Admin Endpoints
GET /dev - Developer dashboard (requires dev access code)
POST /api/status/<player_id> - Get player status
POST /api/accept/<player_id> - Accept player
POST /api/reject/<player_id> - Reject player
🛡️ Security Considerations
Current Implementation
✅ AES-256 encryption for network packets
✅ Environment-based configuration (no hardcoded secrets)
✅ Parameterized SQL queries (protects against injection)
✅ Secure session cookies (HttpOnly, SameSite=Lax)
Recommendations for Production
Enable HTTPS

FLASK_SESSION_SECURE=True  # Requires HTTPS
Use stronger Flask secret

python -c "import secrets; print(secrets.token_hex(32))"
Implement rate limiting

pip install flask-limiter
Add CSRF protection

pip install flask-talisman
Database connection pooling (already implemented in code)

Add admin action logging (already implemented)

🧪 Testing
Unit Tests
pytest tests/
Integration Tests
pytest tests/integration/
Load Testing
locust -f tests/locustfile.py
📊 Project Structure
ISMAILBOTzip/
├── .env.example              # Template for environment variables
├── .git/                     # Git repository (not Replit-specific)
├── .gitignore               # Git ignore file
├── main.py                  # Entry point (minimal wrapper)
├── pyproject.toml           # Python project metadata (non-Replit)
├── run_bot.sh              # Start bot (PORTABLE - no hardcoded paths)
├── run_website.sh          # Start website (PORTABLE)
├── README.md               # This file
│
├── ISMAIL_BOT/             # Bot application package
│   ├── __init__.py
│   ├── config.py           # Environment-based configuration
│   ├── main.py             # Core bot logic
│   ├── crypto.py           # AES encryption & protobuf (de-obfuscated)
│   ├── helpers.py          # API functions (de-obfuscated)
│   ├── accounts.json       # Account credentials
│   ├── requirements.txt    # Python dependencies
│   ├── install.sh          # Installation script
│   ├── package.json        # Node.js dependencies (legacy)
│   │
│   ├── APIS/               # External API modules
│   │   ├── __init__.py
│   │   └── insta.py        # Instagram profile scraper
│   │
│   └── Pb2/                # Protobuf message definitions (auto-generated)
│       ├── DEcwHisPErMsG_pb2.py
│       ├── MajoRLoGinrEs_pb2.py
│       ├── Team_msg_pb2.py
│       └── ... (other protobuf files)
│
├── website/                # Flask web application
│   ├── app.py             # Flask app initialization & routes
│   ├── requirements.txt    # Flask dependencies
│   ├── static/            # CSS, JavaScript, images
│   │   ├── style.css
│   │   └── script.js
│   └── templates/         # Jinja2 HTML templates
│       ├── base.html      # Base layout
│       ├── login.html     # Login page
│       ├── start.html     # Waitlist submission
│       ├── dev_area.html  # Developer dashboard
│       └── dev_stats.html # Statistics page
│
└── docs/                  # Documentation (can be added)
    ├── API.md
    ├── ARCHITECTURE.md
    └── TROUBLESHOOTING.md
🔄 Migration from Replit
What Changed
Shell Scripts: Removed hardcoded /home/runner/workspace → Now use $(pwd) for portability
Configuration: All secrets moved to .env file (not in source code)
Code Quality: De-obfuscated modules for better maintainability:
xC4.py → crypto.py (encryption functions)
xHeaders.py → helpers.py (API functions)
Session Security: Added HTTPOnly and SameSite cookie flags
Removed Files:
.replit (Replit-specific configuration) - DELETE THIS FILE
replit.md (replaced by README.md)
Running on Different Platforms
Windows (PowerShell)

# Bot
python ISMAIL_BOT/main.py

# Website
python website/app.py
Linux/macOS (Bash)

# Using shell scripts
bash run_bot.sh &
bash run_website.sh &

# Or direct Python
python3 ISMAIL_BOT/main.py &
python3 website/app.py &
Docker Compose

docker compose up
🤝 Contributing
Create a feature branch: git checkout -b feature/your-feature
Make your changes
Test thoroughly
Commit with descriptive messages
Push to your fork and submit a Pull Request
📝 Changelog
v2.0.0 (Current)
✅ Removed all Replit-specific traces
✅ De-obfuscated code for maintainability
✅ Enhanced security configuration
✅ Portable shell scripts
✅ Comprehensive documentation
v1.0.0
Initial Replit-based release
⚠️ Legal Disclaimer
This bot is designed for automated gameplay in Free Fire. Usage should comply with:

Free Fire Terms of Service
Garena's API usage policies
Local gaming regulations
The authors are not responsible for account bans or penalties from using this bot.

📞 Support & Feedback
Bug Reports: Create an issue on GitHub
Feature Requests: Open a discussion thread
Security Issues: Please report privately to maintainers
📄 License
This project is provided as-is for personal and educational use only. You may modify and distribute with proper attribution.

👤 Credits
Original Developer: AbdeeLkarim BesTo (@ISMAIL_FF)
Collaborators: DAJAL FF, C4 Team
De-obfuscation & Modernization: 2025 Improvements
❓ FAQ
Q: Why was the code de-obfuscated?
A: Improved maintainability, security auditing, and easier debugging.

Q: Is this safe to use?
A: The bot handles encryption securely, but usage against Garena's TOS may result in account bans.

Q: Can I run this without PostgreSQL?
A: Not currently (required for waitlist storage). Support for SQLite can be added.

Q: How often do I need to update tokens?
A: Tokens are automatically refreshed every 5 hours by the fetch_tokens() background task.

Q: What if I see "SSL certificate verification failed"?
A: This is expected for development. In production, either use verified certificates or run behind a proxy.

Last Updated: March 2025
Version: 2.0.0
Status: ✅ Production-Ready (with proper configuration)
