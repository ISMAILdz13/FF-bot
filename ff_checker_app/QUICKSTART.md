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
cd ff_checker_app
chmod +x install.sh
bash install.sh
```

**On Windows (PowerShell):**

```powershell
cd ff_checker_app
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### Method 2: Manual Step-by-Step Installation

#### Step 1: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\\Scripts\\activate  # Windows
```

#### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Configure Application

```bash
cp .env.example .env
nano .env  # Edit configuration
```

#### Step 4: Verify Installation

```bash
python -c "import flask; import requests; print('✅ All dependencies installed')"
python app.py
# Press Ctrl+C to stop
```

### Method 3: Docker Installation

```bash
docker build -t ff-checker:latest .
docker run -p 5000:5000 --env-file .env ff-checker:latest
# Access at http://localhost:5000
```

Or with Docker Compose:

```bash
docker compose up -d
```

---

## ✅ Verification

```bash
python --version  # Should show 3.9+
which python      # Should show venv path
curl http://localhost:5000/health  # Should return healthy status
```

---

## 🎮 Running the Application

**Development:**
```bash
source venv/bin/activate
python app.py
```

**Production:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app_instance.app
```

Access at: **http://localhost:5000**

---

See **INSTALLATION.md** for detailed setup guide.
