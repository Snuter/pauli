# P.A.U.L.I. — Implementation Plan

Source: `docs/concept-technical.md` + `docs/concept-user-journey.md`.
Stack: Python >=3.13, Poetry, pytest, FastAPI, SQLite + sqlite-vec, Ollama-local.
Constraints: no built-in default topics in code or DB; OA subset only; weekly manual sync, no cron.

Conventions used below: each step is one unit of work. `Verify:` is the done-criteria. Run `poetry run pytest tests/<file>` after each code step.

## Phase S — Skeleton + config + DB (prereq for all P0–P3)

- [ ] S1 Add runtime deps to `pyproject.toml`: `fastapi`, `uvicorn`, `httpx`, `sqlite-vec`, `ollama-python`, `jinja2`. Keep `sentence-transformers` optional (alternative embed backend only).
      Verify: `poetry install` succeeds, `poetry run pytest` collects (0 tests OK).
- [ ] S2 Create package skeleton with `__init__.py` per dir: `pauli/ingest/`, `pauli/index/`, `pauli/questionanswering/`, `pauli/safety/`, `pauli/tracker/`, `pauli/web/`, `tests/`. No logic yet.
      Verify: `poetry run python -c "import pauli"` succeeds.
- [ ] S3 Add `pauli/config.py`: paths (`data/pauli.db`, `data/topics/<hash>/raw/`), `MODEL` env default matching `setup_dev_ai.sh`, `CHUNK_TOKENS=512`, `CHUNK_OVERLAP=50`, `TOP_K`, `SCORE_THRESHOLD`, `HIT_LIMIT=50000`, `OPEN_ACCESS:Y` filter.
      Verify: unit test asserts constants importable; no topic strings hardcoded.
- [ ] S4 Add `pauli/db.py`: init + migrate SQLite + sqlite-vec tables `topics(hash, terms_json, last_sync)`, `papers(pmcid PK, topic_hash, title, year, authors, url, abstract)`, `chunks(id, pmcid, topic_hash, idx, text, vec)`, `answers(id, question, answer, mode)`, `library(...)`, `warning_events(category, action, mode, at — no PHI)`.
      Verify: `tests/test_db.py` creates temp DB, all tables exist.
- [ ] S5 Gitignore runtime data: `data/pauli.db`, `data/topics/`.
      Verify: `git status --porcelain` clean after a test ingest run.

## Phase P0 — Cache + search (concept §2)

- [ ] P0.1 `pauli/ingest/validate.py`: 1–5 terms; reject empty / single-letter / >50k hits; return narrow-down hint. Pure function, takes hit-count callback — no HTTP inside.
      Verify: `tests/test_validate.py` covers 0 terms, 6 terms, empty, 1-char, broad-term hint.
- [ ] P0.2 `pauli/ingest/europepmc.py`: `search(OPEN_ACCESS:Y AND TITLE_ABS:"<term>")` via `httpx`, hit-count query, paged metadata fetch, OA fullText/abstract fetch. OA-only.
      Verify: `tests/test_europepmc.py` with mocked HTTP; asserts OA query string and paging.
- [ ] P0.3 `pauli/ingest/topics.py`: `topic_hash` (stable hash of normalized terms) + `last_sync` CRUD on `topics` table.
      Verify: same terms → same hash; `last_sync` round-trips.
- [ ] P0.4 `pauli/ingest/pipeline.py`: fetch → store raw to `data/topics/<hash>/raw/` → normalized rows in `papers`. Used for initial ~500-paper fetch.
      Verify: mocked fetch of 3 papers writes 3 raw files + 3 DB rows; rerun is idempotent on PMCID.
- [ ] P0.5 `pauli/index/chunk.py`: chunk abstracts/sections ~512 tokens / 50 overlap. Deterministic, no network.
      Verify: `tests/test_chunk.py` asserts chunk size/overlap and PMCID linkage.
- [ ] P0.6 `pauli/index/embed.py`: `embed(texts)` interface; default `ollama/nomic-embed-text` via `ollama-python`, alternative `sentence-transformers/all-MiniLM-L6-v2`. No other backends.
      Verify: mocked Ollama returns fixed dim vectors; interface swappable via config.
- [ ] P0.7 `pauli/index/store.py`: insert vectors + metadata (`topic_hash` filter), `search_vectors(topic_hash, vec, top_k)`.
      Verify: insert 5 chunks, filtered search returns only matching `topic_hash`.
- [ ] P0.8 `pauli/ingest/sync.py`: `Check for new papers` query `FIRST_PDATE:[last_sync TO NOW]`, dedup by PMCID, append-only, re-embed new chunks, update `last_sync`, return count.
      Verify: `tests/test_sync_dedup.py` — second sync with same PMCIDs adds 0 rows; 1 new PMCID adds 1 paper + N chunks.
