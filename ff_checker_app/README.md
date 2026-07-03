# 🎮 Free Fire Guest Account Checker

## Production-Ready Web Application for Free Fire Account Lookup

**Version**: 1.0.0  
**Status**: ✅ Production-Ready  
**Language**: Python (Flask) + HTML5 + CSS3 + JavaScript  
**License**: MIT

---

## 📋 Overview

A sophisticated, modular web application that allows users to:

1. **Upload** a Free Fire guest account file (`.dat` format)
2. **Extract** the guest UID from the file
3. **Query** the Free Fire API for account information
4. **Display** comprehensive account data in a gaming-style dashboard

### Key Features

✅ **Secure File Handling** - In-memory processing, no permanent storage  
✅ **Comprehensive Error Handling** - Graceful error messages for all scenarios  
✅ **Rate Limiting** - Prevents API abuse  
✅ **Modern UI** - Dark gaming aesthetic with neon accents  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  
✅ **Production-Grade Code** - Type hints, docstrings, logging, PEP8  
✅ **Security First** - Input sanitization, CSRF protection, secure cookies  
✅ **Modular Architecture** - Clean separation of concerns  

---

## 📊 Project Structure

```
ff_checker_app/
├── app.py                    # Flask application & routes
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
│
├── services/                 # Business logic layer
│   ├── __init__.py
│   ├── file_parser.py       # File upload & UID extraction
│   ├── ff_api.py            # Free Fire API client
│   └── exceptions.py        # Custom exception classes
│
├── utils/                    # Helper functions
│   ├── __init__.py
│   └── helpers.py           # Sanitization, formatting, logging
│
├── templates/               # HTML templates
│   ├── base.html            # Base layout
│   ├── index.html           # Upload interface
│   └── dashboard.html       # Results dashboard
│
├── static/                  # Frontend assets
│   ├── css/
│   │   └── style.css        # Styling (dark gaming theme)
│   ├── js/
│   │   └── upload.js        # Frontend logic
│   └── images/              # Icons and images
│
└── uploads/                 # Temporary upload folder (gitignored)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **pip** - Comes with Python
- **Git** - For cloning (optional)

### Installation

#### 1. Clone/Download Repository

```bash
cd ff_checker_app
```

#### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env with your settings (optional for development)
nano .env
```

#### 5. Run Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

---

## 📖 Usage Guide

### User Workflow

1. **Access the Application**
   - Open `http://localhost:5000` in your browser
   - You'll see the upload interface

2. **Upload Guest Account File**
   - Drag & drop `.dat` file or use file browser
   - File is validated (extension, size)
   - Guest UID is extracted from JSON

3. **View Results**
   - Dashboard displays account information:
     - Basic profile data
     - Rank information
     - Clan details
     - Ban/suspension status

### File Format

Expected `.dat` file structure:

```json
{
    "guest_account_info": {
        "com.garena.msdk.guest_uid": "5104522486",
        "com.garena.msdk.guest_password": "0F7DB00E1EE70824..."
    }
}
```

---

## ⚙️ Configuration

### Environment Variables

Edit `.env` file:

```env
# Flask
FLASK_ENV=production        # or 'development'
FLASK_DEBUG=False           # Never True in production
FLASK_SECRET_KEY=...        # Strong random key

# Free Fire API
FF_API_BASE_URL=https://...
API_TIMEOUT=30              # Seconds
MAX_RETRIES=3

# File Upload
MAX_FILE_SIZE=10485760      # 10 MB

# Garena Auth (from FF-bot project)
GARENA_USER_ID=...
GARENA_AUTH_TOKEN=...
GARENA_DEVICE_ID=...
```

### Generate Strong Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output to `FLASK_SECRET_KEY` in `.env`

---

## 🔒 Security Features

### File Upload Security

✅ Extension validation (`.dat` only)  
✅ File size limits (10 MB max)  
✅ In-memory processing (no disk storage)  
✅ Automatic cleanup after processing  
✅ Safe JSON parsing with error handling  

### Web Security

