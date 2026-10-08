# P.A.U.L.I. — Implementation Plan

Source: `docs/concept-technical.md` + `docs/concept-user-journey.md`.
Stack: Python >=3.13, Poetry, pytest, FastAPI + Jinja + HTMX only, SQLite + sqlite-vec, user-configured Ollama (local or cloud).
Constraints: no built-in default topics in code or DB; OA subset only; weekly manual sync, no cron; single-user local, no auth; fetch all matches (no 500-paper cap) with paged ingest + progress + idempotent resume; missing chat model / cloud key is a hard misconfiguration error.
`setup_dev_ai.sh` is dev-only (opencode agent tooling, incl. the `ollama launch opencode` harness) and is not a runtime dependency; the app talks directly to user-configured Ollama via `ollama-python`, never via opencode; no shipped default model or key.

Conventions used below: each step is one unit of work. `Verify:` is the done-criteria. Run `poetry run pytest tests/<file>` after each code step.

## Phase S — Skeleton + config + DB (prereq for all P0–P3)

- [ ] S1 Add runtime deps to `pyproject.toml`: `fastapi`, `uvicorn`, `httpx`, `sqlite-vec`, `ollama-python`, `jinja2`, `textstat`. Keep `sentence-transformers` optional (offline embed alternative only).
      Verify: `poetry install` succeeds, `poetry run pytest` collects (0 tests OK).
- [ ] S2 Create package skeleton with `__init__.py` per dir: `pauli/ingest/`, `pauli/index/`, `pauli/questionanswering/`, `pauli/safety/`, `pauli/tracker/`, `pauli/web/`, `tests/`. No logic yet.
      Verify: `poetry run python -c "import pauli"` succeeds.
- [ ] S3 Add `pauli/config.py`: paths (`data/pauli.db`, `data/topics/<hash>/raw/`), `CHUNK_TOKENS=512`, `CHUNK_OVERLAP=50`, `TOP_K=15`, `SCORE_THRESHOLD=0.3` plus user-calibration `strictness 0–100` → threshold `0.0–0.6` (`TOP_K` fixed), `HIT_LIMIT=50000`, `OPEN_ACCESS:Y` filter with OR-union `(TITLE_ABS:"<t1>" OR TITLE_ABS:"<t2>" ...)`; Ollama via `OLLAMA_HOST` (default `http://localhost:11434`), `OLLAMA_CHAT_MODEL` + `OLLAMA_EMBED_MODEL` (default `nomic-embed-text`), `OLLAMA_API_KEY` (only for the cloud endpoint, never committed). No reference to `setup_dev_ai.sh` / `MODEL` here — that script and its `ollama launch opencode` harness are dev-only.
      Verify: unit test asserts constants importable; no topic strings hardcoded; missing chat model (or missing cloud key for a cloud host) raises a clear misconfiguration error.
- [ ] S4 Add `pauli/db.py`: init + migrate SQLite + sqlite-vec tables `topics(hash, terms_json, last_sync)`, `papers(pmcid PK, topic_hash, title, year, authors, url, abstract)`, `chunks(id, pmcid, topic_hash, idx, text, vec)`, `answers(id, question, answer, mode)`, `library(...)`, `warning_events(category, action, mode, at — no PHI)`.
      Verify: `tests/test_db.py` creates temp DB, all tables exist.
- [ ] S5 Gitignore runtime data: `data/pauli.db`, `data/topics/`.
      Verify: `git status --porcelain` clean after a test ingest run.

## Phase P0 — Cache + search (concept §2)

- [ ] P0.1 `pauli/ingest/validate.py`: 1–5 terms; reject empty / single-letter / >50k hits; return narrow-down hint. Pure function, takes hit-count callback — no HTTP inside.
      Verify: `tests/test_validate.py` covers 0 terms, 6 terms, empty, 1-char, broad-term hint.
- [ ] P0.2 `pauli/ingest/europepmc.py`: `search(OPEN_ACCESS:Y AND (TITLE_ABS:"<t1>" OR TITLE_ABS:"<t2>" ...))` via `httpx`, per-term hit-count query, paged metadata fetch of all matches (no 500-paper cap) with progress, OA fullText/abstract fetch. OA-only.
      Verify: `tests/test_europepmc.py` with mocked HTTP; asserts OA query string and paging.
- [ ] P0.3 `pauli/ingest/topics.py`: `topic_hash` (stable hash of normalized terms) + `last_sync` CRUD on `topics` table.
      Verify: same terms → same hash; `last_sync` round-trips.
- [ ] P0.4 `pauli/ingest/pipeline.py`: fetch → store raw to `data/topics/<hash>/raw/` → normalized rows in `papers`. Used for initial fetch of all matches (paged, progress UI, idempotent resume on PMCID).
      Verify: mocked fetch of 3 papers writes 3 raw files + 3 DB rows; rerun is idempotent on PMCID.
- [ ] P0.5 `pauli/index/chunk.py`: chunk abstracts/sections ~512 tokens / 50 overlap. Deterministic, no network.
      Verify: `tests/test_chunk.py` asserts chunk size/overlap and PMCID linkage.
- [ ] P0.6 `pauli/index/embed.py`: `embed(texts)` interface; default Ollama `OLLAMA_EMBED_MODEL` (`nomic-embed-text`) via `ollama-python` against `OLLAMA_HOST`, alternative `sentence-transformers/all-MiniLM-L6-v2`. No other backends.
      Verify: mocked Ollama returns fixed dim vectors; interface swappable via config.
