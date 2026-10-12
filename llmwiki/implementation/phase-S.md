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
* S3 `pauli/config.py`: paths (`data/pauli.db`, `data/raw/<PMCID>.*` single shared dir, settings config file in `data/` decided 2026-10-12), `CHUNK_TOKENS=512` words / `CHUNK_OVERLAP=50` words (word-based, decided 2026-10-12), `TOP_K=15`, `SCORE_THRESHOLD=0.3`, strictness `0–100` → `threshold = strictness/100*0.6` linear with cosine similarity via sqlite-vec (decided 2026-10-12), `HIT_LIMIT=50000` (max paged Europe PMC IDs per Ask/sync; approved 2026-10-12) + `PAGESIZE=100` + newest-first, `OPEN_ACCESS:Y` OR-union; Ollama `OLLAMA_HOST` (default `http://localhost:11434`), `OLLAMA_CHAT_MODEL` + `OLLAMA_EMBED_MODEL` (`nomic-embed-text`), `OLLAMA_API_KEY` cloud-only. No `setup_dev_ai.sh` / `MODEL`. Verify: constants importable, no hardcoded topics, misconfiguration error.[^impl-plan]
* S4 `pauli/db.py`: single shared corpus (global retrieval): tables `sync_state(last_run)` (scheduler status only; `topics` table DROPPED 2026-10-12 — no query log, no hash dirs), `papers(pmcid PK, title, year, authors, url, abstract)`, `chunks(id, pmcid, idx, text, vec)`, `answers(id, question, answer, mode)`, `sessions(id, title UNIQUE, created_at, subscribed INTEGER DEFAULT 0)`, `session_answers(session_id, question, answer_id, position)` (ordered by `position`/`rowid`), `warning_events(category, action, mode, at — no PHI)`. Verify: `tests/test_db.py` temp DB + global search (no filter arg).[^impl-plan]
* S5 Gitignore `data/pauli.db`, `data/topics/`. Verify: `git status` clean after ingest.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
