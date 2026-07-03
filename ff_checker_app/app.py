"""Flask Application Entry Point

Main application factory and route handlers for the Free Fire Guest Account Checker.
Handles file uploads, account lookups, and result rendering.

Author: Senior Python Full-Stack Engineer
Date: 2026
"""

import os
import logging
from typing import Dict, Any, Tuple
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from services.file_parser import FileParser
from services.ff_api import FFAPIClient
from services.exceptions import (
    FileValidationError,
    JSONParseError,
    GuestUIDExtractionError,
    APIError,
    RateLimitError,
    AccountBannedError
)
from utils.helpers import sanitize_input, format_account_data, log_request
from config import Config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FFCheckerApp:
    """Flask application wrapper with initialization and configuration."""

    def __init__(self):
        """Initialize the Flask application."""
        self.app = Flask(__name__)
        self.config = Config()
        self._configure_app()
        self._initialize_services()
        self._register_routes()
        self._register_error_handlers()

    def _configure_app(self) -> None:
        """Configure Flask application settings."""
        self.app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')
        self.app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
        self.app.config['UPLOAD_FOLDER'] = self.config.UPLOAD_FOLDER
        self.app.config['SESSION_COOKIE_SECURE'] = self.config.SESSION_COOKIE_SECURE
        self.app.config['SESSION_COOKIE_HTTPONLY'] = True
        self.app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        self.app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

        logger.info("✅ Flask application configured")

    def _initialize_services(self) -> None:
        """Initialize service layer dependencies."""
        self.file_parser = FileParser(self.config.UPLOAD_FOLDER)
        self.ff_api = FFAPIClient(
            api_base_url=self.config.FF_API_BASE_URL,
            timeout=self.config.API_TIMEOUT,
            max_retries=self.config.MAX_RETRIES
        )
        logger.info("✅ Services initialized")

    def _register_routes(self) -> None:
        """Register all application routes."""
        @self.app.route('/', methods=['GET'])
        def index():
            """Render the main upload interface.
            
            Returns:
                Rendered HTML template for the index page.
            """
            logger.info("GET / - User accessed index page")
            return render_template('index.html')

        @self.app.route('/api/upload', methods=['POST'])
        def upload_file() -> Tuple[Dict[str, Any], int]:
            """Handle file upload and guest UID extraction.
            
            Expected multipart form data:
                - file: .dat file containing guest account info
            
            Returns:
                JSON response with guest_uid or error message.
                Status codes:
                    - 200: Success
                    - 400: Validation error
                    - 413: File too large
                    - 422: Invalid file format
                    - 500: Server error
            """
            try:
                # Validate file presence
                if 'file' not in request.files:
                    logger.warning("Upload attempted without file")
                    return jsonify({'error': 'No file part in request'}), 400

                file = request.files['file']
                if file.filename == '':
                    logger.warning("Upload attempted with empty filename")
                    return jsonify({'error': 'No selected file'}), 400

                # Validate file type and size
                try:
                    self.file_parser.validate_file(file)
                except FileValidationError as e:
                    logger.warning(f"File validation error: {str(e)}")
                    return jsonify({'error': str(e)}), 422

                # Read and parse file
                file_content = file.read()
                if not file_content:
                    logger.warning("Empty file received")
                    return jsonify({'error': 'File is empty'}), 400

                try:
                    guest_uid = self.file_parser.extract_guest_uid(file_content)
                except (JSONParseError, GuestUIDExtractionError) as e:
                    logger.warning(f"Guest UID extraction error: {str(e)}")
                    return jsonify({'error': str(e)}), 422

                logger.info(f"✅ Successfully extracted guest UID: {guest_uid}")
                
                # Store in session for dashboard
                session['guest_uid'] = sanitize_input(guest_uid)
                session['extraction_timestamp'] = str(__import__('datetime').datetime.now(tz=__import__('datetime').timezone.utc))

                return jsonify({
                    'success': True,
                    'guest_uid': guest_uid,
                    'message': 'Guest UID extracted successfully'
                }), 200

            except Exception as e:
                logger.error(f"Unexpected error during file upload: {str(e)}", exc_info=True)
                return jsonify({'error': 'Internal server error'}), 500

        @self.app.route('/api/lookup', methods=['POST'])
        def lookup_account() -> Tuple[Dict[str, Any], int]:
            """Lookup Free Fire account information using guest UID.
            
            Expected JSON:
                {
                    "guest_uid": "5104522486"
                }
            
            Returns:
                JSON response with account data or error message.
                Status codes:
                    - 200: Success
                    - 400: Validation error
                    - 404: Account not found
                    - 429: Rate limited
                    - 500: Server error
            """
            try:
                data = request.get_json() or {}
                guest_uid = data.get('guest_uid', '').strip()

                # Validate guest UID
                if not guest_uid:
                    logger.warning("Lookup attempted without guest_uid")
                    return jsonify({'error': 'Guest UID is required'}), 400

                if not guest_uid.isdigit() or len(guest_uid) < 8:
                    logger.warning(f"Invalid guest UID format: {guest_uid}")
                    return jsonify({'error': 'Invalid guest UID format'}), 400

                # Sanitize input
                guest_uid = sanitize_input(guest_uid)

                logger.info(f"🔍 Looking up account for UID: {guest_uid}")

                # Query Free Fire API
                try:
                    account_data = self.ff_api.get_account_info(guest_uid)
                except RateLimitError as e:
                    logger.warning(f"Rate limit exceeded for UID {guest_uid}: {str(e)}")
                    return jsonify({
                        'error': 'API rate limit exceeded. Please try again in a few minutes.',
                        'retry_after': getattr(e, 'retry_after', 60)
                    }), 429
                except AccountBannedError as e:
                    logger.info(f"Account banned: {guest_uid} - {str(e)}")
                    return jsonify({
                        'success': False,
                        'error': str(e),
                        'account_data': {
                            'status': 'banned',
                            'uid': guest_uid,
                            'ban_info': getattr(e, 'ban_info', {})
                        }
                    }), 200
                except APIError as e:
                    logger.error(f"API error for UID {guest_uid}: {str(e)}")
                    return jsonify({'error': f'API Error: {str(e)}'}), 500

                # Format account data
                formatted_data = format_account_data(account_data)
                
                logger.info(f"✅ Account lookup successful for UID: {guest_uid}")

                return jsonify({
                    'success': True,
                    'account_data': formatted_data,
                    'message': 'Account information retrieved successfully'
                }), 200

            except Exception as e:
                logger.error(f"Unexpected error during account lookup: {str(e)}", exc_info=True)
                return jsonify({'error': 'Internal server error'}), 500

        @self.app.route('/dashboard', methods=['GET'])
        def dashboard():
            """Render the results dashboard.
            
            Returns:
                Rendered HTML dashboard with account information.
            """
            guest_uid = session.get('guest_uid')
            if not guest_uid:
                logger.warning("Dashboard accessed without guest_uid in session")
                return render_template('index.html', error='No guest UID in session. Please upload a file first.')
            
            logger.info(f"Rendering dashboard for UID: {guest_uid}")
            return render_template('dashboard.html', guest_uid=guest_uid)

        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint for monitoring.
            
            Returns:
                JSON response indicating application status.
            """
            return jsonify({
                'status': 'healthy',
                'service': 'FF-Checker',
                'version': '1.0.0',
                'timestamp': str(__import__('datetime').datetime.now(tz=__import__('datetime').timezone.utc))
            }), 200

    def _register_error_handlers(self) -> None:
        """Register global error handlers."""
        @self.app.errorhandler(404)
        def not_found(error):
            """Handle 404 errors."""
            logger.warning(f"404 error: {request.path}")
            return jsonify({'error': 'Resource not found'}), 404

        @self.app.errorhandler(413)
        def request_entity_too_large(error):
            """Handle 413 file too large errors."""
            logger.warning(f"413 error: File too large from {request.remote_addr}")
            return jsonify({'error': 'File too large. Maximum size is 10MB.'}), 413

        @self.app.errorhandler(500)
        def internal_error(error):
            """Handle 500 internal server errors."""
            logger.error(f"500 error: {str(error)}", exc_info=True)
            return jsonify({'error': 'Internal server error'}), 500

    def run(self, debug: bool = False, host: str = '0.0.0.0', port: int = 5000) -> None:
        """Run the Flask development server.
        
        Args:
            debug: Enable debug mode (never in production)
            host: Host to bind to
            port: Port to listen on
        """
        logger.info(f"🚀 Starting FF-Checker on {host}:{port}")
        self.app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    app_instance = FFCheckerApp()
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    app_instance.run(debug=debug_mode, host=host, port=port)
