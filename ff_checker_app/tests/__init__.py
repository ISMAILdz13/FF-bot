"""Test suite for FF-Checker application

Run with: pytest -v
"""

import json
import pytest
from pathlib import Path
from io import BytesIO


class TestFileParser:
    """Test cases for FileParser service."""

    def test_validate_file_valid_extension(self):
        """Test validation of valid .dat file."""
        from services.file_parser import FileParser
        
        parser = FileParser('uploads')
        # Create mock file object
        class MockFile:
            filename = 'guest.dat'
            def seek(self, pos, whence=0):
                pass
            def tell(self):
                return 1024  # 1 KB
        
        result = parser.validate_file(MockFile())
        assert result is True

    def test_validate_file_invalid_extension(self):
        """Test validation rejects invalid file extension."""
        from services.file_parser import FileParser
        from services.exceptions import FileValidationError
        
        parser = FileParser('uploads')
        class MockFile:
            filename = 'guest.txt'
            def seek(self, pos, whence=0):
                pass
            def tell(self):
                return 1024
        
        with pytest.raises(FileValidationError):
            parser.validate_file(MockFile())

    def test_extract_guest_uid_valid_json(self):
        """Test extraction of guest UID from valid JSON."""
        from services.file_parser import FileParser
        
        parser = FileParser('uploads')
        
        # Create valid JSON content
        data = {
            "guest_account_info": {
                "com.garena.msdk.guest_uid": "5104522486",
                "com.garena.msdk.guest_password": "abc123"
            }
        }
        content = json.dumps(data).encode('utf-8')
        
        uid = parser.extract_guest_uid(content)
        assert uid == "5104522486"

    def test_extract_guest_uid_missing_field(self):
        """Test extraction fails with missing guest UID field."""
        from services.file_parser import FileParser
        from services.exceptions import GuestUIDExtractionError
        
        parser = FileParser('uploads')
        
        # Missing guest_uid field
        data = {
            "guest_account_info": {
                "com.garena.msdk.guest_password": "abc123"
            }
        }
        content = json.dumps(data).encode('utf-8')
        
        with pytest.raises(GuestUIDExtractionError):
            parser.extract_guest_uid(content)

    def test_extract_guest_uid_invalid_json(self):
        """Test extraction fails with invalid JSON."""
        from services.file_parser import FileParser
        from services.exceptions import JSONParseError
        
        parser = FileParser('uploads')
        content = b'{invalid json}'
        
        with pytest.raises(JSONParseError):
            parser.extract_guest_uid(content)


class TestHelpers:
    """Test cases for helper functions."""

    def test_sanitize_input(self):
        """Test input sanitization."""
        from utils.helpers import sanitize_input
        
        # XSS attempt
        malicious = '<script>alert("xss")</script>'
        sanitized = sanitize_input(malicious)
        assert '<script>' not in sanitized
        assert '&lt;script&gt;' in sanitized

    def test_sanitize_input_truncation(self):
        """Test input truncation."""
        from utils.helpers import sanitize_input
        
        long_string = 'a' * 200
        sanitized = sanitize_input(long_string, max_length=100)
        assert len(sanitized) <= 100

    def test_format_account_data(self):
        """Test account data formatting."""
        from utils.helpers import format_account_data
        
        data = {
            'uid': '123456',
            'nickname': 'TestPlayer',
            'level': 50,
            'total_matches': 100,
            'total_wins': 25,
            'status': {'is_banned': False, 'is_active': True}
        }
        
        formatted = format_account_data(data)
        
        assert 'win_rate' in formatted
        assert formatted['win_rate'] == 25.0
        assert formatted['status_color'] == 'success'
        assert formatted['status_text'] == 'Active'


class TestExceptions:
    """Test cases for custom exceptions."""

    def test_file_validation_error(self):
        """Test FileValidationError exception."""
        from services.exceptions import FileValidationError
        
        error = FileValidationError('Test error')
        assert error.error_code == 'FILE_VALIDATION_ERROR'
        assert 'Test error' in str(error)

    def test_exception_to_dict(self):
        """Test exception serialization to dict."""
        from services.exceptions import APIError
        
        error = APIError('Test error', status_code=500)
        error_dict = error.to_dict()
        
        assert error_dict['error'] == 'Test error'
        assert error_dict['error_code'] == 'API_ERROR'
        assert 'details' in error_dict

    def test_rate_limit_error(self):
        """Test RateLimitError exception."""
        from services.exceptions import RateLimitError
        
        error = RateLimitError(retry_after=120)
        assert error.retry_after == 120
        assert error.status_code == 429


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
