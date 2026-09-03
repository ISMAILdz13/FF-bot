"""Dockerfile for Free Fire Guest Account Checker

Builds a containerized application with all dependencies.
Use for consistent deployment across environments.

Build: docker build -t ff-checker .
Run: docker run -p 5000:5000 --env-file .env ff-checker
"""

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads logs

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app_instance.app"]
