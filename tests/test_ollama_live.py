"""Live Ollama check (real network, stdlib only; skips when unreachable).

Uses `ollama_settings` from `tests/conftest.py` (env/`.env`).
Unit/UI tests stay mocked — this is the only test that dials Ollama.
"""

import json
import urllib.error
import urllib.request

import pytest


def test_live_chat_greeting(ollama_settings):
    if not ollama_settings["chat_model"]:
        pytest.skip("OLLAMA_CHAT_MODEL not configured")
    payload = json.dumps(
        {
            "model": ollama_settings["chat_model"],
            "messages": [{"role": "user", "content": "Say hi briefly."}],
            "stream": False,
        }
    ).encode()
    req = urllib.request.Request(
        f"{ollama_settings['host']}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = json.loads(resp.read().decode())
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        pytest.skip(f"Ollama unreachable: {exc}")
    content = (body.get("message") or {}).get("content") or ""
    assert content.strip() != ""
