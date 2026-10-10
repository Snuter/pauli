"""Shared fixtures for UI tests (pytest-playwright)."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def mockup_url() -> str:
    """File URL for the static ui-mockup under test."""
    index = Path(__file__).resolve().parents[2] / "ui-mockup" / "index.html"
    assert index.is_file(), f"mockup not found: {index}"
    return index.as_uri()
