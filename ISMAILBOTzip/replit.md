# Ismail Bot & Website

A Free Fire game bot with a premium waitlist management website featuring modern UI and sidebar navigation.

## 🎮 Bot Features (ISMAIL_BOT/main.py)
- **Commands**: `/help`, `/info`, `/bio`, `/likes`, `/ai`, `/join`, `/ghost`, `/lag`, `/alltitles`, `/spam`, `/evo`, `/ig`, `/check`
- **Auto Features**: Automatic squad acceptance, emote responses, evolution emote support
- **Connectivity**: TCP connection to Free Fire servers with full packet handling
- **Admin Controls**: Commands restricted to admin UID for security
- **Logger**: Built-in logging system for tracking bot activity

## 🌐 Website Features (website/app.py)

### Design & UX
- **Sidebar Navigation**: Left-side persistent menu for easy access
- **Modern Dark Theme**: Gradient backgrounds with neon cyan accents (#00bfff)
- **Responsive Design**: Mobile, tablet, and desktop optimized
- **Smooth Animations**: Hover effects and transitions on all interactive elements
- **Glass-morphism**: Backdrop blur effects on cards

### Public Area (Main Code: `1460738025351811104`)
- Join waitlist with Free Fire Player ID
- Real-time status feedback (pending, accepted, rejected)
- Input validation (5+ digits required)
- Descriptive messaging for next steps after acceptance

### Developer Area (Dev Code: `3476575559`)
- **Player Management Dashboard**
  - View all applications in organized table
  - Status badges with color coding
  - Timestamps for all submissions
  - Accept/Reject buttons for each entry
  
- **Advanced Filtering**
  - Filter by: Pending, Accepted, Rejected, All
  - Shows count badges for quick overview
  - Real-time stats in filter buttons
  
- **Statistics Dashboard**
  - Total applications counter
  - Pending applications count
  - Accepted players count
  - Rejected applications count
  - Quick action links

## 🔐 Access Credentials
- **Main Code**: `1460738025351811104` (for players)
- **Dev Code**: `3476575559` (for admin management)
- **Bot UID**: `14881602318` (ISMAIL-BOT™)
- **Admin UID**: `8804135237`

## 📁 Project Structure
```
ISMAIL_BOT/
├── main.py              (Bot core logic with logger)
├── requirements.txt     (Dependencies)
├── xC4.py              (Authentication)
├── xHeaders.py         (Headers)
├── xKEys.py            (Keys)
└── Pb2/                (Protocol buffers)

website/
├── app.py              (Flask server - 175+ lines)
├── templates/
│   ├── base.html       (Sidebar template - shared layout)
│   ├── login.html      (Access code entry)
│   ├── start.html      (Player signup)
│   ├── dev_area.html   (Admin player management)
│   └── dev_stats.html  (Statistics dashboard)
```

## 🚀 Running the Project
- **Bot Workflow**: `python3 ISMAIL_BOT/main.py`
- **Website Workflow**: `python3 website/app.py` (Port 5000)

Both workflows are configured and ready to use.

## ✨ Recent Improvements

### Bug Fixes (March 2026)
- ✅ Fixed `/e` command catching `/evo`, `/evos`, `/emot`, `/emote` (changed startswith to exact word match)
- ✅ Synced `EMOTE_MAP` and `evo_emotes` — both now use identical, correct emote IDs (1-21)
- ✅ Added emotes 19 (AUG), 20 (MP5), 21 (SVD) to both maps
- ✅ Bundle command now accepts numeric IDs directly (`/bundle 914000002`)
- ✅ Added "pinball" as bundle alias
- ✅ `SEndPacKeT` now raises real exceptions when connections are None (no more false "Message sent" logs)
- ✅ `SEndMsG` raises on unknown chat type instead of silent UnboundLocalError
- ✅ Auth retry loop no longer hammers Garena (30s delay on 429, 10s backoff in restart loop)
- ✅ `/lw` runs silently (status only every 5 cycles, not every join/start/wait/leave)
- ✅ Website configured for production deployment (gunicorn, autoscale)
- ✅ Fixed `requirements.txt` (`flask` and `python-dotenv` were merged into one invalid line)

### Website (Earlier)
- ✅ Gorgeous sidebar navigation (persistent, responsive)
- ✅ Dark theme with neon cyan accents
- ✅ Statistics dashboard with real-time counts
- ✅ Mobile responsive UI (works on all devices)
- ✅ Enhanced input validation and error messages
- ✅ Color-coded status badges in tables
- ✅ Database connection pooling for performance
- ✅ Bot logger for activity tracking
- ✅ Clean code organization and documentation
- ✅ Session management with logout functionality

## 🎨 UI/UX Highlights
- Gradient backgrounds (deep blue to dark purple)
- Smooth transitions and hover effects
- Neon cyan accent colors for contrast
- Glass-morphism cards with backdrop blur
- Color-coded action buttons (green/red)
- Emoji indicators for quick visual feedback
- Responsive grid layouts
- Custom scrollbars matching theme

## 📊 Technology Stack
- **Backend**: Python (Flask)
- **Database**: PostgreSQL
- **Frontend**: HTML5/CSS3 with responsive design
- **Bot**: Python (asyncio) with TCP sockets
- **Styling**: Custom CSS with gradients and animations

## 🔄 Database
- PostgreSQL connection with pooling
- Waitlist table with: id, player_id, status, created_at
- Safe connection handling with try/finally blocks
