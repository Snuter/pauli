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

* P0.1 `questionanswering/extract.py`: `build_extraction_prompt(question, history)` + `parse_extraction_response(text)` + `extract_terms(question, history, chat_fn)`. No hit-count gate — normalize/lowercase/dedup only. Verify `test_extract.py` (splits, dedup, history in prompt, empty short-circuits).
* P0.1b REMOVED 2026-10-12 — no persisted term store, no limit/prune. Delete `TermStore` from `pauli/index/terms.py` (keep `get_db_stats(db_path)` only, moved to `pauli/index/stats.py` if cleaner), delete `tests/test_terms.py` prune tests, drop `#terms-limit`/`#prune-freq` from mockup + `test_auto_terms.py` (DB-stats-only `#terms-count`/`#terms-stats`). Verify `pytest` green.
* P0.2 `ingest/europepmc.py`: OR-union `OPEN_ACCESS:Y` ID-first search via `httpx`, newest-first, `pageSize=100`, cap `HIT_LIMIT=50000`, then full fetch ONLY for PMCIDs missing from DB. Verify mocked HTTP, query + paging + ID-filter.[^impl-plan]
* P0.3 DROPPED 2026-10-12 — no `topic_hash`/topics table (single `data/raw/`, global corpus). Keep stable-hash helper only if needed for migration; otherwise delete `ingest/topics.py`. Verify removal + `pytest` green.
* P0.4 `ingest/pipeline.py`: IDs → PMCID-filter against DB → `data/raw/<PMCID>.*` → `papers` rows for new PMCIDs only, paged + resumable on PMCID, async fast-slice (~50–100) + background backfill. Verify 3 mocked papers, idempotent rerun, no re-download of stored PMCIDs.[^impl-plan]
* P0.5 `index/chunk.py`: ~512/50 deterministic, no network. Verify size/overlap/PMCID link.[^impl-plan]
* P0.6 `index/embed.py`: `embed(texts)` via Ollama `nomic-embed-text`, alt `all-MiniLM-L6-v2`. Verify mocked vectors, swappable.[^impl-plan]
* P0.7 `index/store.py`: insert + `search_vectors(vec, top_k)` GLOBAL (no `topic_hash` arg; column may persist as provenance but is never filtered). Verify 5-chunk global search.[^impl-plan]
* P0.8 `ingest/sync.py`: re-extract terms from stored past questions of subscribed sessions, same ID-first lookup (`pageSize=100`/`HIT_LIMIT=50000`), PMCID dedup vs DB, append-only, re-embed, count. No `FIRST_PDATE` window. Verify `test_sync_dedup.py`.[^impl-plan]
* P0-gate manual: real topic fetch, cache hit, links resolve; `pytest` green.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
