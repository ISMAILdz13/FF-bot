"""Free Fire API Client Service

Integrates with Free Fire API to retrieve account information.
Implements retry logic, rate limiting, and error handling.

This module reuses authentication and request patterns from the FF-bot project.
Key differences:
- Focused on read-only account lookups (not gameplay automation)
- Rate-limited requests
- Comprehensive error handling
- Defensive API response parsing

Author: Senior Python Full-Stack Engineer
Date: 2026
"""

import logging
import time
from typing import Optional, Dict, Any
from datetime import datetime, timezone

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from services.exceptions import (
    APIError,
    RateLimitError,
    AccountNotFoundError,
    AccountBannedError,
    NetworkError
)

logger = logging.getLogger(__name__)


class FFAPIClient:
    """Free Fire API Client with retry logic and error handling.
    
    Features:
    - Connection pooling
    - Automatic retries
    - Rate limiting
    - Comprehensive error handling
    - Request/response logging
    
    Note: This client is designed for querying account info from Free Fire.
    Authentication credentials should be obtained from environment variables.
    """

    def __init__(
        self,
        api_base_url: str = 'https://api-garenanow.garena.com',
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize Free Fire API Client.
        
        Args:
            api_base_url: Base URL for Free Fire API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = self._create_session()
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.5  # Minimum 500ms between requests
        
        logger.info(f"✅ FFAPIClient initialized: {self.api_base_url}")

    def _create_session(self) -> requests.Session:
        """
        Create requests session with retry strategy.
        
        Returns:
            Configured requests Session object
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=['GET', 'POST'],
            backoff_factor=1  # Exponential backoff: 1s, 2s, 4s, etc.
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Set default headers
        session.headers.update({
            'User-Agent': 'FF-Checker/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        return session

    def _enforce_rate_limit(self) -> None:
        """
        Enforce minimum time between API requests.
        
        This prevents overwhelming the Free Fire API and getting rate limited.
        """
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            sleep_time = self.min_request_interval - elapsed
            logger.debug(f"Rate limit: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

    def get_account_info(self, guest_uid: str) -> Dict[str, Any]:
        """
        Retrieve Free Fire account information using guest UID.
        
        This method demonstrates how to query account info from Free Fire.
        In production, you would use your actual FF-bot authentication tokens.
        
        Args:
            guest_uid: Guest account UID (e.g., '5104522486')
        
        Returns:
            Dictionary containing account information
        
        Raises:
            AccountNotFoundError: Account doesn't exist
            AccountBannedError: Account is banned
            RateLimitError: API rate limit exceeded
            APIError: Other API errors
            NetworkError: Network connection error
        """
        if not guest_uid or not guest_uid.isdigit():
            raise APIError('Invalid guest UID format')

        logger.info(f"🔍 Fetching account info for UID: {guest_uid}")
        
        # Enforce rate limiting
        self._enforce_rate_limit()

        try:
            # This is a mock implementation. In production, replace with actual API call.
            # Example real implementation would use authentication from FF-bot:
            # POST /account/profile with auth tokens
            
            account_data = self._fetch_account_from_api(guest_uid)
            
            logger.info(f"✅ Successfully retrieved account info for UID: {guest_uid}")
            return account_data

        except RateLimitError:
            raise
        except AccountNotFoundError:
            raise
        except AccountBannedError:
            raise
        except NetworkError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching account: {str(e)}", exc_info=True)
            raise APIError(f'Failed to fetch account info: {str(e)}')

    def _fetch_account_from_api(self, guest_uid: str) -> Dict[str, Any]:
        """
        Internal method to fetch account from Free Fire API.
        
        This is a MOCK implementation. In production:
        1. Use authentication tokens from environment variables
        2. Call actual Free Fire API endpoint
        3. Parse response according to Garena's protocol
        4. Handle account ban/suspension status
        
        Args:
            guest_uid: Guest account UID
        
        Returns:
            Account information dictionary
        
        Raises:
            Various API exceptions
        """
        try:
            # Mock API endpoint (replace with actual Garena endpoint)
            endpoint = f"{self.api_base_url}/account/profile/{guest_uid}"
            
            # In production, add authentication headers from FF-bot
            headers = {
                'Authorization': 'Bearer YOUR_AUTH_TOKEN',  # From environment
                'X-Device-ID': 'YOUR_DEVICE_ID',            # From environment
            }
            
            logger.debug(f"Calling API endpoint: {endpoint}")
            
            response = self.session.get(
                endpoint,
                headers=headers,
                timeout=self.timeout,
                verify=True
            )
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                raise RateLimitError(
                    'API rate limit exceeded',
                    retry_after=retry_after,
                    details={'retry_after': retry_after}
                )
            
            # Handle not found
            if response.status_code == 404:
                raise AccountNotFoundError(
                    f'Account not found: {guest_uid}',
                    details={'uid': guest_uid}
                )
            
            # Handle other errors
            if response.status_code >= 400:
                raise APIError(
                    f'API error: {response.status_code}',
                    status_code=response.status_code,
                    details={'response': response.text[:200]}
                )
            
            # Parse successful response
            data = response.json()
            
            # Check for ban status in response
            if self._check_ban_status(data):
                ban_info = self._extract_ban_info(data)
                raise AccountBannedError(
                    'Account is banned',
                    ban_info=ban_info,
                    details={'uid': guest_uid}
                )
            
            return self._normalize_account_data(data)
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise NetworkError(f'Failed to connect to API: {str(e)}')
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout: {str(e)}")
            raise NetworkError(f'API request timed out: {str(e)}')
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            raise NetworkError(f'Request error: {str(e)}')

    def _check_ban_status(self, data: Dict[str, Any]) -> bool:
        """
        Check if account is banned based on API response.
        
        Args:
            data: API response data
        
        Returns:
            True if account is banned
        """
        # Check various ban status indicators from Free Fire API
        ban_status = data.get('ban_status')
        is_banned = data.get('is_banned', False)
        
        return ban_status == 'banned' or is_banned

    def _extract_ban_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract ban information from API response.
        
        Args:
            data: API response data
        
        Returns:
            Dictionary with ban details
        """
        return {
            'status': data.get('ban_status', 'unknown'),
            'reason': data.get('ban_reason', 'Not specified'),
            'duration': data.get('ban_duration'),
            'ban_time': data.get('ban_time'),
            'unban_time': data.get('unban_time')
        }

    def _normalize_account_data(self, api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize and standardize API response data.
        
        Transforms Free Fire API response into our internal format.
        
        Args:
            api_response: Raw API response
        
        Returns:
            Standardized account data dictionary
        """
        return {
            # Basic Information
            'uid': str(api_response.get('uid', '')),
            'nickname': api_response.get('nickname', 'Unknown'),
            'level': api_response.get('level', 0),
            'experience': api_response.get('experience', 0),
            'region': api_response.get('region', 'GLOBAL'),
            'created_at': api_response.get('created_at'),
            
            # Ranked Information
            'ranked': {
                'br_rank': api_response.get('br_rank', 0),
                'cs_rank': api_response.get('cs_rank', 0),
                'rank_points': api_response.get('rank_points', 0),
                'current_season': api_response.get('current_season', 'Unknown')
            },
            
            # Clan Information
            'clan': {
                'name': api_response.get('clan_name', 'No Clan'),
                'id': api_response.get('clan_id'),
                'role': api_response.get('clan_role'),
                'level': api_response.get('clan_level', 0)
            },
            
            # Account Status
            'status': {
                'is_active': api_response.get('is_active', True),
                'is_banned': api_response.get('is_banned', False),
                'is_suspended': api_response.get('is_suspended', False),
                'ban_reason': api_response.get('ban_reason'),
                'ban_duration': api_response.get('ban_duration')
            },
            
            # Additional Data
            'last_login': api_response.get('last_login'),
            'total_matches': api_response.get('total_matches', 0),
            'total_wins': api_response.get('total_wins', 0),
            'headshots': api_response.get('headshots', 0),
            'kill_death_ratio': api_response.get('kd_ratio', 0)
        }

    def close(self) -> None:
        """
        Close the HTTP session and cleanup resources.
        """
        if self.session:
            self.session.close()
            logger.info("✅ APIClient session closed")
