"""Canonical runtime config (Phase S3).

Single source of truth for paths, RAG constants, and user settings.

- Runtime user settings persist in ``data/config.json`` (JSON, decided per
  review 2026-10-13; ``.env`` is secrets-only for ``OLLAMA_API_KEY``).
- Env takes precedence for ``OLLAMA_HOST`` / models only when set; file wins
  for sliders/sensitivity/mail. ``OLLAMA_API_KEY`` comes from env only and is
  never written to ``data/config.json`` or logs.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass

CONFIG_PATH = os.path.join("data", "config.json")
DB_PATH = os.path.join("data", "pauli.db")
RAW_DIR = os.path.join("data", "raw")

CHUNK_TOKENS = 512
CHUNK_OVERLAP = 50
TOP_K = 15
SCORE_THRESHOLD = 0.3
HIT_LIMIT = 50000
PAGESIZE = 100
OPEN_ACCESS_FILTER = "OPEN_ACCESS:Y"

OLLAMA_HOST_DEFAULT = "http://localhost:11434"
OLLAMA_EMBED_MODEL_DEFAULT = "nomic-embed-text"
# No shipped chat default: user must pick in Settings.
OLLAMA_CHAT_MODEL_DEFAULT = ""
OLLAMA_MODES = ("local", "cloud")

EMAIL_RE = r"[^@\s]+@[^@\s]+\.[^@\s]+"

# Canonical 422 fragment: routes return this HTML with status 422; dialog stays open.
# Kept here so routes + tests share one shape. Escaped, no secrets echoed.
def validation_error_fragment(message: str) -> str:
    import html as _html

    return f'<p class="meta" role="alert">{_html.escape(message, quote=True)}</p>'


def is_valid_host(host: str) -> bool:
    from urllib.parse import urlparse as _urlparse

    try:
        u = _urlparse((host or "").strip())
    except ValueError:
        return False
    return u.scheme in ("http", "https") and bool(u.netloc) and " " not in (host or "")


def is_valid_email(addr: str) -> bool:
    import re as _re

    return bool(_re.fullmatch(EMAIL_RE, (addr or "").strip()))


def is_valid_smtp(smtp: str) -> bool:
    """Explicit host:port only. Bare host without port is invalid (422)."""
    s = (smtp or "").strip()
    if ":" not in s or " " in s:
        return False
    host, _, port = s.rpartition(":")
    if not host or not port.isdigit():
        return False
    return 1 <= int(port) <= 65535


def validate_ollama_form(host: str, chat_model: str, embed_model: str, mode: str) -> list[str]:
    """Strict POST /settings/ollama validation (422 on any error).

    Stricter than Settings.validate(): chat_model is required here.
    Key (cloud-only) is never passed here; it comes from env only.
    """
    errors: list[str] = []
    if not is_valid_host(host or ""):
        errors.append("ollama host must be http(s) URL")
    if (mode or "") not in OLLAMA_MODES:
        errors.append(f"ollama mode must be one of {OLLAMA_MODES}")
    if not (chat_model or "").strip() or len((chat_model or "").strip()) > 100:
        errors.append("chat_model is required (1-100 chars, no shipped default)")
    if not (embed_model or "").strip() or len((embed_model or "").strip()) > 100:
        errors.append("embed_model is required (1-100 chars)")
    return errors


def validate_mail_form(to: str, from_: str, smtp: str, freq: str) -> list[str]:
    """Strict POST /settings/mail validation.

    All-empty means disabled (valid). Otherwise to+from+smtp+freq all required:
    to/from must be email, smtp must be host:port, freq must be known.
    """
    errors: list[str] = []
    if not (to or "").strip() and not (from_ or "").strip() and not (smtp or "").strip():
        if (freq or "") not in TRACKER_FREQ_OPTIONS:
            errors.append(f"mail_freq must be one of {TRACKER_FREQ_OPTIONS}")
        return errors
    if not is_valid_email(to or ""):
        errors.append("mail to must be a valid email")
    if not is_valid_email(from_ or ""):
        errors.append("mail from must be a valid email")
    if not is_valid_smtp(smtp or ""):
        errors.append("mail smtp must be host:port (explicit port required)")
    if (freq or "") not in TRACKER_FREQ_OPTIONS:
        errors.append(f"mail_freq must be one of {TRACKER_FREQ_OPTIONS}")
    return errors

SIMPLICITY_MIN, SIMPLICITY_MAX, SIMPLICITY_DEFAULT = 10, 15, 12
STRICTNESS_MIN, STRICTNESS_MAX, STRICTNESS_DEFAULT = 0, 100, 50
SENSITIVITY_MODES = ("low", "standard", "hide")
SENSITIVITY_DEFAULT = "standard"
TRACKER_FREQ_DEFAULT = "weekly"
TRACKER_FREQ_OPTIONS = ("daily", "weekly", "monthly")


def strictness_to_threshold(strictness: int) -> float:
    """Linear mapping: threshold = strictness/100*0.6 (cosine via sqlite-vec)."""
    s = max(STRICTNESS_MIN, min(STRICTNESS_MAX, int(strictness)))
    return s / 100 * 0.6


@dataclass
class Settings:
    ollama_host: str = OLLAMA_HOST_DEFAULT
    ollama_chat_model: str = OLLAMA_CHAT_MODEL_DEFAULT
    ollama_embed_model: str = OLLAMA_EMBED_MODEL_DEFAULT
    ollama_mode: str = "local"
    strictness: int = STRICTNESS_DEFAULT
    simplicity: int = SIMPLICITY_DEFAULT
    sensitivity: str = SENSITIVITY_DEFAULT
    mail_to: str = ""
    mail_from: str = ""
    mail_smtp: str = ""
    mail_freq: str = TRACKER_FREQ_DEFAULT

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not (SIMPLICITY_MIN <= self.simplicity <= SIMPLICITY_MAX):
            errors.append(f"simplicity must be {SIMPLICITY_MIN}-{SIMPLICITY_MAX}")
        if not (STRICTNESS_MIN <= self.strictness <= STRICTNESS_MAX):
            errors.append(f"strictness must be {STRICTNESS_MIN}-{STRICTNESS_MAX}")
        if self.sensitivity not in SENSITIVITY_MODES:
            errors.append(f"sensitivity must be one of {SENSITIVITY_MODES}")
        if self.mail_freq not in TRACKER_FREQ_OPTIONS:
            errors.append(f"mail_freq must be one of {TRACKER_FREQ_OPTIONS}")
        # Strict-but-default-safe checks (defaults pass; empty mail = disabled).
        # POST routes use validate_ollama_form/validate_mail_form for stricter
        # chat_model-required / all-or-nothing mail rules.
        if not is_valid_host(self.ollama_host):
            errors.append("ollama_host must be http(s) URL")
        if self.ollama_mode not in OLLAMA_MODES:
            errors.append(f"ollama_mode must be one of {OLLAMA_MODES}")
        if not (self.ollama_embed_model or "").strip():
            errors.append("ollama_embed_model is required")
        if (self.mail_to or "").strip() and not is_valid_email(self.mail_to):
            errors.append("mail_to must be a valid email")
        if (self.mail_from or "").strip() and not is_valid_email(self.mail_from):
            errors.append("mail_from must be a valid email")
        if (self.mail_smtp or "").strip() and not is_valid_smtp(self.mail_smtp):
            errors.append("mail_smtp must be host:port (explicit port required)")
        return errors


def load_settings(path: str = CONFIG_PATH) -> Settings:
    """Load JSON settings; missing file -> defaults. Never reads API key."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    data.pop("ollama_api_key", None)
    known = {k for k in asdict(Settings())}
    return Settings(**{k: v for k, v in data.items() if k in known})


def save_settings(settings: Settings, path: str = CONFIG_PATH) -> None:
    """Persist settings as JSON. Never persists API key."""
    errors = settings.validate()
    if errors:
        raise ValueError("; ".join(errors))
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(settings), f, indent=2, sort_keys=True)


def ollama_api_key() -> str:
    """Cloud-only key from env; never from config file."""
    return os.environ.get("OLLAMA_API_KEY", "")
