# FF-Checker Application Structure

## Quick Reference

### Entry Point
- **app.py** - Flask application initialization and routes

### Configuration
- **config.py** - Environment-based configuration
- **.env** - Environment variables (create from .env.example)

### Services (Business Logic)
- **services/file_parser.py** - File upload validation and UID extraction
- **services/ff_api.py** - Free Fire API client with retry logic
- **services/exceptions.py** - Custom exception classes

### Utilities
- **utils/helpers.py** - Helper functions for sanitization, formatting, logging

### Templates (HTML)
- **templates/base.html** - Base layout with navigation and footer
- **templates/index.html** - Upload interface with drag-and-drop
- **templates/dashboard.html** - Results dashboard with account info

### Static Assets
- **static/css/style.css** - Dark gaming theme with neon accents
- **static/js/upload.js** - Frontend upload logic
- **static/images/** - Icons and images

### Supporting Files
- **requirements.txt** - Python dependencies
- **README.md** - Complete documentation
- **.gitignore** - Git ignore rules

---

## File Responsibilities

### Core Application (app.py)
```python
# Contains:
- FFCheckerApp class (Flask wrapper)
- Route handlers:
  - GET / - Index/upload page
  - POST /api/upload - File upload & UID extraction
  - POST /api/lookup - Account information lookup
  - GET /dashboard - Results dashboard
  - GET /health - Health check
- Error handlers (404, 413, 500)
```

### Configuration (config.py)
```python
# Contains:
- Config base class with all settings
- DevelopmentConfig for local development
- ProductionConfig for production
- TestingConfig for unit tests
- get_config() factory function
```

### File Parser (services/file_parser.py)
```python
# Responsibilities:
- validate_file() - Check extension, size, integrity
- extract_guest_uid() - Parse JSON and extract UID
- parse_file() - Full file parsing
- cleanup_file() - Delete temporary files

# Security features:
- File extension validation
- File size limits
- Safe JSON parsing
- In-memory processing
- Comprehensive error handling
```

### Free Fire API (services/ff_api.py)
```python
# Responsibilities:
- get_account_info() - Query account data
- _fetch_account_from_api() - Make API requests
- _check_ban_status() - Detect banned accounts
- _normalize_account_data() - Standardize response format

# Features:
- Connection pooling
- Automatic retries
- Rate limiting
- Error recovery

# Integration with FF-bot:
- Uses same API endpoints
- Compatible authentication patterns
- Same data structures
```

### Exception Classes (services/exceptions.py)
```python
# Custom exceptions:
- FFCheckerException - Base class
- FileValidationError - File upload issues
- JSONParseError - JSON parsing failures
- GuestUIDExtractionError - UID extraction issues
- APIError - API communication errors
- RateLimitError - Rate limit exceeded
- AccountBannedError - Account is banned
- AccountNotFoundError - Account not found
- NetworkError - Network issues
```

### Helper Functions (utils/helpers.py)
```python
# Functions:
- sanitize_input() - XSS prevention
- format_account_data() - Data formatting
- format_datetime() - Date/time display
- log_request() - HTTP request logging
- get_rank_color() - Color coding for ranks
- get_level_color() - Color coding for levels
- truncate_text() - Text truncation with ellipsis
```

---

## Data Flow

### Upload & Extraction Flow
```
User browses file
    ↓
File sent to POST /api/upload
    ↓
FileParser.validate_file()
    ↓
FileParser.extract_guest_uid()
    ↓
Return guest_uid to frontend
    ↓
Store in session
    ↓
User navigates to /dashboard
```

### Account Lookup Flow
```
User on dashboard
    ↓
Fetch /api/lookup with guest_uid
    ↓
FFAPIClient.get_account_info()
    ↓
Make API request with retries
    ↓
Parse and normalize response
    ↓
Return account data
    ↓
Display in dashboard
```

---

## Directory Permissions

- **uploads/** - Temporary file storage (writable, auto-cleanup)
- **logs/** - Application logs (writable)
- **static/** - Read-only assets (served by Flask)
- **templates/** - Read-only templates (served by Flask)

---

## Environment Variables

Required (if empty, defaults are used):
- `FLASK_SECRET_KEY` - Session encryption key
- `FF_API_BASE_URL` - Free Fire API endpoint

Optional:
- `FLASK_ENV` - Development/production
- `FLASK_DEBUG` - Debug mode
- `API_TIMEOUT` - Request timeout
- `MAX_RETRIES` - Retry attempts
- `GARENA_*` - Authentication tokens

See `.env.example` for complete list.

---

## Adding New Features

1. **New Endpoint**
   - Add route to app.py
   - Create template in templates/
   - Add static assets if needed

2. **New Service**
   - Create file in services/
   - Add exception class if needed
   - Add to services/__init__.py

3. **New API Integration**
   - Extend ff_api.py
   - Add error handling
   - Document in code comments

---

## Testing

```bash
# Unit tests
pytest -v

# Coverage
pytest --cov=services --cov=utils

# Manual API testing
curl -X POST http://localhost:5000/api/upload -F "file=@guest.dat"
curl -X POST http://localhost:5000/api/lookup -H "Content-Type: application/json" -d '{"guest_uid": "5104522486"}'
```

---

## Deployment

```bash
# Development
python app.py

# Production
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Docker
docker build -t ff-checker .
docker run -p 5000:5000 --env-file .env ff-checker
```
