#!/bin/bash

# Free Fire Guest Account Checker - Run Script
# Starts the Flask development server

set -e

echo "🚀 Starting FF-Checker Application..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "✗ Virtual environment not found. Run: bash install.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "Please edit .env with your settings before running!"
    exit 1
fi

echo "✓ Environment ready"
echo "✓ Starting Flask application on http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run Flask app
python app.py
