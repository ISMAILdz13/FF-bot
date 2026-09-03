"""Unit Tests for FF-Checker Application

Run with: pytest tests/
Run with coverage: pytest --cov=services --cov=utils tests/
"""

import os
import sys
import pytest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure pytest
def pytest_configure(config):
    """Configure pytest."""
    # Set test environment
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['FLASK_TESTING'] = 'True'


if __name__ == '__main__':
    # Run tests
    exit_code = pytest.main([
        'tests/',
        '-v',
        '--tb=short',
        '--strict-markers'
    ])
    sys.exit(exit_code)
