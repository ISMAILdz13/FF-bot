# Installation Guide - FF-Checker

## 📋 Prerequisites

Before installing FF-Checker, ensure you have:

- **Python 3.9 or higher** - [Download](https://www.python.org/downloads/)
- **pip** - Comes bundled with Python
- **Git** (optional) - For cloning the repository
- **4GB+ RAM** - For running the application
- **Internet connection** - For API communication

### System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows, macOS, or Linux |
| **Python** | 3.9+ |
| **RAM** | 512 MB minimum, 2GB recommended |
| **Disk** | 500 MB for installation |
| **Internet** | Required for API calls |

---

## 🚀 Installation Methods

### Method 1: Automated Installation (Recommended)

**On macOS/Linux:**

```bash
# Navigate to project directory
cd ff_checker_app

# Make installation script executable
chmod +x install.sh

# Run installation
bash install.sh
```

**On Windows (PowerShell):**

```powershell
# Navigate to project directory
cd ff_checker_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy configuration
Copy-Item .env.example .env
```

### Method 2: Manual Step-by-Step Installation

#### Step 1: Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Configure Application

```bash
# Copy example configuration
cp .env.example .env

# Edit with your preferred editor
nano .env  # or use: code .env (VS Code) / vim .env
```

#### Step 4: Verify Installation

```bash
# Test imports
python -c "import flask; import requests; print('✅ All dependencies installed')"

# Test application startup
python app.py
# Should show: "Running on http://0.0.0.0:5000"
# Press Ctrl+C to stop
```

### Method 3: Docker Installation

#### Prerequisites

- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop)
- Docker running in the background

#### Installation Steps

```bash
# Build Docker image
docker build -t ff-checker:latest .

# Run container
docker run -p 5000:5000 --env-file .env --name ff-checker ff-checker:latest

# Access at http://localhost:5000

# To stop container
docker stop ff-checker

# To remove container
docker rm ff-checker
```

#### Using Docker Compose

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

---

## ⚙️ Configuration

### Environment Variables

Edit the `.env` file with these settings:

```env
# ========== Flask Configuration ==========
FLASK_ENV=production              # or 'development'
FLASK_DEBUG=False                 # Never True in production
FLASK_SECRET_KEY=your_secret_key  # See below to generate
FLASK_HOST=0.0.0.0               # Listen on all interfaces
FLASK_PORT=5000                  # Port number

# ========== Free Fire API ==========
FF_API_BASE_URL=https://api-garenanow.garena.com
API_TIMEOUT=30                   # Seconds
MAX_RETRIES=3                    # Retry attempts

# ========== Security ==========
SESSION_COOKIE_SECURE=False      # Set to True if using HTTPS
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=10           # Per window
RATE_LIMIT_WINDOW=60             # Seconds

# ========== Garena Authentication (Optional) ==========
GARENA_USER_ID=
GARENA_AUTH_TOKEN=
GARENA_DEVICE_ID=
```

### Generate Strong Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it in `.env` as `FLASK_SECRET_KEY`

---

## ✅ Verification

### Test Installation

```bash
# Check Python version
python --version
# Should show: Python 3.9 or higher

# Test virtual environment
which python  # macOS/Linux
where python  # Windows
# Should show path inside venv/

# Test imports
python -c "from flask import Flask; from requests import Session; print('✅ OK')"
```

### Test Application

```bash
# Start the app
python app.py

# In another terminal, test endpoints
curl http://localhost:5000/health
# Should return: {"status": "healthy", ...}

curl http://localhost:5000/
# Should return HTML page
```

---

## 🐛 Troubleshooting

### Issue: "Python 3 not found"

**Solution:**
```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt-get install python3.11 python3.11-venv

# Windows
# Download from python.org and add to PATH
```

### Issue: "Permission denied" on install.sh

**Solution:**
```bash
chmod +x install.sh
bash install.sh
```

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
# Check virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Change port in .env
FLASK_PORT=8000

# Or kill the process using port 5000
lsof -i :5000  # Find process
kill -9 <PID>  # Kill it
```

### Issue: "SSL certificate verification failed"

**Solution (Development only):**
```env
# In .env (never in production)
CERTIFI_VERIFY=False
```

---

## 🚀 Running the Application

### Development Mode

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run with Flask development server
python app.py

# Access at http://localhost:5000
```

### Production Mode

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app_instance.app

# Or use production script
bash run_production.sh
```

### Using Shell Scripts

```bash
# Development
bash run.sh

# Production
bash run_production.sh
```

---

## 🔄 Updating Installation

### Update Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --upgrade
```

### Update Application Code

```bash
# If using Git
git pull origin ff-checker-app

# Reinstall dependencies (in case requirements.txt changed)
pip install -r requirements.txt
```

---

## 📦 Virtual Environment Management

### Deactivate Virtual Environment

```bash
deactivate
```

### Delete Virtual Environment

```bash
# macOS/Linux
rm -rf venv

# Windows
rmdir /s venv
```

### Create Fresh Virtual Environment

```bash
# Remove old environment
rm -rf venv

# Create new
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🆘 Getting Help

### Check Logs

```bash
# Application logs
cat logs/ff_checker.log

# Recent errors
tail -20 logs/ff_checker.log

# Real-time logs
tail -f logs/ff_checker.log
```

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| App won't start | Check .env file, verify Python version |
| Port in use | Change FLASK_PORT in .env |
| Import errors | Reinstall dependencies: `pip install -r requirements.txt` |
| Permission denied | Run `chmod +x install.sh` and try again |
| Virtual env not working | Deactivate/reactivate or create fresh |

---

## ✨ Next Steps

1. **Read the Documentation**
   - See `README.md` for full documentation
   - See `STRUCTURE.md` for project structure
   - See `SECURITY.md` for security considerations

2. **Configure the Application**
   - Edit `.env` with your settings
   - Generate a strong secret key
   - Set up Garena authentication (if available)

3. **Test the Application**
   - Visit http://localhost:5000
   - Try uploading a guest account file
   - View the dashboard

4. **Deploy to Production**
   - Set `FLASK_ENV=production`
   - Use Gunicorn or Docker
   - Enable HTTPS
   - Set strong secrets

---

## 📞 Support

For issues and questions:
- Check README.md and STRUCTURE.md
- Review logs in `logs/ff_checker.log`
- Create GitHub issue with details and logs

**Happy checking!** 🎮
