#!/bin/bash

# Free Fire Guest Account Checker - Installation Script
# This script sets up the development environment

set -e

echo "🚀 FF-Checker Installation Script"
echo "================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed. Please install Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 -V 2>&1 | awk '{print $2}')
echo "  Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created"
else
    echo "  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo "  Virtual environment activated"
echo ""

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "  pip upgraded"
echo ""

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "  Dependencies installed"
echo ""

# Create .env file
echo "✓ Setting up configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  .env file created from template"
    echo "  ⚠️  Please edit .env with your settings"
else
    echo "  .env file already exists"
fi
echo ""

# Create required directories
echo "✓ Creating directories..."
mkdir -p uploads logs
echo "  Directories created"
echo ""

# Run health check
echo "✓ Running health check..."
python3 -c "import flask; import requests; print('  Flask:', flask.__version__); print('  Requests:', requests.__version__)" || true
echo ""

echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Edit .env file with your settings"
echo "  2. Run: python app.py"
echo "  3. Open: http://localhost:5000"
echo ""
echo "For more information, see README.md"
