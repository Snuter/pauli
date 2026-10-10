# LLMWIKI Update Log

## 2026-10-10
* **Update**: Adopted python-playwright (+ pytest-playwright, Chromium) as UI testing framework — new `architecture/testing.md` strategy page (pytest vs playwright layers, `tests/` + `tests/ui/` layout, commands, locator/gate conventions, phase mapping); wired into tech-stack, implementation index (S/P1/P2), plan summary. `tests/ui/test_mockup_smoke.py` green (3 passed).
* **Verification**: Full `docs/` ingest audit for deletion — all load-bearing strings present in wiki; fixed stale root `index.md` pending wording, wrong companion link in `concept-user-journey-summary.md`, restored full DB column list + paths in `phase-S.md`, pure-function callback nuance in `phase-P0.md`, full §9 success criteria + MVP gates in `concept-technical-summary.md`; noted `docs/`-deletable state in `schema.md`. `docs/` safe to delete.
* **Update**: Ingested `docs/implementation-plan.md` — populated `sources/implementation-plan-summary.md`, `implementation/` (S, P0-P3, non-goals); refreshed indexes. All three `docs/` sources now ingested.
* **Update**: Ingested `docs/concept-technical.md` — populated `sources/concept-technical-summary.md`, `architecture/` (6 pages), extended `overview/glossary.md`; refreshed indexes.
* **Update**: Ingested `docs/concept-user-journey.md` — populated `sources/concept-user-journey-summary.md`, `overview/` (vision, principles, glossary), `workflows/` (5 journeys); refreshed section indexes.
* **Creation**: Established `llmwiki/` OKF v0.2 bundle structure (index, schema, section indexes, draft stubs). No docs ingest yet — awaiting user command.