✅ Input sanitization (XSS prevention)  
✅ CSRF protection via session tokens  
✅ HttpOnly cookies (XSS mitigation)  
✅ Secure session management  
✅ Environment variable secrets (no hardcoding)  
✅ Rate limiting (prevents API abuse)  

### API Security

✅ Rate limiting (configurable)  
✅ Retry logic with exponential backoff  
✅ Request timeout protection  
✅ Comprehensive error handling  
✅ Request logging for auditing  

---

## 🐛 Error Handling

The application handles:

**File Upload Errors**
- Invalid file extension
- File too large
- Empty file
- Corrupted file
- Encoding issues

**Parsing Errors**
- Invalid JSON
- Missing guest UID
- Invalid UID format

**API Errors**
- Account not found
- Account banned
- Rate limit exceeded
- Network timeout
- Server errors

All errors are logged and returned with descriptive messages.

---

## 📝 API Endpoints

### Public Endpoints

**GET /**
- Render upload interface

**POST /api/upload**
- Upload and parse `.dat` file
- Returns: `{ "success": true, "guest_uid": "5104522486" }`

**POST /api/lookup**
- Query account information
- Body: `{ "guest_uid": "5104522486" }`
- Returns: Account data or error

**GET /dashboard**
- Render results dashboard

**GET /health**
- Health check endpoint

---

## 🎨 UI/UX Design

### Dark Gaming Theme

- **Primary Colors**: Neon Blue (#00D9FF), Neon Purple (#7C3AED)
- **Background**: Dark (#0F172A)
- **Accents**: Cyan (#06B6D4), Purple (#8B5CF6)

### Responsive Layouts

- **Desktop**: Full layout with sidebars
- **Tablet**: Optimized touch interface
- **Mobile**: Single-column layout

### Components

- Drag-and-drop file upload
- Progress indicators
- Status badges
- Animated cards
- Loading spinners

---

## 🧪 Testing

### Run Tests

```bash
pytest -v
```

### Test Coverage

```bash
pytest --cov=services --cov=utils tests/
```

### Manual Testing

1. **Valid File Upload**
   ```bash
   curl -F "file=@guest.dat" http://localhost:5000/api/upload
   ```

2. **Account Lookup**
   ```bash
   curl -X POST http://localhost:5000/api/lookup \
     -H "Content-Type: application/json" \
     -d '{"guest_uid": "5104522486"}'
   ```

3. **Health Check**
   ```bash
   curl http://localhost:5000/health
   ```

---

## 📦 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

```bash
# Build
docker build -t ff-checker .

# Run
docker run -p 5000:5000 --env-file .env ff-checker
```

### Using systemd (Linux)

Create `/etc/systemd/system/ff-checker.service`:

```ini
[Unit]
Description=Free Fire Guest Account Checker
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ff-checker
ExecStart=/usr/bin/python3 app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable ff-checker
sudo systemctl start ff-checker
```

---

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Change port in .env
FLASK_PORT=8000
```

### SSL Certificate Error

```bash
# For development
SSL_VERIFY=False
```

### Upload Folder Permission Denied

```bash
chmod 755 uploads/
```

### API Connection Issues

1. Check internet connection
2. Verify `FF_API_BASE_URL` in `.env`
3. Check API rate limits
4. Review logs: `tail -f logs/ff_checker.log`

---

## 📚 Code Quality

### Standards

✅ **PEP 8** - Code style compliance  
✅ **Type Hints** - Full type annotations  
✅ **Docstrings** - Comprehensive documentation  
✅ **Logging** - Structured logging throughout  
✅ **Error Handling** - Defensive programming  
✅ **Testing** - pytest with coverage  

### Code Analysis

```bash
# Type checking
mypy services/ utils/

# Linting
flake8 .

# Code formatting
black .
isort .

# Security
bandit -r services/ utils/
```

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚠️ Legal Disclaimer

This application is designed for educational purposes. Usage must comply with:
- Free Fire Terms of Service
- Garena API usage policies
- Local gaming regulations

The authors are not responsible for account bans or penalties.

---

## 🆘 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Security**: Contact maintainers privately

---

**Last Updated**: July 2026  
**Maintained By**: Senior Python Full-Stack Engineer
