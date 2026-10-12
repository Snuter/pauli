"""Shared fixtures for implementation tests: `.env` + Ollama settings."""

import os
from pathlib import Path

import pytest


def _load_dotenv() -> None:
    """Minimal `.env` loader (no dependency): env vars take precedence."""
    env_file = Path(__file__).resolve().parents[1] / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        os.environ.setdefault(key, value)


_load_dotenv()


@pytest.fixture(scope="session")
def ollama_settings() -> dict:
    """Ollama connection settings from env/`.env` (README defaults)."""
    return {
        "host": os.getenv("OLLAMA_HOST", "").rstrip("/"),
        "chat_model": os.getenv("OLLAMA_CHAT_MODEL", ""),
        "embed_model": os.getenv("OLLAMA_EMBED_MODEL", ""),
        "api_key": os.getenv("OLLAMA_API_KEY", ""),
    }
