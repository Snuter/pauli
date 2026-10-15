"""Phase S3 verify: config importable, JSON round-trip, no key persistence."""

import json
import os

from pauli import config as C


def test_constants():
    assert C.CHUNK_TOKENS == 512
    assert C.CHUNK_OVERLAP == 50
    assert C.TOP_K == 15
    assert C.SCORE_THRESHOLD == 0.3
    assert C.CONFIG_PATH == os.path.join("data", "config.json")
    assert C.strictness_to_threshold(50) == 0.3


def test_settings_roundtrip_no_key(tmp_path, monkeypatch):
    monkeypatch.setenv("OLLAMA_API_KEY", "secret")
    s = C.Settings()
    assert s.validate() == []
    p = str(tmp_path / "config.json")
    C.save_settings(s, p)
    raw = json.loads(open(p).read())
    assert "ollama_api_key" not in raw
    assert "secret" not in open(p).read()
    assert C.load_settings(p) == s


def test_settings_validation():
    s = C.Settings(simplicity=9)
    assert s.validate()
