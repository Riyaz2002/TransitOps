"""Shared pytest setup.

These environment variables are set before importing ``app``.  They make
settings valid during tests without reading or using your real .env file.
"""

import os

os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/transitops_test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-long-enough-for-safe-validation")

import pytest

from app.core.config import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    """Keep settings isolated if a test changes environment variables."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
