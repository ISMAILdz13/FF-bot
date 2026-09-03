"""Application Configuration Module

Centralized configuration management using environment variables and defaults.
Follows the 12-factor app methodology.

Author: Senior Python Full-Stack Engineer
Date: 2026
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Base configuration class with all application settings."""

    # ==================== Application Settings ====================
    DEBUG: bool = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING: bool = os.getenv('FLASK_TESTING', 'False').lower() == 'true'
    ENVIRONMENT: str = os.getenv('FLASK_ENV', 'production')

    # ==================== Security Settings ====================
    SECRET_KEY: str = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')
    SESSION_COOKIE_SECURE: bool = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = 'Lax'

    # ==================== File Upload Settings ====================
    UPLOAD_FOLDER: str = os.path.join(Path(__file__).parent, 'uploads')
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS: set = {'.dat'}
    ALLOWED_EXTENSIONS_STR: str = ', '.join(ALLOWED_EXTENSIONS)

    # Create upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # ==================== Free Fire API Settings ====================
    FF_API_BASE_URL: str = os.getenv(
        'FF_API_BASE_URL',
        'https://api-garenanow.garena.com'
    )
    API_TIMEOUT: int = int(os.getenv('API_TIMEOUT', '30'))  # seconds
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY: float = float(os.getenv('RETRY_DELAY', '1.0'))  # seconds

    # Rate limiting
    RATE_LIMIT_ENABLED: bool = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_REQUESTS: int = int(os.getenv('RATE_LIMIT_REQUESTS', '10'))  # requests
    RATE_LIMIT_WINDOW: int = int(os.getenv('RATE_LIMIT_WINDOW', '60'))  # seconds

    # ==================== Garena Authentication ====================
    # These credentials should be obtained from your FF-bot project
    GARENA_USER_ID: Optional[str] = os.getenv('GARENA_USER_ID')
    GARENA_AUTH_TOKEN: Optional[str] = os.getenv('GARENA_AUTH_TOKEN')
    GARENA_DEVICE_ID: Optional[str] = os.getenv('GARENA_DEVICE_ID')

    # ==================== Logging Settings ====================
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.path.join(Path(__file__).parent, 'logs', 'ff_checker.log')
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # ==================== Data Validation ====================
    MIN_GUEST_UID_LENGTH: int = 8
    MAX_GUEST_UID_LENGTH: int = 20
    VALID_REGIONS: set = {'BD', 'IND', 'US', 'GLOBAL'}
    DEFAULT_REGION: str = 'BD'

    # ==================== UI/UX Settings ====================
    ITEMS_PER_PAGE: int = 20
    PAGINATION_WINDOW: int = 5
    AUTO_REFRESH_INTERVAL: int = 5000  # milliseconds

    @classmethod
    def validate(cls) -> bool:
        """Validate critical configuration values.
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        
        Raises:
            ValueError: If critical configuration is missing or invalid.
        """
        errors = []

        # Check environment variables
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-key-change-in-production':
            if cls.ENVIRONMENT == 'production':
                errors.append(
                    "FLASK_SECRET_KEY must be set and strong in production"
                )

        # Check paths exist
        if not os.path.exists(cls.UPLOAD_FOLDER):
            try:
                os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
            except PermissionError:
                errors.append(f"Cannot create upload folder: {cls.UPLOAD_FOLDER}")

        if errors:
            raise ValueError("Configuration validation failed:\n" + "\n".join(errors))

        return True

    @classmethod
    def get_summary(cls) -> dict:
        """Get configuration summary for logging.
        
        Returns:
            dict: Configuration overview (with sensitive values masked).
        """
        return {
            'environment': cls.ENVIRONMENT,
            'debug': cls.DEBUG,
            'testing': cls.TESTING,
            'upload_folder': cls.UPLOAD_FOLDER,
            'max_file_size_mb': cls.MAX_FILE_SIZE / (1024 * 1024),
            'api_base_url': cls.FF_API_BASE_URL,
            'api_timeout': cls.API_TIMEOUT,
            'rate_limit_enabled': cls.RATE_LIMIT_ENABLED,
            'secret_key_set': bool(cls.SECRET_KEY and cls.SECRET_KEY != 'dev-key-change-in-production')
        }


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True
    SESSION_COOKIE_SECURE = False


def get_config(env: Optional[str] = None) -> Config:
    """Factory function to get appropriate config class.
    
    Args:
        env: Environment name ('development', 'production', 'testing')
             Defaults to FLASK_ENV environment variable
    
    Returns:
        Config: Configuration instance for the specified environment
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'production')

    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }

    return config_map.get(env.lower(), ProductionConfig)()
