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
- Sync: weekly manual sync, no auto-cron in MVP.
- Compliance: only OA subset per Europe PMC terms. No bulk scraping of non-OA.

## 2. Data pipeline

1. Onboarding input: 1–5 buzzwords. No defaults in code or DB.
2. Validate: for each term, query Europe PMC REST API for
   `OPEN_ACCESS:Y AND TITLE_ABS:"<term>"`, check hit count.
   Reject empty / single-letter / too-broad (>50k hits) with a narrow-down hint.
3. Ingest: fetch metadata + OA full text / abstract, store raw in
   `data/topics/<topic-hash>/raw/`, normalized rows in SQLite `data/pauli.db`.
4. Index: chunk abstracts/sections, embed locally (e.g. sentence-transformers),
   store vectors in sqlite-vec / faiss / chroma with PMCID, title, year, authors,
   Europe PMC URL.
5. Sync: per-topic `last_sync` timestamp. `Check for new papers` button queries
   `FIRST_PDATE:[last_sync TO NOW]`. Dedup by PMCID, append-only, re-embed new
   chunks. UI shows `3 new papers since 2026-09-30`.

## 3. Chat Q&A + anti-hallucination

Pipeline: rewrite query -> retrieve top-k chunks above score threshold ->
generate from chunks only -> post-check citations -> render.

Built-in guidelines:
- System prompt: only use retrieved chunks. No general knowledge.
- Every sentence containing a fact must end with `[PMCID]` linking to Europe PMC.
- Citations must exist in the retrieval set; otherwise fail closed.
- If retrieval score is below threshold or no chunks support an answer, return
  the unknown template, never guess.
- Unknown template: `I don't know from your saved papers — [what is missing,
  what term to add, what to ask your doctor]`.
- Distinguish: no papers cached vs papers cached but no answer vs conflicting papers.
- Tests: citation-presence test, citation-validity test, abstention test.

## 4. Language modes (implementation)

Toggle: `Standard / Simple`. Same chunks and citations, different wording.

- Standard: grade 8–10, keeps term + short definition,
  e.g. `post-exertional malaise (crash after effort)`.
- Simple: grade 5–6, sentences <15 words, expand all acronyms, use glossary
  (`PEM -> crash after effort`), add `What this means:` line.
- Simplification must not add facts. Citation check applies to both modes.
- Default: Simple for first answer to reduce cognitive load.
- Verify with readability scores per mode.

## 5. Trigger warnings (implementation)

Categories: prognosis/mortality, suicidality, severe disability,
pregnancy/children, medical trauma, PEM crash risk.

- Detector: keyword + classifier on retrieved chunks and draft answer.
- UI: blurred card `This answer contains [category] — Show / Skip / Why am I
  seeing this?` Click-to-reveal only. Simple mode uses gentler wording.
- Always show: `Research info only, not medical advice` + local crisis resources
  where relevant.
- Sensitivity profile stored locally: `low / standard / hide details`.
- Log warnings shown/skipped (no PHI) for evaluation.
- Tests per category; gate must fire in both language modes.

## 6. Tracker + doctor printout (implementation)

- Follow topics, weekly manual digest in plain language.
- Personal library: save answers/papers (SQLite relations to PMCID + answer id).
- Export: 1-page Markdown/PDF with question, short answer, citations, unknowns,
  suggested questions for doctor.

## 7. Tech stack & layout

- Backend: FastAPI, SQLite + sqlite-vec, local embeddings.
- Frontend: minimal server-rendered UI (HTMX) or Streamlit for MVP.
- LLM: Ollama-local via `run_opencode.sh` (`MODEL` var) to avoid sending health
  queries externally.
- Layout: `pauli/ingest/`, `pauli/index/`, `pauli/qa/`, `pauli/safety/`,
  `pauli/web/`, `data/`, `tests/`.

## 8. MVP phases & verification

1. P0 cache + search: fetch ~500 papers for a user topic, verify cache hit and
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
