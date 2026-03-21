"""
Pytest configuration for the seed crawler pipeline tests.
Adds the crawl4ai root to sys.path so imports work naturally.
"""

import sys
from pathlib import Path

# Add crawl4ai/ to sys.path so `from config import ...` etc. work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "network: marks tests that require network access (deselect with '-m \"not network\"')",
    )
