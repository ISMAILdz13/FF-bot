"""Helper Functions

Utility functions for input sanitization, data formatting, and logging.

Author: Senior Python Full-Stack Engineer
Date: 2026
"""

import re
import logging
from typing import Any, Dict, Optional
from datetime import datetime
import html

logger = logging.getLogger(__name__)


def sanitize_input(user_input: str, max_length: int = 100) -> str:
    """
    Sanitize user input to prevent XSS and injection attacks.
    
    Args:
        user_input: Raw user input
        max_length: Maximum allowed length
    
    Returns:
        Sanitized string
    """
    if not isinstance(user_input, str):
        user_input = str(user_input)
    
    # Remove leading/trailing whitespace
    user_input = user_input.strip()
    
    # Truncate if too long
    if len(user_input) > max_length:
        user_input = user_input[:max_length]
    
    # HTML escape dangerous characters
    user_input = html.escape(user_input)
    
    # Remove control characters
    user_input = ''.join(char for char in user_input if ord(char) >= 32 or char in '\n\r\t')
    
    return user_input


def format_account_data(account_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format account data for display in dashboard.
    
    Adds calculated fields, formats dates, and prepares data for frontend.
    
    Args:
        account_data: Raw account data from API
    
    Returns:
        Formatted account data
    """
    if not isinstance(account_data, dict):
        return account_data
    
    formatted = account_data.copy()
    
    # Format dates
    for date_field in ['created_at', 'last_login', 'ban_time', 'unban_time']:
        if date_field in formatted and formatted[date_field]:
            try:
                formatted[f"{date_field}_display"] = format_datetime(formatted[date_field])
            except Exception:
                pass
    
    # Calculate additional metrics
    if 'total_matches' in formatted and 'total_wins' in formatted:
        total = formatted.get('total_matches', 1)
        wins = formatted.get('total_wins', 0)
        formatted['win_rate'] = round((wins / max(total, 1)) * 100, 2)
    
    # Format K/D ratio
    if 'kill_death_ratio' in formatted:
        formatted['kd_ratio_display'] = f"{formatted['kill_death_ratio']:.2f}"
    
    # Determine status color
    if formatted.get('status', {}).get('is_banned'):
        formatted['status_color'] = 'danger'  # Red
        formatted['status_text'] = 'Banned'
    elif formatted.get('status', {}).get('is_suspended'):
        formatted['status_color'] = 'warning'  # Yellow
        formatted['status_text'] = 'Suspended'
    elif formatted.get('status', {}).get('is_active'):
        formatted['status_color'] = 'success'  # Green
        formatted['status_text'] = 'Active'
    else:
        formatted['status_color'] = 'secondary'  # Gray
        formatted['status_text'] = 'Unknown'
    
    return formatted


def format_datetime(dt_value: Any) -> str:
    """
    Format datetime value for display.
    
    Args:
        dt_value: DateTime value (string or datetime object)
    
    Returns:
        Formatted datetime string
    """
    if isinstance(dt_value, datetime):
        return dt_value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(dt_value, str):
        try:
            # Try parsing ISO format
            dt_obj = datetime.fromisoformat(dt_value.replace('Z', '+00:00'))
            return dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            return dt_value
    return str(dt_value)


def log_request(method: str, path: str, status_code: int, duration: float) -> None:
    """
    Log HTTP request details.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        path: Request path
        status_code: Response status code
        duration: Request duration in milliseconds
    """
    status_emoji = '✅' if 200 <= status_code < 300 else '⚠️' if 400 <= status_code < 500 else '❌'
    logger.info(
        f"{status_emoji} {method} {path} - {status_code} ({duration:.2f}ms)"
    )


def get_rank_color(rank: int) -> str:
    """
    Get color for rank tier display.
    
    Args:
        rank: Rank number
    
    Returns:
        Color class name for Bootstrap
    """
    if rank <= 0:
        return 'secondary'
    elif rank <= 5:
        return 'info'
    elif rank <= 10:
        return 'success'
    elif rank <= 15:
        return 'primary'
    elif rank <= 18:
        return 'warning'
    else:
        return 'danger'


def get_level_color(level: int) -> str:
    """
    Get color for level display.
    
    Args:
        level: Account level
    
    Returns:
        Color class name for Bootstrap
    """
    if level < 10:
        return 'secondary'
    elif level < 30:
        return 'info'
    elif level < 50:
        return 'primary'
    elif level < 70:
        return 'success'
    else:
        return 'warning'


def truncate_text(text: str, max_length: int = 50, suffix: str = '...') -> str:
    """
    Truncate text with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        suffix: Suffix to add (default: '...')
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
