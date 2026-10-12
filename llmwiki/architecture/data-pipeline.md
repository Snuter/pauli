---
type: Architecture
title: Data pipeline
description: OR-union query, validation, paged ingest, 512/50 word chunks, Ollama embeds, sync_state sync.
tags: [pauli, pipeline]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# Data pipeline — single shared corpus, transient terms, ID-first dedup

1. AI extracts transient search terms from each question + session history (no manual input, no hit-count gate, no persisted term store; `pauli/questionanswering/extract.py`). Terms live only for that lookup.[^tech-concept]
2. Lookup per Ask (async backfill): ID-first Europe PMC query — OR-union, `OPEN_ACCESS:Y`, newest-first, paged IDs (`pageSize=100`, cap `HIT_LIMIT=50000` IDs per Ask/sync, approved 2026-10-12); compare returned PMCIDs against `papers(pmcid)` in `data/pauli.db`; download full text/abstract ONLY for PMCIDs not already stored. Fast slice first (newest ~50–100 OA papers) so Ask answers immediately marked incomplete with digest progress + manual `Refresh answer`; remaining new matches backfill in a background thread (decided 2026-10-12; HTMX polling for progress, manual `Refresh answer`), append-only, re-embed new chunks. Raw → `data/raw/<PMCID>.*` (single shared dir, hash dirs dropped 2026-10-12), rows → SQLite `data/pauli.db` (single shared corpus, no `topic_hash` filter at retrieval). Vector DB grows monotonically; no term cap/prune.[^tech-concept]
3. Index: chunk abstracts/sections (~512 words, 50-word overlap, decided 2026-10-12), embed via user-configured Ollama (`pauli/index/embed.py`, `OLLAMA_EMBED_MODEL` default `nomic-embed-text`; `sentence-transformers/all-MiniLM-L6-v2` offline alternative). Vectors in sqlite-vec with PMCID, title, year, authors, Europe PMC URL (no `topic_hash`). Idempotent resume on PMCID.[^tech-concept]
4. Sync (decided 2026-10-12): no persisted query log. On each scheduled run the scheduler re-extracts terms from stored past questions (subscribed sessions only) via `extract.py`, OR-unions per session, runs the same ID-first lookup (`pageSize=100`, `HIT_LIMIT=50000`), PMCID-filters against the DB, and downloads/digests only missing PMCIDs. No `FIRST_PDATE` window needed — PMCID-dedup is the new-only guarantee. Global `sync_state(last_run)` records run time for Settings status; delivery failure shown loudly there.[^tech-concept]

User view: [settings](/workflows/onboarding-buzzwords.md), [tracking](/workflows/tracking-doctor-visit.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
