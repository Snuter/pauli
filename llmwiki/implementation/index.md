# Implementation

Task ledger convention (autonomous agent): each bullet is `ID -> owner file(s) -> Verify: exact pytest command -> Forbidden: negative check`. Build in order S -> P0 -> P1 -> P2 -> P3. Canonical contracts: `pauli/config.py` (CONFIG_PATH=`data/config.json`), `pauli/db.py:SCHEMA_SQL`, `llmwiki/architecture/web-api.md` (fragments frozen from `ui-mockup/` IDs verbatim).

* [Phase S](phase-S.md) - Skeleton, config constants, DB tables, gitignore (S1-S5).
* [Phase P0](phase-P0.md) - Validate, fetch, topics, pipeline, chunk, embed, store, sync.
* [Phase P1](phase-P1.md) - Retrieve, generate, citations, abstain, language, service, web UI.
* [Phase P2](phase-P2.md) - Detector, gate, events, wiring.
* [Phase P3](phase-P3.md) - Scheduled checks, email digest, export, settings mail routes.
* [Non-Goals](non-goals.md) - MVP exclusions: no frameworks/diagnosis/non-OA/shipped keys.