- [ ] P0.7 `pauli/index/store.py`: insert vectors + metadata (`topic_hash` filter), `search_vectors(topic_hash, vec, top_k)`.
      Verify: insert 5 chunks, filtered search returns only matching `topic_hash`.
- [ ] P0.8 `pauli/ingest/sync.py`: `Check for new papers` query `FIRST_PDATE:[last_sync TO NOW]`, dedup by PMCID, append-only, re-embed new chunks, update `last_sync`, return count.
      Verify: `tests/test_sync_dedup.py` — second sync with same PMCIDs adds 0 rows; 1 new PMCID adds 1 paper + N chunks.
- [ ] P0-gate Manual: fetch all matching papers for a real user topic; confirm cache hit and Europe PMC links resolve.
      Verify: manual run + `pytest` all green.

## Phase P1 — RAG chat + anti-hallucination (concept §3–§4)

- [ ] P1.1 `pauli/questionanswering/retrieve.py`: query rewrite + `store.search_vectors` top-k (`TOP_K=15`) + score threshold filter (default `0.3`, user-calibration `strictness 0–100` → `0.0–0.6`).
      Verify: below-threshold → empty list (triggers abstain); above-threshold returns chunks; slider mapping unit-tested.
- [ ] P1.2 `pauli/questionanswering/generate.py`: generate from chunks only via user-configured Ollama (`ollama-python` against `OLLAMA_HOST` with `OLLAMA_CHAT_MODEL`; `OLLAMA_API_KEY` only for cloud); never via opencode; chunks-only system prompt; no general knowledge; fail closed on misconfiguration.
      Verify: mocked Ollama; prompt contains all chunks and forbids external knowledge; no key in logs.
- [ ] P1.3 `pauli/questionanswering/citations.py`: every factual sentence ends with `[PMCID]`; each cited PMCID ∈ retrieval set; else fail closed.
      Verify: `tests/test_citations.py` — presence test + validity test (invented PMCID rejected).
- [ ] P1.4 `pauli/questionanswering/abstain.py`: unknown template `I don't know from your saved papers — [...]`; distinguish no-papers / no-answer / conflicting-papers (conflicting = present both cited sides + unknown note, no automatic contradiction detection).
      Verify: `tests/test_abstain.py` covers all 3 branches; never guesses.
- [ ] P1.5 `pauli/questionanswering/language.py`: `Standard` (grade 8–10) / `Simple` (grade 5–6, <15-word sentences, acronyms expanded, `What this means:` line) plus `simplicity` slider for Simple-mode intensity; same chunks+citations; simplification adds no facts. Default Simple for first answer.
      Verify: `tests/test_language.py` `textstat` Flesch-Kincaid scores per mode + citation preservation.
- [ ] P1.6 `pauli/questionanswering/service.py`: orchestrate rewrite → retrieve → generate → citation-check → abstain → render.
      Verify: end-to-end with mocked embed+Ollama: happy path returns cited answer; empty retrieval returns unknown template; misconfigured Ollama (missing model/key) returns misconfiguration error.
- [ ] P1.7 `pauli/web/app.py` + `routes_topics.py` + `routes_chat.py`: minimal FastAPI + Jinja + HTMX chat UI (no Streamlit), mode toggle + simplicity slider + strictness slider, onboarding buzzword form.
      Verify: manual — `What triggers PEM?` → <150 words, 3+ Europe PMC links, or explicit unknown.
- [ ] P1-gate: `pytest` green; zero invented citations on abstention tests.

## Phase P2 — Trigger warnings (concept §5)

- [ ] P2.1 `pauli/safety/detector.py`: keyword (+ later classifier) scan of retrieved chunks + draft answer; 6 categories: prognosis/mortality, suicidality, severe disability, pregnancy/children, medical trauma, PEM crash risk.
      Verify: `tests/test_warnings.py` one positive + one negative per category.
- [ ] P2.2 `pauli/safety/gate.py` + `resources.py`: blurred card `This answer contains [category] — Show / Skip / Why am I seeing this?`, click-to-reveal only; gentler Simple-mode wording; always `Research info only, not medical advice` + crisis resources where relevant; sensitivity `low` = gate only suicidality/self-harm, `standard` = gate all 6, `hide details` = title-only + double-confirm, stored locally (single-user).
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
- [ ] P3.3 `pauli/tracker/export.py`: 1-page browser print-view HTML (print to PDF via browser, print CSS) with question, short answer, citations, unknowns, suggested doctor questions.
      Verify: `tests/test_export.py` asserts all 5 sections present, fits 1 page (~500 words max).
- [ ] P3.4 `pauli/web/routes_sync.py` + `routes_library.py`: `Check for new papers` button, follow topic, library, print-view export page.
      Verify: manual — sync shows new count, export downloads.
- [ ] P3-gate: full `poetry run pytest` green; manual doctor-export review.

## Explicit non-goals (do not build in MVP)

Hand-rolled RAG only (no LangChain/LlamaIndex/Haystack); no auto-cron; no diagnosis/treatment logic; no bulk non-OA scraping; no framework-side citation defaults — gate + abstention in our code; no opencode harness at runtime (`setup_dev_ai.sh` + `ollama launch opencode` stay dev-only); no shipped/committed model or API key.
