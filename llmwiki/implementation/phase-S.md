---
type: Phase
title: Phase S — skeleton + config + DB
description: Deps, skeleton, config constants, DB tables, gitignore (S1-S5).
tags: [pauli, phase-S]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: impl-plan
    resource: /docs/implementation-plan.md
    title: P.A.U.L.I. Implementation Plan
---

# Phase S

Prereq for all P0–P3.[^impl-plan]

* S1 Deps in `pyproject.toml`: `fastapi`, `uvicorn`, `httpx`, `sqlite-vec`, `ollama-python`, `jinja2`, `textstat`, `apscheduler` (daily sync+notify; mail send via stdlib `smtplib`); `sentence-transformers` optional. Test deps: `pytest`, `playwright`, `pytest-playwright` (+ `poetry run python -m playwright install chromium` for the browser binary). Verify: `poetry install`, `pytest` collects.[^impl-plan]
* S2 Skeleton `__init__.py` per dir: `pauli/ingest/`, `pauli/index/`, `pauli/questionanswering/`, `pauli/safety/`, `pauli/tracker/`, `pauli/web/`, `tests/`, `tests/ui/`. Verify: `import pauli`.[^impl-plan]
* S3 `pauli/config.py` (canonical: `CONFIG_PATH=data/config.json` JSON, `DB_PATH=data/pauli.db`, `RAW_DIR=data/raw/<PMCID>.*`): `CHUNK_TOKENS=512`/`CHUNK_OVERLAP=50` words, `TOP_K=15`, `SCORE_THRESHOLD=0.3`, strictness `0-100` -> `threshold=strictness/100*0.6` (`strictness_to_threshold()`), `HIT_LIMIT=50000`+`PAGESIZE=100`+newest-first+`OPEN_ACCESS:Y`, `Settings` dataclass (`ollama_host/chat_model/embed_model/mode`, sliders, `sensitivity low|standard|hide`, `mail_to/from/smtp/freq daily|weekly|monthly` default `weekly`) with `validate()`/`load_settings()`/`save_settings()` (never persists `OLLAMA_API_KEY`; key from env only via `ollama_api_key()`). Verify: `poetry run pytest tests/test_config.py -q`. Forbidden: no `topic_hash`, no LangChain/SQLAlchemy/Alembic, no key in logs/file.[^impl-plan]
* S4 `pauli/db.py` (canonical `SCHEMA_SQL` + `init_db(path)`): `papers(pmcid TEXT PK, title TEXT NOT NULL, year INTEGER, authors TEXT, url TEXT, abstract TEXT)`, `chunks(id INTEGER PK, pmcid TEXT FK, idx INTEGER, text TEXT, vec BLOB)` + `idx_chunks_pmcid`, `answers(id, question, answer, mode)`, `sessions(id TEXT PK, title TEXT UNIQUE, created_at INTEGER, subscribed INTEGER DEFAULT 0)`, `session_answers(session_id FK, question, answer_id FK, position INTEGER)` + index, `sync_state(id CHECK(id=1), last_run TEXT)`, `warning_events(id, category, action, mode, at)` — no PHI, no `topic_hash`. Verify: `poetry run pytest tests/test_db.py -q` (temp DB, init idempotent, UNIQUE title enforced). Forbidden: no per-topic tables, no `topic_hash` column/filter.[^impl-plan]
* S5 Gitignore `data/pauli.db`, `data/raw/`, `data/config.json`, `.env`. Verify: `git status` clean after ingest; `git check-ignore data/pauli.db data/config.json .env`.


[^impl-plan]: P.A.U.L.I. Implementation Plan
