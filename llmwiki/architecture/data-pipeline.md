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
2. Lookup per Ask (async backfill): ID-first Europe PMC REST query — OR-union, `OPEN_ACCESS:Y`, newest-first, paged IDs (`pageSize=100`, cap `HIT_LIMIT=50000` IDs per Ask/sync, approved 2026-10-12); compare returned PMCIDs against `papers(pmcid)` in `data/pauli.db`; download full text/abstract ONLY for PMCIDs not already stored. Fast slice first (newest ~50–100 OA papers) so Ask answers immediately marked incomplete with digest progress + manual `Refresh answer`; remaining new matches backfill in a background thread (decided 2026-10-12; HTMX polling for progress, manual `Refresh answer`), append-only, re-embed new chunks. Raw → `data/raw/<PMCID>.*` (single shared dir, hash dirs dropped 2026-10-12), rows → SQLite `data/pauli.db` (single shared corpus, no `topic_hash` filter at retrieval). Vector DB grows monotonically; no term cap/prune.[^tech-concept]

Contract (frozen 2026-10-13, REST search + fullTextXML, JSON; signatures frozen 2026-10-15 per user Q&A):
* Search: `GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={query}&format=json&pageSize=100&cursorMark=*&sort=FIRST_PDATE_D desc` with `query=(term1 OR term2) AND OPEN_ACCESS:Y`. Example: `(myalgic encephalomyelitis OR PEM) AND OPEN_ACCESS:Y`. Note: `FIRST_PDATE_D` here is a sort key only, not a date-window filter (date-window filtering stays banned).
* Paging: follow `nextCursorMark` until `hitCount` exhausted or `HIT_LIMIT=50000` IDs; `httpx` timeout 30s, retry 2x on 5xx/timeout, honor `Retry-After`. Stream IDs (never hold >1000 raw records in RAM; PMCID-filter incrementally).
* Minimal search fixture: `{"hitCount":1,"resultList":{"result":[{"pmcid":"PMC1234567","title":"X","authorString":"A et al.","pubYear":"2024","inEPMC":"Y","isOpenAccess":"Y"}]},"nextCursorMark":"*"}`.
* Full text: `GET https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML` (fallback: use abstract from the search result when full text returns 404; no second endpoint in MVP). Store raw bytes to `data/raw/<PMCID>.xml` (+ `.json` search record). JATS frozen: keep text of `<abstract>`, `<article-title>`, `<sec>`, `<title>`, `<p>`; strip `<ref-list>`, `<fig>`, `<table-wrap>`, `<disp-formula>`, `<inline-formula>`, `<supplementary-material>`; guarantee: 404 -> abstract fallback, never empty string without `unknown` path, idempotent on PMCID. Canonical `chat_fn(prompt)->str` for all LLM calls (single prompt string in/out).
* `P0.2` mock strategy: `httpx.MockTransport` serving the fixture above; assert OR-union query string, newest-first sort param, PMCID-filter, retry count.[^tech-concept]
3. Index: chunk abstracts/sections (~512 words, 50-word overlap, decided 2026-10-12), embed via user-configured Ollama (`pauli/index/embed.py`, `OLLAMA_EMBED_MODEL` default `nomic-embed-text`; `sentence-transformers/all-MiniLM-L6-v2` offline alternative). Vectors frozen (2026-10-15): `chunks.vec BLOB` float32 little-endian (via `struct`, dim = embedding width, stored alongside in code assert) + Python cosine in `index/store.py`; no `vec0` virtual table in MVP (no native extension load). No `topic_hash`. Idempotent resume on PMCID. `search_vectors(vec,top_k=15,threshold,db_path)` stays GLOBAL, owns threshold + `TOP_K` filtering; fail closed on embedding-dim mismatch.[^tech-concept]
4. Sync (decided 2026-10-12, signatures frozen 2026-10-15): explicit params only (no hidden imports): `ingest/sync.py: collect_subscribed_questions(db_path)->dict[session_id,list[str]]` + `sync_subscribed(db_path,settings,chat_fn)->dict{new_pmcids:int}` (re-extract via `extract.py`, same ID-first lookup, PMCID dedup, append-only, re-embed). `ingest/pipeline.py: filter_missing(pmcids,db_path)->list[str]` + `download_missing(pmcids,raw_dir)->list[Path]` + `upsert_papers(records,db_path)->int` + `run_fast_slice(terms,db_path,settings,chat_fn)->dict{answer,incomplete,remaining}` (~50-100 newest fast slice; `remaining` = count of unfetched PMCIDs = `digest-progress count`) + `backfill_job(job_id,terms,db_path,settings,chat_fn)->None` (background thread, updates in-memory `{digesting,count}` owned by `web/app.py`). `tracker/sync_cron.py:run_once()` calls `sync_subscribed` (no duplicate logic).

User view: [settings](/workflows/onboarding-buzzwords.md), [tracking](/workflows/tracking-doctor-visit.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
