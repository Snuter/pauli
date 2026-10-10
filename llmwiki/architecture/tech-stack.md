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

Backend FastAPI, SQLite + sqlite-vec, Ollama embeddings. Hand-rolled RAG only (no LangChain/LlamaIndex/Haystack); embeddings behind `pauli/index/embed.py` (`OLLAMA_EMBED_MODEL` default `nomic-embed-text`, `sentence-transformers/all-MiniLM-L6-v2` offline alt); vectors in `data/pauli.db` with `topic_hash` filter, append-only sync; generation via `ollama-python` on `OLLAMA_HOST` + `OLLAMA_CHAT_MODEL`, never opencode; citation/abstain in code; revisit LlamaIndex only for hybrid/rerank need.[^tech-concept] Frontend: FastAPI + Jinja + HTMX only.[^tech-concept]

LLM: user-configured Ollama local/cloud. `OLLAMA_HOST` (default `http://localhost:11434`), `OLLAMA_CHAT_MODEL` / `OLLAMA_EMBED_MODEL` (no shipped chat default), `OLLAMA_API_KEY` cloud-only via env/gitignored `.env`, never logged. Fail closed on missing model/key. `setup_dev_ai.sh` is dev-only, not runtime. Local keeps queries on-machine; cloud follows provider terms; retrieval stays local.[^tech-concept]

Layout: `pauli/ingest/`, `pauli/index/`, `pauli/questionanswering/`, `pauli/safety/`, `pauli/web/`, `data/`, `tests/`. MVP: local web app + RAG, Python >=3.13, Poetry, pytest; OA-only compliance.[^tech-concept]

[^tech-concept]: P.A.U.L.I. Technical Concept
