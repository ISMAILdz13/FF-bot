<div align="center">

<!-- Animated Banner SVG -->
<svg xmlns="http://www.w3.org/2000/svg" width="700" height="160" viewBox="0 0 700 160">
  <defs>
    <linearGradient id="botBanner" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1">
        <animate attributeName="offset" values="0;0.5;0" dur="4s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" style="stop-color:#764ba2;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#f5576c;stop-opacity:1">
        <animate attributeName="offset" values="1;0.5;1" dur="4s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
    <filter id="botGlow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="700" height="160" rx="25" fill="url(#botBanner)"/>
  <text x="350" y="65" font-family="monospace" font-size="28" font-weight="bold" fill="white" text-anchor="middle" filter="url(#botGlow)">ISMAIL-BOT</text>
  <text x="350" y="100" font-family="monospace" font-size="14" fill="white" text-anchor="middle" opacity="0.9">Free Fire Game Bot | Flask Dashboard | v2.0.0</text>
  <circle cx="60" cy="40" r="8" fill="white" opacity="0.5">
    <animate attributeName="opacity" values="0.5;0.1;0.5" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="r" values="8;12;8" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="640" cy="120" r="6" fill="white" opacity="0.3">
    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="120" cy="130" r="4" fill="white" opacity="0.4">
    <animate attributeName="opacity" values="0.4;0.9;0.4" dur="3s" repeatCount="indefinite"/>
  </circle>
  <rect x="200" y="115" width="300" height="4" rx="2" fill="white" opacity="0.2">
    <animate attributeName="width" values="100;300;100" dur="5s" repeatCount="indefinite"/>
    <animate attributeName="x" values="300;200;300" dur="5s" repeatCount="indefinite"/>
  </rect>
</svg>

<!-- Badges -->
<img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Flask-Dashboard-green?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/AES--256-Encryption-red?style=for-the-badge" alt="Encryption"/>
<img src="https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
<img src="https://img.shields.io/badge/Version-2.0.0-orange?style=for-the-badge" alt="Version"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
<img src="https://img.shields.io/github/stars/ISMAILdz13/ff-game-bot?style=for-the-badge" alt="Stars"/>

<!-- Animated Status -->
<svg xmlns="http://www.w3.org/2000/svg" width="180" height="28" viewBox="0 0 180 28">
  <rect width="180" height="28" rx="14" fill="#2D2D2D" stroke="#667eea" stroke-width="1.5">
    <animate attributeName="stroke" values="#667eea;#f5576c;#667eea" dur="3s" repeatCount="indefinite"/>
  </rect>
  <circle cx="14" cy="14" r="5" fill="#43e97b">
    <animate attributeName="r" values="5;7;5" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <text x="30" y="18" font-family="monospace" font-size="10" fill="#43e97b" font-weight="bold">PRODUCTION READY</text>
</svg>

</div>

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Features](#-features)
3. [Architecture](#-architecture)
4. [Installation](#-installation)
5. [Configuration](#-configuration)
6. [Running the Bot](#-running-the-bot)
7. [Web Dashboard](#-web-dashboard)
8. [API Reference](#-api-reference)
9. [OB54-TCP-BOT Module](#-ob54-tcp-bot-module)
10. [FAQ](#-faq)
11. [Credits](#-credits)

---

## 🔥 Overview

**ISMAIL-BOT** is an automated game bot for **Free Fire** with an integrated Flask web dashboard for squad management, player waitlist handling, and administrative controls.

| Component | Purpose |
|-----------|---------|
| **Game Bot** | Automates gameplay, squad management, messaging, emotes |
| **Web Dashboard** | Flask interface for managing players and waitlists |
| **Instagram API** | Scrapes public Instagram profiles for verification |
| **PostgreSQL** | Stores player data, bot accounts, and activity logs |
| **Encryption** | AES-256 for secure network communication |
| **OB54-TCP-BOT** | Direct TCP socket communication with game servers |

---

## ✨ Features

### Game Bot
- 🤖 Squad management — auto-join squads, manage teammates
- 💬 Messaging — send automated messages and emotes
- 👤 Player profiles — fetch and display player statistics
- 🔄 Token refresh — auto-refresh auth tokens every 5 hours
- 🌐 Multi-server — BD, IND, US, ME regions
- 🔐 AES-256 encryption for all packets

### Web Dashboard
- 📋 Player waitlist — submit and track join requests
- 👑 Admin panel — accept/reject players, manage bot accounts
- 📊 Statistics — bot usage metrics and performance logs
- 🔒 Two-tier authentication (main user + admin)
- 📝 Activity logs — track all administrative actions

---

## 📊 Architecture

<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="300" viewBox="0 0 680 300">
  <defs>
    <linearGradient id="archGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea"/>
      <stop offset="100%" style="stop-color:#764ba2"/>
    </linearGradient>
    <linearGradient id="archGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f093fb"/>
      <stop offset="100%" style="stop-color:#f5576c"/>
    </linearGradient>
    <linearGradient id="archGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4facfe"/>
      <stop offset="100%" style="stop-color:#00f2fe"/>
    </linearGradient>
    <filter id="archShadow"><feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.3"/></filter>
    <marker id="archArrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <text x="340" y="25" font-family="monospace" font-size="14" font-weight="bold" fill="#333" text-anchor="middle">System Architecture</text>

  <!-- Flask Dashboard -->
  <rect x="20" y="50" width="160" height="60" rx="12" fill="url(#archGrad1)" filter="url(#archShadow)"/>
  <text x="100" y="78" font-family="monospace" font-size="11" fill="white" text-anchor="middle" font-weight="bold">Flask Dashboard</text>
  <text x="100" y="95" font-family="monospace" font-size="9" fill="white" text-anchor="middle">Admin + Waitlist</text>

  <!-- Core Bot -->
  <rect x="240" y="50" width="160" height="60" rx="12" fill="url(#archGrad2)" filter="url(#archShadow)"/>
  <text x="320" y="78" font-family="monospace" font-size="11" fill="white" text-anchor="middle" font-weight="bold">ISMAIL-BOT</text>
  <text x="320" y="95" font-family="monospace" font-size="9" fill="white" text-anchor="middle">Game Logic + Auth</text>

  <!-- TCP Module -->
  <rect x="460" y="50" width="160" height="60" rx="12" fill="url(#archGrad3)" filter="url(#archShadow)"/>
  <text x="540" y="78" font-family="monospace" font-size="11" fill="white" text-anchor="middle" font-weight="bold">OB54-TCP</text>
  <text x="540" y="95" font-family="monospace" font-size="9" fill="white" text-anchor="middle">Socket + Packets</text>

  <!-- Arrows -->
  <line x1="180" y1="80" x2="235" y2="80" stroke="#666" stroke-width="2" marker-end="url(#archArrow)"/>
  <line x1="400" y1="80" x2="455" y2="80" stroke="#666" stroke-width="2" marker-end="url(#archArrow)"/>

  <!-- PostgreSQL -->
  <rect x="80" y="160" width="160" height="50" rx="12" fill="#336791" filter="url(#archShadow)"/>
  <text x="160" y="190" font-family="monospace" font-size="11" fill="white" text-anchor="middle" font-weight="bold">PostgreSQL</text>

  <!-- Garena API -->
  <rect x="300" y="160" width="160" height="50" rx="12" fill="#FF4B2B" filter="url(#archShadow)"/>
  <text x="380" y="190" font-family="monospace" font-size="11" fill="white" text-anchor="middle" font-weight="bold">Garena Servers</text>

  <!-- Game TCP -->
  <rect x="500" y="160" width="120" height="50" rx="12" fill="#2D2D2D" stroke="#4facfe" stroke-width="1.5" filter="url(#archShadow)">
    <animate attributeName="stroke" values="#4facfe;#00f2fe;#4facfe" dur="2s" repeatCount="indefinite"/>
  </rect>
  <text x="560" y="190" font-family="monospace" font-size="11" fill="#4facfe" text-anchor="middle" font-weight="bold">TCP Socket</text>

  <!-- Arrows down -->
  <line x1="320" y1="110" x2="160" y2="155" stroke="#666" stroke-width="1.5" marker-end="url(#archArrow)"/>
  <line x1="320" y1="110" x2="380" y2="155" stroke="#666" stroke-width="1.5" marker-end="url(#archArrow)"/>
  <line x1="540" y1="110" x2="560" y2="155" stroke="#666" stroke-width="1.5" marker-end="url(#archArrow)"/>

  <!-- Encryption layer -->
  <rect x="180" y="240" width="320" height="40" rx="10" fill="#2D2D2D" stroke="#f5576c" stroke-width="1.5">
    <animate attributeName="stroke" values="#f5576c;#667eea;#f5576c" dur="2s" repeatCount="indefinite"/>
  </rect>
  <text x="340" y="265" font-family="monospace" font-size="11" fill="#f5576c" text-anchor="middle" font-weight="bold">AES-256 Encryption Layer</text>
</svg>

</div>

---

## 📦 Installation

<details>
<summary><b>Prerequisites</b></summary>

<br>

- Python 3.11+
- PostgreSQL 14+
- Node.js 18+ (for OB54-TCP-BOT server)
- pip, npm

</details>

<details open>
<summary><b>Quick Setup</b></summary>

<br>

```bash
# Clone
git clone https://github.com/ISMAILdz13/ff-game-bot.git
cd ff-game-bot

# Install Python dependencies
pip install -r ISMAILBOTzip/ISMAIL_BOT/requirements.txt

# Set up PostgreSQL
createdb ismail_bot
psql -U postgres -d ismail_bot -f database.sql

# Configure environment
cp ISMAILBOTzip/ISMAIL_BOT/config.py.example ISMAILBOTzip/ISMAIL_BOT/config.py
# Edit config.py with your database URL and bot credentials

# Run the bot
python ISMAILBOTzip/ISMAIL_BOT/main.py &

# Run the web dashboard
python ISMAILBOTzip/website/app.py
```

</details>

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://user:password@localhost/ismail_bot` | PostgreSQL connection string |
| `BOT_NAME` | `ISMAIL-BOT™` | Display name for the bot |
| `TOKEN_REFRESH_INTERVAL` | `18000` (5 hours) | Auto-refresh interval in seconds |
| `SERVER_REGION` | `ME` | Default server region |

---

## 🎮 Running the Bot

```bash
# Start the bot
python ISMAILBOTzip/ISMAIL_BOT/main.py

# Start the web dashboard (separate terminal)
python ISMAILBOTzip/website/app.py

# Or use the run scripts
bash ISMAILBOTzip/run_bot.sh
bash ISMAILBOTzip/run_website.sh

# Run the TCP module
cd OB54-TCP-BOT && node server.js
```

---

## 🌐 Web Dashboard

The Flask dashboard provides:
- **Player Waitlist** — users submit join requests
- **Admin Panel** — accept/reject players, view stats
- **Bot Management** — add/remove bot accounts
- **Activity Logs** — track all admin actions

Access at `http://localhost:5000` (default)

---

## 📡 API Reference

<details>
<summary><b>Bot Commands</b></summary>

<br>

| Command | Description |
|---------|-------------|
| `/infox <uid>` | Fetch detailed player info |
| `/praisa <name>` | Send 17 positive messages with emotes |
| `/emote <emote_id>` | Send a specific emote |
| `/join <team_code>` | Join a squad |
| `/leave` | Leave current squad |

</details>

---

## 🔧 OB54-TCP-BOT Module

The `OB54-TCP-BOT/` directory contains the TCP communication module:

| File | Purpose |
|------|---------|
| `main.py` | Main TCP bot logic |
| `server.js` | Express.js wrapper server |
| `xC4.py` | AES encryption module |
| `xHeaders.py` | HTTP header construction |
| `Pb2/` | Compiled protobuf definitions |
| `emotes.json` | Emote ID mappings |

See [OB54-TCP-BOT/README.md](OB54-TCP-BOT/README.md) for details.

---

## ❓ FAQ

<details>
<summary><b>How often are tokens refreshed?</b></summary>

Tokens auto-refresh every 5 hours via the `fetch_tokens()` background task.

</details>

<details>
<summary><b>What regions are supported?</b></summary>

BD (Bangladesh), IND (India), US, ME (Middle East).

</details>

<details>
<summary><b>Is PostgreSQL required?</b></summary>

Yes, for waitlist and admin storage. SQLite support can be added.

</details>

<details>
<summary><b>What if I get SSL errors?</b></summary>

Expected in development. Use verified certificates or a reverse proxy in production.

</details>

---

## 📁 Project Structure

```
ff-game-bot/
├── README.md
├── LICENSE
├── .gitignore
├── ISMAILBOTzip/
│   ├── ISMAIL_BOT/              # Core bot application
│   │   ├── main.py              # Main bot logic
│   │   ├── config.py            # Configuration
│   │   ├── crypto.py             # AES encryption
│   │   ├── helpers.py            # Helper functions
│   │   ├── xC4.py               # Legacy encryption
│   │   ├── xHeaders.py          # Legacy headers
│   │   ├── APIS/                # External API integrations
│   │   └── Pb2/                 # Protobuf definitions
│   ├── website/                 # Flask web dashboard
│   │   ├── app.py
│   │   └── templates/
│   ├── main.py                  # Entry point
│   ├── README.md
│   ├── CLEANUP.md
│   ├── IMPROVEMENTS.md
│   ├── MIGRATION.md
│   └── QUICKSTART.md
└── OB54-TCP-BOT/                # TCP communication module
    ├── main.py
    ├── server.js
    ├── xC4.py
    ├── Pb2/
    └── README.md
```

---

## 👤 Credits

- **Developer**: ISMAILdz13 (@ISMAILdz13)
- **Repository**: [github.com/ISMAILdz13/ff-game-bot](https://github.com/ISMAILdz13/ff-game-bot)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

---

<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" width="500" height="50" viewBox="0 0 500 50">
  <defs>
    <linearGradient id="footerG" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:0">
        <animate attributeName="offset" values="0;1;0" dur="5s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" style="stop-color:#f5576c;stop-opacity:0">
        <animate attributeName="offset" values="1;0;1" dur="5s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
  </defs>
  <rect x="30" y="20" width="440" height="2" rx="1" fill="url(#footerG)"/>
  <text x="250" y="42" font-family="monospace" font-size="10" fill="#666" text-anchor="middle">Python + Flask + PostgreSQL + AES-256 | by ISMAILdz13</text>
</svg>

⭐ **Star this repo if it helped you!** ⭐

</div>
