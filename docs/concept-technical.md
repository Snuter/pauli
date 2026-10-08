# P.A.U.L.I. — Technical Concept
Patient-centered AI for Understanding Literature and Insights

See also: `concept-user-journey.md` for user flows.
Source: Europe PMC Open Access subset (https://europepmc.org/downloads/openaccess).

## 1. Scope & constraints

- Data: cached Europe PMC Open Access subset, keyed by patient-provided
  buzzwords. No built-in defaults in code or DB.
- Interaction: Chat Q&A over cached papers.
- Safety: gated warning cards (blur + reveal).
- MVP shape: local web app + RAG (Python >=3.13, Poetry, pytest).
  Single-user local, no auth. Frontend is FastAPI + Jinja + HTMX only.
- Sync: weekly manual sync, no auto-cron in MVP.
- Compliance: only OA subset per Europe PMC terms. No bulk scraping of non-OA.

## 2. Data pipeline

1. Onboarding input: 1–5 buzzwords. No defaults in code or DB.
   Combined with OR-union: `OPEN_ACCESS:Y AND (TITLE_ABS:"<t1>" OR TITLE_ABS:"<t2>" ...)`.
2. Validate: for each term, query Europe PMC REST API for
   `OPEN_ACCESS:Y AND TITLE_ABS:"<term>"`, check hit count.
   Reject empty / single-letter / too-broad (>50k hits) with a narrow-down hint.
3. Ingest: fetch all matching papers (no 500-paper cap), paged
   metadata + OA full text / abstract fetch with progress UI and idempotent
   resume on PMCID, store raw in
   `data/topics/<topic-hash>/raw/`, normalized rows in SQLite `data/pauli.db`.
4. Index: chunk abstracts/sections (~512 tokens, 50 overlap), embed via
   user-configured Ollama (`pauli/index/embed.py`, `OLLAMA_EMBED_MODEL`
   default `nomic-embed-text`; `sentence-transformers/all-MiniLM-L6-v2`
   as offline alternative), store vectors in sqlite-vec alongside metadata with PMCID, title,
   year, authors, Europe PMC URL, `topic_hash`.
5. Sync: per-topic `last_sync` timestamp. `Check for new papers` button queries
   `FIRST_PDATE:[last_sync TO NOW]`. Dedup by PMCID, append-only, re-embed new
   chunks. UI shows `3 new papers since 2026-09-30`.

## 3. Chat Q&A + anti-hallucination

Pipeline: rewrite query (`pauli/questionanswering/retrieve.py`) -> retrieve top-k chunks above
score threshold (`pauli/questionanswering/retrieve.py` + `pauli/index/store.py`,
defaults `TOP_K=15`, `SCORE_THRESHOLD=0.3`, plus a user-calibration
`strictness 0–100` slider mapping to threshold `0.0–0.6`, `TOP_K` fixed) ->
generate from chunks only via user-configured Ollama
(`pauli/questionanswering/generate.py` via `ollama-python` against
`OLLAMA_HOST` with `OLLAMA_CHAT_MODEL`; `OLLAMA_API_KEY` only for the cloud
endpoint; never via the `ollama launch opencode` dev harness) ->
post-check citations in code (`pauli/questionanswering/citations.py`, `pauli/questionanswering/abstain.py`) -> render.
Missing chat model (or missing cloud key for a cloud host) is a hard
misconfiguration error with a setup hint; the app reports it instead of answering.

Built-in guidelines:
- System prompt: only use retrieved chunks. No general knowledge.
- Every sentence containing a fact must end with `[PMCID]` linking to Europe PMC.
- Citations must exist in the retrieval set; otherwise fail closed.
- If retrieval score is below threshold or no chunks support an answer, return
  the unknown template, never guess.
- Unknown template: `I don't know from your saved papers — [what is missing,
  what term to add, what to ask your doctor]`.
- Distinguish: no papers cached vs papers cached but no answer vs conflicting papers.
  Conflicting papers: no automatic contradiction detection in MVP; present both
  cited sides plus an unknown note.
- Tests: citation-presence test, citation-validity test, abstention test.

## 4. Language modes (implementation)

Toggle: `Standard / Simple` plus a `simplicity` slider for Simple-mode intensity
(sentence length 10–15, glossary on/off). Same chunks and citations, different wording.

- Standard: grade 8–10, keeps term + short definition,
  e.g. `post-exertional malaise (crash after effort)`.
- Simple: grade 5–6, sentences <15 words, expand all acronyms, use glossary
  (`PEM -> crash after effort`), add `What this means:` line.
- Simplification must not add facts. Citation check applies to both modes.
- Default: Simple for first answer to reduce cognitive load.
- Verify with `textstat` Flesch-Kincaid readability scores per mode.

## 5. Trigger warnings (implementation)

Categories: prognosis/mortality, suicidality, severe disability,
pregnancy/children, medical trauma, PEM crash risk.

- Detector: keyword + classifier on retrieved chunks and draft answer.
- UI: blurred card `This answer contains [category] — Show / Skip / Why am I
  seeing this?` Click-to-reveal only. Simple mode uses gentler wording.
- Always show: `Research info only, not medical advice` + local crisis resources
  where relevant.
- Sensitivity profile stored locally (single-user, no auth): `low` = gate only
  suicidality/self-harm, `standard` = gate all 6 categories,
  `hide details` = title-only gate requiring double-confirm to reveal.
- Log warnings shown/skipped (no PHI) for evaluation.
- Tests per category; gate must fire in both language modes.

## 6. Tracker + doctor printout (implementation)

- Follow topics, weekly manual digest in plain language.
- Personal library: save answers/papers (SQLite relations to PMCID + answer id).
  Single-user local, no auth; no retention/delete button in MVP.
- Export: 1-page browser print-view HTML (user prints to PDF) with question,
  short answer, citations, unknowns, suggested questions for doctor.

## 7. Tech stack & layout

- Backend: FastAPI, SQLite + sqlite-vec, Ollama embeddings.
- RAG: Option A hand-rolled minimal (no LangChain/LlamaIndex/Haystack in MVP).
  Embeddings behind `pauli/index/embed.py` (user-configured Ollama
  `OLLAMA_EMBED_MODEL` default `nomic-embed-text`,
  `sentence-transformers/all-MiniLM-L6-v2` as offline alternative). Vectors in `sqlite-vec`
  in `data/pauli.db` with `topic_hash` filter for per-topic isolation and
  append-only sync. Generation via `ollama-python` against user-configured
  Ollama (`OLLAMA_HOST` + `OLLAMA_CHAT_MODEL`), never via opencode.
  Citation gate + abstention enforced in code, not framework defaults.
  Revisit LlamaIndex only if hybrid search/reranking proves necessary.
- Frontend: minimal server-rendered UI with FastAPI + Jinja + HTMX only.
- LLM: user-configured Ollama, local or cloud. `OLLAMA_HOST` (default
  `http://localhost:11434`; cloud endpoint for cloud models),
  `OLLAMA_CHAT_MODEL` / `OLLAMA_EMBED_MODEL` (no shipped default chat model),
  `OLLAMA_API_KEY` required only for the cloud endpoint (empty for local;
  via env or gitignored `.env`, never logged or committed).
  The app fails closed on missing model / missing cloud key.
  `setup_dev_ai.sh` is dev-only (installs Ollama + opencode coding agent for
  working ON this project, including the `ollama launch opencode` harness)
  and is NOT used by the app at runtime. Local mode keeps health queries on
  the user's machine; cloud mode is covered by that provider's terms —
  retrieval/caching stays local.
- Layout: `pauli/ingest/`, `pauli/index/`, `pauli/questionanswering/`, `pauli/safety/`,
  `pauli/web/`, `data/`, `tests/`.

## 8. MVP phases & verification

1. P0 cache + search: fetch all matching papers for a user topic (OR-union,
   paged, progress + idempotent resume), verify cache hit and
   citation links. Verify: `pytest`.
2. P1 RAG chat: `What triggers PEM?` -> <150 words, grade-appropriate,
   3+ Europe PMC links, or explicit unknown.
3. P2 warnings: prognosis-type query shows gate before details. Tests per category.
4. P3 tracker + printout: follow topic, manual sync digest, doctor export.

## 9. Success criteria (technical)

- All factual sentences cited and resolvable to cached PMCID.
- Zero invented citations on abstention tests.
- Warning gate appears before gated content in both language modes.
- Sync adds only new PMCIDs, no duplicates.
- Readability scores meet mode targets.
