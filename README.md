<div align="center">

<!-- Animated Banner SVG -->
![](assets/banner.svg)

<!-- Badges -->
<img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Flask-Dashboard-green?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/AES--256-Encryption-red?style=for-the-badge" alt="Encryption"/>
<img src="https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
<img src="https://img.shields.io/badge/Version-2.0.0-orange?style=for-the-badge" alt="Version"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
<img src="https://img.shields.io/github/stars/ISMAILdz13/FreeFireGameBot?style=for-the-badge" alt="Stars"/>

<!-- Animated Status -->
![](assets/status-badge.svg)

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

![](assets/architecture.svg)

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
git clone https://github.com/ISMAILdz13/FreeFireGameBot.git
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
- **Repository**: [github.com/ISMAILdz13/FreeFireGameBot](https://github.com/ISMAILdz13/FreeFireGameBot)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

---

<div align="center">

![](assets/footer.svg)

⭐ **Star this repo if it helped you!** ⭐

</div>
