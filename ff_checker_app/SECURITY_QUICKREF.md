# Security Guide - FF-Checker

## 🔐 Security Overview

FF-Checker implements multiple layers of security:

✅ **File Upload Security**
- Extension validation (.dat only)
- File size limits (10 MB max)
- In-memory processing (no disk storage)
- Automatic cleanup

✅ **Web Security**
- XSS prevention (HTML escaping)
- CSRF protection (session tokens)
- Rate limiting (configurable)
- Secure cookies (HttpOnly, SameSite)

✅ **API Security**
- Request validation
- Response sanitization
- Error message safety
- No sensitive data leakage

✅ **Secret Management**
- Environment variables (never hardcoded)
- .env file (added to .gitignore)
- Strong key generation

---

## 🔧 Configuration

### Generate Strong Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy output to `.env` as `FLASK_SECRET_KEY`

### Production Checklist

- [ ] Generate strong `FLASK_SECRET_KEY`
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Install SSL/TLS certificate
- [ ] Review all `.env` variables
- [ ] Setup log monitoring

---

## 📊 Logging & Monitoring

```bash
# View logs
tail -f logs/ff_checker.log

# Filter errors
grep ERROR logs/ff_checker.log

# Health check
curl http://localhost:5000/health
```

---

See **SECURITY.md** for comprehensive security guide.
