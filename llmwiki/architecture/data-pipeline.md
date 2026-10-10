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

1. Input 1–5 buzzwords, no defaults. OR-union: `OPEN_ACCESS:Y AND (TITLE_ABS:"<t1>" OR TITLE_ABS:"<t2>" ...)`.[^tech-concept]
2. Validate per term via Europe PMC REST `OPEN_ACCESS:Y AND TITLE_ABS:"<term>"` hit count. Reject empty / single-letter / too-broad (`>50k`) with narrow-down hint.[^tech-concept]
3. Ingest all matches (no 500-paper cap): paged metadata + OA full text / abstract, progress UI, idempotent resume on PMCID. Raw → `data/topics/<topic-hash>/raw/`, rows → SQLite `data/pauli.db`.[^tech-concept]
4. Index: chunk abstracts/sections (~512 tokens, 50 overlap), embed via user-configured Ollama (`pauli/index/embed.py`, `OLLAMA_EMBED_MODEL` default `nomic-embed-text`; `sentence-transformers/all-MiniLM-L6-v2` offline alternative). Vectors in sqlite-vec with PMCID, title, year, authors, Europe PMC URL, `topic_hash`.[^tech-concept]
5. Sync per-topic `last_sync`: `Check for new papers` queries `FIRST_PDATE:[last_sync TO NOW]`. Dedup by PMCID, append-only, re-embed new chunks. UI shows `3 new papers since 2026-09-30`.[^tech-concept]

User view: [onboarding](/workflows/onboarding-buzzwords.md), [tracking](/workflows/tracking-doctor-visit.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
