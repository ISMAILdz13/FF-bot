import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for ISMAIL-BOT"""
    
    BOT_NAME = os.getenv("BOT_NAME", "ISMAIL-BOT™")
    
    BOT_IDS = {
        "admin_uid": os.getenv("ADMIN_UID", "8804135237"),
        "bot_uid": os.getenv("BOT_UID", "14881602318"),
    }
    
    SERVER_CONFIG = {
        "server": os.getenv("BOT_SERVER", "BD"),
        "key": os.getenv("BOT_KEY", "mg24"),
    }
    
    SECURITY = {
        "bypass_token": os.getenv("BYPASS_TOKEN", "your_bypass_token_here"),
    }
    
    TIMING = {
        "start_spam_duration": int(os.getenv("START_SPAM_DURATION", 18)),
        "wait_after_match": int(os.getenv("WAIT_AFTER_MATCH", 20)),
        "start_spam_delay": float(os.getenv("START_SPAM_DELAY", 0.2)),
    }
    
    LOGGING = {
        "level": os.getenv("LOG_LEVEL", "INFO"),
    }


class FlaskConfig:
    """Configuration for Flask web application"""
    
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change_me_in_production")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/ismail_bot")
    
    WEB_CONFIG = {
        "host": os.getenv("FLASK_HOST", "0.0.0.0"),
        "port": int(os.getenv("FLASK_PORT", 5000)),
        "debug": os.getenv("FLASK_DEBUG", "False").lower() == "true",
    }
    
    SECURITY_CODES = {
        "main_access_code": os.getenv("MAIN_ACCESS_CODE", "default_main_code"),
        "dev_access_code": os.getenv("DEV_ACCESS_CODE", "default_dev_code"),
    }
    
    # Session Security Configuration
    SESSION_COOKIE_SECURE = os.getenv("FLASK_SESSION_SECURE", "False").lower() == "true"  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookies
    SESSION_COOKIE_SAMESITE = "Lax"  # CSRF protection
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour session timeout


if __name__ == "__main__":
    print("Bot Configuration:")
    print(f"  Bot Name: {Config.BOT_NAME}")
    print(f"  Admin UID: {Config.BOT_IDS['admin_uid']}")
    print(f"  Bot UID: {Config.BOT_IDS['bot_uid']}")
    print(f"\nFlask Configuration:")
    print(f"  Host: {FlaskConfig.WEB_CONFIG['host']}")
    print(f"  Port: {FlaskConfig.WEB_CONFIG['port']}")
