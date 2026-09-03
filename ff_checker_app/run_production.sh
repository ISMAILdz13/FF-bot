#!/bin/bash

# Free Fire Guest Account Checker - Production Run Script
# Uses Gunicorn for production deployment

set -e

echo "🚀 Starting FF-Checker with Gunicorn (Production)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "✗ Virtual environment not found. Run: bash install.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check dependencies
if ! python -c "import gunicorn" 2>/dev/null; then
    echo "✗ Gunicorn not found. Installing..."
    pip install gunicorn
fi

echo "✓ Environment ready"
echo "✓ Starting with Gunicorn (4 workers)"
echo ""

# Run with gunicorn
gunicorn \
    -w 4 \
    -b 0.0.0.0:5000 \
    -t 30 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    "app:app_instance.app"
