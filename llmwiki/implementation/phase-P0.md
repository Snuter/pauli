---
type: Phase
title: Phase P0 — cache + search
description: Validate, Europe PMC fetch, topics, pipeline, chunk, embed, store, sync (P0.1-P0.8).
tags: [pauli, phase-P0]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: impl-plan
    resource: /docs/implementation-plan.md
    title: P.A.U.L.I. Implementation Plan
---

# Phase P0

Implements [data pipeline](/architecture/data-pipeline.md).[^impl-plan]

* P0.1 `ingest/validate.py`: 1–5 terms, reject empty/1-char/`>50k`, narrow hint. Pure function taking hit-count callback — no HTTP inside. Verify `test_validate.py` (0 terms, 6 terms, empty, 1-char, broad-term hint).[^impl-plan]
* P0.2 `ingest/europepmc.py`: OR-union search via `httpx`, per-term counts, paged full fetch, OA fullText/abstract, OA-only. Verify mocked HTTP, query + paging.[^impl-plan]
* P0.3 `ingest/topics.py`: `topic_hash` + `last_sync` CRUD. Verify stable hash, round-trip.[^impl-plan]
* P0.4 `ingest/pipeline.py`: fetch → raw files → `papers` rows, paged + resumable on PMCID. Verify 3 mocked papers, idempotent rerun.[^impl-plan]
* P0.5 `index/chunk.py`: ~512/50 deterministic, no network. Verify size/overlap/PMCID link.[^impl-plan]
* P0.6 `index/embed.py`: `embed(texts)` via Ollama `nomic-embed-text`, alt `all-MiniLM-L6-v2`. Verify mocked vectors, swappable.[^impl-plan]
* P0.7 `index/store.py`: insert + `search_vectors(topic_hash, vec, top_k)`. Verify 5-chunk filtered search.[^impl-plan]
* P0.8 `ingest/sync.py`: `FIRST_PDATE:[last_sync TO NOW]`, PMCID dedup, append-only, re-embed, count. Verify `test_sync_dedup.py`.[^impl-plan]
* P0-gate manual: real topic fetch, cache hit, links resolve; `pytest` green.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
