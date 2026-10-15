# Implementation

Task ledger convention (autonomous agent, frozen 2026-10-15 per user Q&A): each bullet is `ID -> owner file(s) -> TDD (agent writes the named test first) -> Verify: exact pytest command -> Forbidden: negative check`. Build in order S -> P0 -> P1 -> P2 -> P3. Canonical contracts: `pauli/config.py` (`CONFIG_PATH=data/config.json`, `validate_ollama_form/validate_mail_form`, `validation_error_fragment`, `chat_fn(prompt)->str`), `pauli/db.py:SCHEMA_SQL` (uuid4-hex id, unix-seconds `created_at`, mode CHECK, 0-based `position`), `pauli/safety/resources.py` (frozen gate copy), `pauli/web/sanitize.py` (`escape_and_linkify`), `llmwiki/architecture/web-api.md` (fragments + JS poller frozen from `ui-mockup/` IDs verbatim). API tests use FastAPI `TestClient`; playwright only vs static mockup + tmp DB.

* [Phase S](phase-S.md) - Skeleton, config constants, DB tables, gitignore (S1-S5).
* [Phase P0](phase-P0.md) - Validate, fetch, topics, pipeline, chunk, embed, store, sync.
* [Phase P1](phase-P1.md) - Retrieve, generate, citations, abstain, language, service, web UI.
* [Phase P2](phase-P2.md) - Detector, gate, events, wiring.
* [Phase P3](phase-P3.md) - Scheduled checks, email digest, export, settings mail routes.
* [Non-Goals](non-goals.md) - MVP exclusions: no frameworks/diagnosis/non-OA/shipped keys.
