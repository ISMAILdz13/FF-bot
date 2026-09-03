# Deployment Guide - FF-Checker

## 🚀 Deployment Options

FF-Checker can be deployed using multiple methods depending on your environment and requirements.

---

## Local Development

### Quick Start

```bash
# Clone/extract project
cd ff_checker_app

# Install dependencies
bash install.sh  # or manual steps

# Configure
cp .env.example .env
nano .env  # Edit with your settings

# Run
python app.py

# Access at http://localhost:5000
```

---

## Production Deployment

### Using Gunicorn

Gunicorn is a production-grade WSGI HTTP Server.

#### Installation

```bash
pip install gunicorn
```

#### Run with Gunicorn

```bash
# Basic command
gunicorn -w 4 -b 0.0.0.0:5000 app:app_instance.app

# With logging
gunicorn -w 4 -b 0.0.0.0:5000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info \
  app:app_instance.app

# With timeout protection
gunicorn -w 4 -b 0.0.0.0:5000 \
  -t 30 \
  --graceful-timeout 30 \
  app:app_instance.app
```

#### Systemd Service

Create `/etc/systemd/system/ff-checker.service`:

```ini
[Unit]
Description=Free Fire Guest Account Checker
After=network.target
Wants=network-online.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/ff-checker
Environment="PATH=/opt/ff-checker/venv/bin"
EnvironmentFile=/opt/ff-checker/.env
ExecStart=/opt/ff-checker/venv/bin/gunicorn \
  -w 4 \
  -b 0.0.0.0:5000 \
  -t 30 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  app:app_instance.app

ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure
RestartSec=10
KillMode=mixed
KillSignal=SIGQUIT

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ff-checker
sudo systemctl start ff-checker
sudo systemctl status ff-checker

# View logs
sudo journalctl -u ff-checker -f
```

---

### Using Docker

#### Build Image

```bash
# Build
docker build -t ff-checker:latest .

# Tag for registry
docker tag ff-checker:latest registry.example.com/ff-checker:latest
```

#### Run Container

```bash
# Basic run
docker run -p 5000:5000 --env-file .env ff-checker:latest

# With volumes
docker run \
  -p 5000:5000 \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/uploads:/app/uploads \
  -d \
  --name ff-checker \
  ff-checker:latest

# View logs
docker logs -f ff-checker

# Stop/remove
docker stop ff-checker
docker rm ff-checker
```

#### Docker Compose

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Remove volumes
docker compose down -v
```

---

### Using Nginx Reverse Proxy

Edit `/etc/nginx/sites-available/ff-checker`:

```nginx
upstream ff_checker {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "DENY";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'";
    
    # Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req /api zone=api burst=20 nodelay;
    
    # Proxy settings
    location / {
        proxy_pass http://ff_checker;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Enable configuration:

```bash
sudo ln -s /etc/nginx/sites-available/ff-checker /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

---

### Using Let's Encrypt SSL

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Auto-renew
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Check renewal
sudo certbot renew --dry-run
```

---

## Cloud Deployment

### Heroku

```bash
# Install Heroku CLI
# See: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_SECRET_KEY="your-secret-key"
heroku config:set FLASK_ENV=production
heroku config:set FLASK_DEBUG=False

# Deploy
git push heroku main

# View logs
heroku logs -t

# Open app
heroku open
```

Create `Procfile`:

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app_instance.app
```

### AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t3.small or larger
   - Security group: open 22 (SSH), 80 (HTTP), 443 (HTTPS)

2. **Connect and Setup**

```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.9 python3.9-venv python3-pip git nginx certbot python3-certbot-nginx

# Clone application
cd /opt
sudo git clone https://github.com/your-repo/ff-checker.git
sudo chown -R ubuntu:ubuntu ff-checker
cd ff-checker

# Setup
bash install.sh
cp .env.example .env
nano .env  # Edit with your settings

# Setup Nginx (see Nginx section above)
# Setup SSL (see Let's Encrypt section above)
# Setup systemd service (see Gunicorn Systemd section above)
```

### Google Cloud Run

1. **Prepare Application**
   - Add `Dockerfile`
   - Set port from environment: `PORT=${PORT:-5000}`

2. **Deploy**

```bash
# Build and push image
gcloud builds submit --tag gcr.io/your-project/ff-checker

# Deploy service
gcloud run deploy ff-checker \
  --image gcr.io/your-project/ff-checker \
  --platform managed \
  --region us-central1 \
  --set-env-vars FLASK_ENV=production,FLASK_SECRET_KEY=your-key
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# Manual check
curl http://localhost:5000/health

# Automated monitoring (e.g., Uptime Robot)
# Monitor endpoint: http://yourdomain.com/health
# Expected response: {"status": "healthy", ...}
```

### Log Monitoring

```bash
# Real-time logs
tail -f logs/ff_checker.log

# Filter errors
grep ERROR logs/ff_checker.log

# Count requests
wc -l logs/access.log
```

### Backup Strategy

```bash
# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/

# Backup configuration
cp .env .env.backup.$(date +%Y%m%d)
```

### Updates

```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Test changes
python -m pytest

# Restart service
sudo systemctl restart ff-checker
```

---

## Performance Optimization

### Gunicorn Workers

```bash
# Recommended: 2 * CPU_CORES + 1
# For 4 CPU cores: (2 * 4) + 1 = 9 workers
gunicorn -w 9 app:app_instance.app
```

### Database Connection Pooling

(If adding database support)

```python
from sqlalchemy.pool import QueuePool
db_pool = QueuePool(create_engine, max_overflow=10, pool_size=5)
```

### Caching

```bash
pip install Flask-Caching

# In app.py
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

---

## Troubleshooting Deployment

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Permission Denied

```bash
# Fix directory permissions
sudo chown -R www-data:www-data /opt/ff-checker
sudo chmod -R 755 /opt/ff-checker
```

### SSL Certificate Issues

```bash
# Check certificate expiration
sudo certbot certificates

# Renew manually
sudo certbot renew --force-renewal
```

### High Memory Usage

```bash
# Monitor memory
watch -n 1 'ps aux | grep gunicorn'

# Reduce worker count if needed
gunicorn -w 2 app:app_instance.app
```

---

## Scaling Considerations

For high-traffic deployments:

1. **Load Balancing**
   - Multiple Gunicorn instances
   - Nginx or HAProxy
   - Round-robin distribution

2. **Caching**
   - Redis for session storage
   - Cache API responses
   - CDN for static assets

3. **Database**
   - Add PostgreSQL if storing data
   - Connection pooling
   - Regular backups

4. **Monitoring**
   - Application Performance Monitoring (APM)
   - Error tracking (Sentry)
   - Metrics collection (Prometheus)

---

**Last Updated**: July 2026

**Next**: See README.md for complete documentation
