"""
Root conftest.py — loads .env before any test runs.

This ensures GEMINI_API_KEY (and other secrets in .env) are available
to all tests, including integration tests that call the real Gemini API.
The .env file is never committed; developers must create it locally.
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
