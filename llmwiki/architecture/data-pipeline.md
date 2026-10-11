---
type: Architecture
title: Data pipeline
description: OR-union query, validation, paged ingest, 512/50 chunks, Ollama embeds, last_sync sync.
tags: [pauli, pipeline]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# Data pipeline

1. AI extracts search terms from each question + session history (no manual input, no hit-count gate; `pauli/questionanswering/extract.py`).[^tech-concept]
2. Ingest per new term: fast slice first (newest ~50–100 OA papers, paged), then background backfill of remaining matches with digest progress. PMCID-dedup, append-only, re-embed new chunks. Raw → `data/topics/<topic-hash>/raw/`, rows → SQLite `data/pauli.db` (single shared corpus, no `topic_hash` filter at retrieval).[^tech-concept]
3. Ingest all matches (no 500-paper cap): paged metadata + OA full text / abstract, progress UI, idempotent resume on PMCID. Raw → `data/topics/<topic-hash>/raw/`, rows → SQLite `data/pauli.db`.[^tech-concept]
4. Index: chunk abstracts/sections (~512 tokens, 50 overlap), embed via user-configured Ollama (`pauli/index/embed.py`, `OLLAMA_EMBED_MODEL` default `nomic-embed-text`; `sentence-transformers/all-MiniLM-L6-v2` offline alternative). Vectors in sqlite-vec with PMCID, title, year, authors, Europe PMC URL, `topic_hash`.[^tech-concept]
5. Sync per-topic `last_sync`: the in-app scheduler queries `FIRST_PDATE:[last_sync TO NOW]` at the Settings cadence (once a week by default). Dedup by PMCID, append-only, re-embed new chunks. Status lives in Settings; delivery failure is shown loudly there.[^tech-concept]

User view: [settings](/workflows/onboarding-buzzwords.md), [tracking](/workflows/tracking-doctor-visit.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
