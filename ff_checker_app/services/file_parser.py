"""File Parser Service

Handles secure file uploads, validation, parsing, and guest UID extraction.
Implements best practices for file handling and data validation.

Author: Senior Python Full-Stack Engineer
Date: 2026
"""

import json
import logging
import os
import tempfile
from typing import Optional, Dict, Any
from pathlib import Path

from services.exceptions import (
    FileValidationError,
    JSONParseError,
    GuestUIDExtractionError
)

logger = logging.getLogger(__name__)


class FileParser:
    """Handles file upload validation and guest UID extraction.
    
    Security Features:
    - File extension validation
    - File size limits
    - Safe JSON parsing
    - In-memory processing (no disk storage)
    - Comprehensive error handling
    """

    # Constants
    ALLOWED_EXTENSIONS = {'.dat'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    CHUNK_SIZE = 8192  # Read in chunks for large files

    # Expected JSON structure paths
    GUEST_UID_PATH = 'guest_account_info.com.garena.msdk.guest_uid'
    GUEST_PASSWORD_PATH = 'guest_account_info.com.garena.msdk.guest_password'

    def __init__(self, upload_folder: str):
        """
        Initialize FileParser.
        
        Args:
            upload_folder: Path to temporary upload folder
        """
        self.upload_folder = Path(upload_folder)
        self.upload_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"FileParser initialized with upload folder: {upload_folder}")

    def validate_file(self, file_obj) -> bool:
        """
        Validate uploaded file.
        
        Checks:
        - File extension
        - File size
        - File object integrity
        
        Args:
            file_obj: Werkzeug FileStorage object
        
        Returns:
            True if file is valid
        
        Raises:
            FileValidationError: If validation fails
        """
        # Check filename
        if not file_obj.filename:
            raise FileValidationError(
                'Filename is required',
                details={'field': 'filename'}
            )

        # Get file extension
        filename = file_obj.filename.lower()
        file_ext = Path(filename).suffix.lower()

        # Validate extension
        if file_ext not in self.ALLOWED_EXTENSIONS:
            raise FileValidationError(
                f'Invalid file extension. Allowed: {", ".join(self.ALLOWED_EXTENSIONS)}',
                details={
                    'extension': file_ext,
                    'allowed': list(self.ALLOWED_EXTENSIONS),
                    'filename': filename
                }
            )

        # Check file size
        # Seek to end to get file size
        file_obj.seek(0, 2)  # Seek to end
        file_size = file_obj.tell()
        file_obj.seek(0)  # Reset to start

        if file_size == 0:
            raise FileValidationError(
                'File is empty',
                details={'file_size': 0}
            )

        if file_size > self.MAX_FILE_SIZE:
            raise FileValidationError(
                f'File size ({file_size} bytes) exceeds maximum allowed ({self.MAX_FILE_SIZE} bytes)',
                details={
                    'file_size': file_size,
                    'max_size': self.MAX_FILE_SIZE
                }
            )

        logger.info(f"✅ File validation passed: {filename} ({file_size} bytes)")
        return True

    def extract_guest_uid(self, file_content: bytes) -> str:
        """
        Extract guest UID from file content.
        
        Expected JSON structure:
        {
            "guest_account_info": {
                "com.garena.msdk.guest_uid": "5104522486",
                "com.garena.msdk.guest_password": "0F7DB00E1EE70824832CEA6112D7C9C82006A68BE59448076CBF957594FEAF26"
            }
        }
        
        Args:
            file_content: Raw file bytes
        
        Returns:
            Guest UID as string
        
        Raises:
            JSONParseError: If JSON is invalid
            GuestUIDExtractionError: If UID extraction fails
        """
        try:
            # Try to decode content
            try:
                content_str = file_content.decode('utf-8')
            except UnicodeDecodeError:
                # Try other encodings
                try:
                    content_str = file_content.decode('latin-1')
                except UnicodeDecodeError:
                    raise JSONParseError(
                        'File encoding is not UTF-8 or Latin-1',
                        details={'encodings_tried': ['utf-8', 'latin-1']}
                    )

            # Parse JSON
            try:
                data = json.loads(content_str)
            except json.JSONDecodeError as e:
                raise JSONParseError(
                    f'Invalid JSON format: {str(e)}',
                    details={
                        'error': str(e),
                        'line': e.lineno,
                        'column': e.colno
                    }
                )

            # Extract guest UID using nested dictionary access
            try:
                guest_info = data.get('guest_account_info', {})
                if not isinstance(guest_info, dict):
                    raise GuestUIDExtractionError(
                        'guest_account_info is not a dictionary',
                        details={'type': type(guest_info).__name__}
                    )

                guest_uid = guest_info.get('com.garena.msdk.guest_uid')
                
                if not guest_uid:
                    raise GuestUIDExtractionError(
                        'Guest UID field not found in file',
                        details={'available_fields': list(guest_info.keys())}
                    )

                # Validate UID format
                guest_uid_str = str(guest_uid).strip()
                
                if not guest_uid_str:
                    raise GuestUIDExtractionError(
                        'Guest UID is empty',
                        details={'raw_value': guest_uid}
                    )

                if not guest_uid_str.isdigit():
                    raise GuestUIDExtractionError(
                        'Guest UID must contain only digits',
                        details={'value': guest_uid_str}
                    )

                if len(guest_uid_str) < 8:
                    raise GuestUIDExtractionError(
                        'Guest UID is too short',
                        details={'length': len(guest_uid_str), 'minimum': 8}
                    )

                logger.info(f"✅ Successfully extracted guest UID: {guest_uid_str}")
                return guest_uid_str

            except GuestUIDExtractionError:
                raise
            except Exception as e:
                raise GuestUIDExtractionError(
                    f'Error extracting guest UID: {str(e)}',
                    details={'error_type': type(e).__name__}
                )

        except (JSONParseError, GuestUIDExtractionError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error in extract_guest_uid: {str(e)}", exc_info=True)
            raise JSONParseError(
                f'Unexpected error: {str(e)}',
                details={'error_type': type(e).__name__}
            )

    def parse_file(self, file_content: bytes) -> Dict[str, Any]:
        """
        Parse file content and extract all data.
        
        Args:
            file_content: Raw file bytes
        
        Returns:
            Dictionary with parsed data
        
        Raises:
            JSONParseError: If JSON is invalid
            GuestUIDExtractionError: If UID extraction fails
        """
        try:
            content_str = file_content.decode('utf-8')
            data = json.loads(content_str)
            
            guest_info = data.get('guest_account_info', {})
            guest_uid = guest_info.get('com.garena.msdk.guest_uid')
            guest_password = guest_info.get('com.garena.msdk.guest_password')

            return {
                'guest_uid': str(guest_uid) if guest_uid else None,
                'guest_password': guest_password,
                'full_data': data
            }

        except (JSONParseError, GuestUIDExtractionError):
            raise
        except Exception as e:
            raise JSONParseError(f'Error parsing file: {str(e)}')

    def cleanup_file(self, file_path: str) -> bool:
        """
        Safely delete uploaded file.
        
        Args:
            file_path: Path to file to delete
        
        Returns:
            True if file was deleted, False if not found
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"✅ Cleaned up temporary file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {str(e)}")
            return False
