# Deployment Guide - FF-Checker

## 🚀 Quick Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app_instance.app
```

### Using Docker

```bash
docker build -t ff-checker:latest .
docker run -p 5000:5000 --env-file .env ff-checker:latest
```

### Using Docker Compose

```bash
docker compose up -d
docker compose logs -f
docker compose down
```

---

## 🔗 Reverse Proxy (Nginx)

```nginx
upstream ff_checker {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://ff_checker;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📋 Systemd Service

Create `/etc/systemd/system/ff-checker.service`:

```ini
[Unit]
Description=Free Fire Guest Account Checker
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/ff-checker
ExecStart=/opt/ff-checker/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app_instance.app
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ff-checker
sudo systemctl start ff-checker
```

---

## 🔒 SSL Certificate (Let's Encrypt)

```bash
sudo certbot certonly --standalone -d yourdomain.com
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

See **DEPLOYMENT.md** for detailed deployment guide.
