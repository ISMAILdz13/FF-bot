"""Custom Exception Classes

Defines domain-specific exceptions for better error handling and diagnostics.

Author: Senior Python Full-Stack Engineer
Date: 2026
"""

from typing import Dict, Any, Optional


class FFCheckerException(Exception):
    """Base exception class for FF-Checker application."""

    def __init__(self, message: str, error_code: str = 'UNKNOWN_ERROR', details: Optional[Dict[str, Any]] = None):
        """
        Initialize exception.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Additional error details
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for JSON responses.
        
        Returns:
            Dictionary representation of the exception.
        """
        return {
            'error': self.message,
            'error_code': self.error_code,
            'details': self.details
        }


class FileValidationError(FFCheckerException):
    """Raised when file validation fails.
    
    Reasons:
    - Invalid file extension
    - File too large
    - File type mismatch
    - Corrupted file
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 'FILE_VALIDATION_ERROR', details)


class JSONParseError(FFCheckerException):
    """Raised when JSON parsing fails.
    
    Reasons:
    - Invalid JSON syntax
    - Malformed JSON structure
    - Encoding issues
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 'JSON_PARSE_ERROR', details)


class GuestUIDExtractionError(FFCheckerException):
    """Raised when guest UID extraction fails.
    
    Reasons:
    - Missing guest_account_info field
    - Missing com.garena.msdk.guest_uid field
    - Invalid UID format
    - Empty UID
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 'GUEST_UID_EXTRACTION_ERROR', details)


class APIError(FFCheckerException):
    """Base class for API-related errors.
    
    Reasons:
    - Server error (5xx)
    - Unexpected response format
    - Connection error
    """

    def __init__(self, message: str, status_code: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        super().__init__(message, 'API_ERROR', details)


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded.
    
    Attributes:
        retry_after: Number of seconds to wait before retrying
    """

    def __init__(self, message: str = 'API rate limit exceeded', retry_after: int = 60, details: Optional[Dict[str, Any]] = None):
        self.retry_after = retry_after
        super().__init__(message, 429, details)
        self.error_code = 'RATE_LIMIT_ERROR'


class AccountBannedError(APIError):
    """Raised when an account is banned.
    
    Attributes:
        ban_info: Dictionary containing ban details
    """

    def __init__(self, message: str = 'Account is banned', ban_info: Optional[Dict[str, Any]] = None, details: Optional[Dict[str, Any]] = None):
        self.ban_info = ban_info or {}
        super().__init__(message, 403, details)
        self.error_code = 'ACCOUNT_BANNED'


class AccountNotFoundError(APIError):
    """Raised when account is not found."""

    def __init__(self, message: str = 'Account not found', details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 404, details)
        self.error_code = 'ACCOUNT_NOT_FOUND'


class NetworkError(APIError):
    """Raised when network communication fails.
    
    Reasons:
    - Connection timeout
    - Connection refused
    - DNS resolution failure
    """

    def __init__(self, message: str = 'Network connection error', details: Optional[Dict[str, Any]] = None):
        super().__init__(message, None, details)
        self.error_code = 'NETWORK_ERROR'


class InvalidConfigError(FFCheckerException):
    """Raised when configuration is invalid."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 'INVALID_CONFIG_ERROR', details)