- [ ] P0-gate Manual: fetch ~500 papers for a real user topic; confirm cache hit and Europe PMC links resolve.
      Verify: manual run + `pytest` all green.

## Phase P1 — RAG chat + anti-hallucination (concept §3–§4)

- [ ] P1.1 `pauli/questionanswering/retrieve.py`: query rewrite + `store.search_vectors` top-k + score threshold filter.
      Verify: below-threshold → empty list (triggers abstain); above-threshold returns chunks.
- [ ] P1.2 `pauli/questionanswering/generate.py`: Ollama-local generate from chunks only; chunks-only system prompt; no general knowledge.
      Verify: mocked Ollama; prompt contains all chunks and forbids external knowledge.
- [ ] P1.3 `pauli/questionanswering/citations.py`: every factual sentence ends with `[PMCID]`; each cited PMCID ∈ retrieval set; else fail closed.
      Verify: `tests/test_citations.py` — presence test + validity test (invented PMCID rejected).
- [ ] P1.4 `pauli/questionanswering/abstain.py`: unknown template `I don't know from your saved papers — [...]`; distinguish no-papers / no-answer / conflicting-papers.
      Verify: `tests/test_abstain.py` covers all 3 branches; never guesses.
- [ ] P1.5 `pauli/questionanswering/language.py`: `Standard` (grade 8–10) / `Simple` (grade 5–6, <15-word sentences, acronyms expanded, `What this means:` line); same chunks+citations; simplification adds no facts. Default Simple for first answer.
      Verify: `tests/test_language.py` readability scores per mode + citation preservation.
- [ ] P1.6 `pauli/questionanswering/service.py`: orchestrate rewrite → retrieve → generate → citation-check → abstain → render.
      Verify: end-to-end with mocked embed+Ollama: happy path returns cited answer; empty retrieval returns unknown template.
- [ ] P1.7 `pauli/web/app.py` + `routes_topics.py` + `routes_chat.py`: minimal HTMX chat UI, mode toggle, onboarding buzzword form.
      Verify: manual — `What triggers PEM?` → <150 words, 3+ Europe PMC links, or explicit unknown.
- [ ] P1-gate: `pytest` green; zero invented citations on abstention tests.

## Phase P2 — Trigger warnings (concept §5)

- [ ] P2.1 `pauli/safety/detector.py`: keyword (+ later classifier) scan of retrieved chunks + draft answer; 6 categories: prognosis/mortality, suicidality, severe disability, pregnancy/children, medical trauma, PEM crash risk.
      Verify: `tests/test_warnings.py` one positive + one negative per category.
- [ ] P2.2 `pauli/safety/gate.py` + `resources.py`: blurred card `This answer contains [category] — Show / Skip / Why am I seeing this?`, click-to-reveal only; gentler Simple-mode wording; always `Research info only, not medical advice` + crisis resources where relevant; sensitivity `low / standard / hide details` stored locally.
      Verify: gate fires in both language modes (test parametrize mode).
- [ ] P2.3 `pauli/safety/events.py`: log shown/skipped (no PHI).
      Verify: event rows contain category+action only, no query text.
- [ ] P2.4 Wire gate into `service.py` + chat template before rendering details.
      Verify: manual prognosis-type query shows gate before details in both modes.
- [ ] P2-gate: `pytest tests/test_warnings.py` green; gate precedes content in both modes.

## Phase P3 — Tracker + doctor printout (concept §6)

- [ ] P3.1 `pauli/tracker/library.py`: save answers/papers (relations to PMCID + answer id).
      Verify: save + list round-trip; unsave works.
- [ ] P3.2 `pauli/tracker/digest.py`: weekly manual digest in plain language over new papers since `last_sync`.
      Verify: digest lists only papers newer than `last_sync` (e.g. `3 new papers since 2026-09-30`).
- [ ] P3.3 `pauli/tracker/export.py`: 1-page Markdown (+ PDF if trivial via existing dep, else Markdown only) with question, short answer, citations, unknowns, suggested doctor questions.
      Verify: `tests/test_export.py` asserts all 5 sections present, fits 1 page (~500 words max).
- [ ] P3.4 `pauli/web/routes_sync.py` + `routes_library.py`: `Check for new papers` button, follow topic, library, export download.
      Verify: manual — sync shows new count, export downloads.
- [ ] P3-gate: full `poetry run pytest` green; manual doctor-export review.

## Explicit non-goals (do not build in MVP)

Hand-rolled RAG only (no LangChain/LlamaIndex/Haystack); no auto-cron; no diagnosis/treatment logic; no bulk non-OA scraping; no framework-side citation defaults — gate + abstention in our code.
