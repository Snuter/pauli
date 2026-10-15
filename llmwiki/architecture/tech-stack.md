---
type: Architecture
title: Tech stack + layout
description: FastAPI/HTMX, sqlite-vec, hand-rolled RAG, Ollama config, package layout.
tags: [pauli, stack]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# Tech stack

Backend FastAPI, SQLite + sqlite-vec, Ollama embeddings. Hand-rolled RAG only (no LangChain/LlamaIndex/Haystack); embeddings behind `pauli/index/embed.py` (`OLLAMA_EMBED_MODEL` default `nomic-embed-text`, `sentence-transformers/all-MiniLM-L6-v2` offline alt); vectors in `data/pauli.db` as one single shared corpus (global, no `topic_hash` filter at retrieval), append-only sync; raw papers in single shared `data/raw/<PMCID>.*` (hash dirs dropped 2026-10-12); generation via `import ollama` canonical (`ollama.Client(host=OLLAMA_HOST, api_key=...)` for chat + embeddings; raw `httpx` POST to `/api/chat` is mockup-only and forbidden in backend, decided 2026-10-15), never opencode; citation/abstain in code; revisit LlamaIndex only for hybrid/rerank need.[^tech-concept] Frontend: FastAPI + Jinja + HTMX only, replicating `ui-mockup/` element IDs/flows — see [web API](web-api.md) (templates + fragment example frozen 2026-10-15).[^tech-concept]

Runtime wiring (decided 2026-10-15): `pauli/web/app.py` lifespan starts `APScheduler` (cadence `mail_freq`) + owns in-memory backfill-job lock (`job_id -> {digesting,count}` for `GET digest-progress` 2s poll); scheduler + backfill build `chat_fn` at run time from loaded `Settings` + `ollama_api_key()` (env-only). No OS cron.

LLM: user-configured Ollama local/cloud. `OLLAMA_HOST` (default `http://localhost:11434`), `OLLAMA_CHAT_MODEL` / `OLLAMA_EMBED_MODEL` (no shipped chat default), `OLLAMA_API_KEY` cloud-only via env/gitignored `.env`, never logged. Runtime user settings persist in `data/config.json` (JSON, never written with secrets). Fail closed on missing model/key. `setup_dev_ai.sh` is dev-only, not runtime. Local keeps queries on-machine; cloud follows provider terms; retrieval stays local.[^tech-concept]

Layout: `pauli/ingest/`, `pauli/index/`, `pauli/questionanswering/`, `pauli/safety/`, `pauli/tracker/`, `pauli/web/` (`app.py`, `routes_sessions.py`, `routes_chat.py`, `routes_settings.py`, `templates/` frozen in [web API](web-api.md)), `data/`, `tests/` (unit/integration) + `tests/ui/` (python-playwright UI). MVP: local web app + RAG, Python >=3.13, Poetry, pytest + `playwright`/`pytest-playwright` dev deps; OA-only compliance.[^tech-concept] Test layers, commands, conventions — [testing strategy](/architecture/testing.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
