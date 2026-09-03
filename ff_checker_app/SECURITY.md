# Security Guide - FF-Checker

## 🔐 Security Overview

FF-Checker implements multiple layers of security to protect user data and prevent attacks.

---

## 📁 File Upload Security

### File Validation

✅ **Extension Validation**
- Only `.dat` files accepted
- Prevents execution of arbitrary files
- Case-insensitive checking

✅ **File Size Limits**
- Maximum 10 MB per file
- Prevents disk space exhaustion
- Configurable via `MAX_FILE_SIZE`

✅ **Content Validation**
- JSON schema validation
- Required field checking
- Type validation

### In-Memory Processing

✅ **No Permanent Storage**
- Files processed entirely in RAM
- No temporary files on disk
- Automatic garbage collection

✅ **Automatic Cleanup**
- Temporary files deleted after processing
- Upload folder cleared on restart
- No sensitive data persistence

---

## 🌐 Web Security

### Input Sanitization

✅ **XSS Prevention**
```python
# All user input is HTML-escaped
user_input = sanitize_input(request.form.get('field'))
# <script> becomes &lt;script&gt;
```

✅ **Injection Prevention**
- Parameterized queries for database operations
- No string concatenation in SQL/API calls
- Input length validation

### Session Security

✅ **Secure Cookies**
```python
SESSION_COOKIE_HTTPONLY = True  # JS can't access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_COOKIE_SECURE = True  # HTTPS only (production)
```

✅ **CSRF Protection**
- Flask session tokens
- SameSite cookie attribute
- Secure session handling

### Rate Limiting

✅ **API Rate Limiting**
```env
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=10  # 10 requests
RATE_LIMIT_WINDOW=60    # per 60 seconds
```

✅ **Prevents**
- Brute force attacks
- Denial of Service (DoS)
- API abuse
- Excessive server load

---

## 🔑 Secret Management

### Environment Variables

✅ **Never Hardcode Secrets**
```python
# ❌ BAD
SECRET_KEY = "my-secret-key"

# ✅ GOOD
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
```

✅ **Use .env File**
```bash
# .env (add to .gitignore)
FLASK_SECRET_KEY=your-secret-key-here
GARENA_AUTH_TOKEN=auth-token-here
```

✅ **.gitignore Configuration**
```gitignore
.env
.env.local
.env.*.local
accounts.json
*.log
```

### Secret Key Generation

```bash
# Generate strong random key
python -c "import secrets; print(secrets.token_hex(32))"

# For passwords
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🔗 API Security

### Request Validation

✅ **Content-Type Validation**
```python
if request.is_json:
    data = request.get_json()
```

✅ **Request Size Limits**
```python
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
```

### Response Security

✅ **Security Headers**
```python
response.headers['X-Content-Type-Options'] = 'nosniff'
response.headers['X-Frame-Options'] = 'DENY'
response.headers['X-XSS-Protection'] = '1; mode=block'
```

✅ **No Sensitive Data in Responses**
- Error messages don't leak internal details
- Stack traces only in development
- Sensitive fields removed from JSON

---

## 🔒 HTTPS/TLS

### Development

```env
# Development (.env)
SESSION_COOKIE_SECURE=False
FLASK_ENV=development
FLASK_DEBUG=True  # Only for local development
```

### Production

✅ **Enable HTTPS**
```env
SESSION_COOKIE_SECURE=True
FLASK_ENV=production
FLASK_DEBUG=False
```

✅ **Get SSL Certificate**
```bash
# Using Let's Encrypt (free)
sudo certbot certonly --standalone -d yourdomain.com

# Use with Gunicorn
gunicorn --certfile=/path/to/cert.pem \
         --keyfile=/path/to/key.pem \
         -b 0.0.0.0:443 \
         app:app
```

---

## 📝 Logging & Monitoring

### Security Logging

✅ **Log Suspicious Activity**
```python
logger.warning(f"Failed login from {request.remote_addr}")
logger.error(f"File validation failed: {error}")
logger.info(f"Account lookup: UID={guest_uid}")
```

✅ **Log Sensitive Operations**
- File uploads
- API requests
- Authentication attempts
- Error conditions

### Log Rotation

```bash
# Keep logs for 30 days
find logs/ -name "*.log" -mtime +30 -delete
```

---

## 🛡️ Production Checklist

### Before Deployment

- [ ] Generate strong `FLASK_SECRET_KEY`
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Install SSL/TLS certificate
- [ ] Update firewall rules
- [ ] Review all `.env` variables
- [ ] Test error handling
- [ ] Setup log monitoring
- [ ] Configure backup strategy

### Security Headers

Add to your reverse proxy (Nginx, Apache):

```nginx
# Nginx configuration
add_header X-Frame-Options "DENY";
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'";
```

### Rate Limiting (Reverse Proxy)

```nginx
# Nginx rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req /api zone=api burst=20 nodelay;
```

---

## 🚨 Incident Response

### If Account Breach is Suspected

1. **Immediate Actions**
   - Rotate `FLASK_SECRET_KEY`
   - Review access logs
   - Check for unauthorized uploads

2. **Investigation**
   - Check `logs/ff_checker.log`
   - Review failed login attempts
   - Examine file upload history

3. **Recovery**
   - Invalidate existing sessions
   - Force password resets if applicable
   - Deploy security patch

4. **Prevention**
   - Enable enhanced logging
   - Implement 2FA if applicable
   - Review file permissions

---

## 📚 Additional Resources

### Security Best Practices

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
- [Flask Security](https://flask.palletsprojects.com/security/)
- [Python Security](https://python.readthedocs.io/en/stable/library/security_warnings.html)

### Tools for Security Testing

```bash
# Security linting
pip install bandit
bandit -r services/ utils/

# Type checking
mypy services/ utils/

# Dependency vulnerabilities
pip install safety
safety check
```

---

## 🔐 Compliance

### Data Protection

✅ **GDPR Compliance**
- No personal data stored
- Files deleted after processing
- No tracking/analytics

✅ **PCI DSS (if handling payments)**
- No payment information storage
- No credential caching
- Secure transmission only

---

## 🔒 Report Security Issues

If you discover a security vulnerability:

1. **Do NOT** post publicly
2. **Contact** maintainers privately
3. **Include** details of the vulnerability
4. **Allow** time for a patch
5. **Coordinate** disclosure timeline

---

**Last Updated**: July 2026

**Remember**: Security is not a destination, it's an ongoing process. Stay informed and keep your dependencies updated.
