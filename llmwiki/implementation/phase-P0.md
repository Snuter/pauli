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

Implements [data pipeline](/architecture/data-pipeline.md). Build order P0.1->P0.2->P0.4->P0.5->P0.6->P0.7->P0.8; P0.5/P0.6 independently testable offline. Canonical `pauli/config.py` (`PAGESIZE=100`, `HIT_LIMIT=50000`, `OPEN_ACCESS:Y`) + `pauli/db.py:SCHEMA_SQL`. Mock HTTP via `httpx.MockTransport`; mock vectors as fixed-dim lists.[^impl-plan]

* P0.1 `questionanswering/extract.py` DONE: `build_extraction_prompt(question:str,history:Sequence[str])->str` + `parse_extraction_response(text:str)->list[str]` + `extract_terms(question,history,chat_fn)->list[str]`. No hit-count gate. Verify: `poetry run pytest tests/test_extract.py -q`. Forbidden: no `TermStore`, no per-term validation.
* P0.1b DONE 2026-10-13 unless residue remains — no persisted term store/limit/prune. Guard: `grep -q TermStore pauli/index/terms.py && <delete it> || true`; keep `get_db_stats(db_path)->dict` only, prune tests already removed from `tests/test_terms.py`, `#terms-limit`/`#prune-freq` already dropped from mockup + `test_auto_terms.py` (DB-stats-only `#terms-count`/`#terms-stats`). Verify: `poetry run pytest tests/test_terms.py tests/ui/test_auto_terms.py -q`. Forbidden: no limit/prune UI.
* P0.2 `ingest/europepmc.py`: `build_query(terms:list[str])->str` (OR-union + `OPEN_ACCESS:Y`) + `search_ids(query,page:int)->tuple[list[str],int]` (newest-first, `pageSize=100`, cap `HIT_LIMIT=50000`) + `fetch_full(pmcids:list[str])->list[dict]` ONLY for PMCIDs missing from DB, `httpx` timeout 30s, retry 2x on 5xx/timeout. Contract frozen in [data pipeline](/architecture/data-pipeline.md) (REST `search?query=...&format=json` + `fullTextXML`, example query + minimal JSON fixture). Parse: agent picks JATS handling but must document tags kept/stripped in-module + 404->abstract fallback. Verify: `poetry run pytest tests/test_europepmc.py -q` (mocked paging, ID-filter, retry). Forbidden: no non-OA bulk scrape, no `FIRST_PDATE` window filter (`FIRST_PDATE_D` sort still required).
* P0.3 DONE 2026-10-13 unless residue remains — no `topic_hash`/topics table. Guard: `test -f pauli/ingest/topics.py && rm pauli/ingest/topics.py || true`. Verify: `grep -r topic_hash pauli/ llmwiki/ --include='*.py' --include='*.md' | grep -v DROPPED | grep -v glossary; poetry run pytest tests/test_db.py -q`. Forbidden: no `topic_hash` column/filter.
* P0.4 `ingest/pipeline.py`: `filter_missing(pmcids,db_path)->list[str]` (PMCID vs `papers`) + `download_missing(pmcids,raw_dir)->list[Path]` (`data/raw/<PMCID>.*`) + `upsert_papers(records,db_path)->int`, paged + resumable on PMCID; `run_fast_slice(terms)->answer(incomplete=True)` (~50-100 newest) + `backfill_thread(job_id)` + `GET digest-progress` JSON poll 2s + manual `refresh-answer`. Signatures stay minimal (decided 2026-10-15): deps (`db_path`, `chat_fn`/`Settings`) resolved via module import and documented in-module, not added as params. Verify: `poetry run pytest tests/test_pipeline.py -q` (3 mocked papers, idempotent rerun, zero re-download). Forbidden: no query log.
* P0.5 `index/chunk.py`: `chunk_text(text:str,pmcid:str)->list[dict{id,pmcid,idx,text}]` ~512/50 word-based deterministic, no network. Verify: `poetry run pytest tests/test_chunk.py -q` (size/overlap/PMCID link). Forbidden: no network calls.
* P0.6 `index/embed.py`: `embed(texts:list[str])->list[list[float]]` via canonical `import ollama` (`ollama.Client`, `OLLAMA_EMBED_MODEL` `nomic-embed-text`), alt `all-MiniLM-L6-v2` offline; batch ≤64. Verify: `poetry run pytest tests/test_embed.py -q` (mocked vectors, swappable dim). Forbidden: no API key in logs, no raw httpx Ollama calls.
* P0.7 `index/store.py`: `insert_chunks(rows,db_path)->int` + `search_vectors(vec,top_k=15,threshold:float|None,db_path)->list[dict{pmcid,text,score}]` GLOBAL cosine via sqlite-vec (no `topic_hash` arg) — store owns threshold + `TOP_K` filtering (decided 2026-10-15; `retrieve.py` passes `threshold=strictness/100*0.6` through, no second filter). DDL agent-picks (decided 2026-10-15) but must document in-module: `vec0` vs `BLOB`, float32 serialize, extension load, dim-mismatch fail-closed. Verify: `poetry run pytest tests/test_store.py -q` (5-chunk global search + threshold/TOP_K respected). Forbidden: no `topic_hash` filter.
* P0.8 `ingest/sync.py`: `collect_subscribed_questions(db_path)->dict[session_id,list[str]]` + `sync_subscribed(db_path)->dict{new_pmcids:int}` (re-extract via `extract.py`, same ID-first lookup, PMCID dedup, append-only, re-embed). Signature stays minimal (decided 2026-10-15): `chat_fn`/`Settings` resolved inside via import + `ollama_api_key()`, documented in-module. Shared with `tracker/sync_cron.py` (P3.1 calls this; no duplicate logic). Verify: `poetry run pytest tests/test_sync_dedup.py -q`. Forbidden: no `FIRST_PDATE` window filter, no deletes/updates.
* P0-gate: `poetry run pytest tests/test_europepmc.py tests/test_pipeline.py tests/test_chunk.py tests/test_embed.py tests/test_store.py tests/test_sync_dedup.py -q` green + manual real-topic fetch/cache-hit/links-resolve.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
