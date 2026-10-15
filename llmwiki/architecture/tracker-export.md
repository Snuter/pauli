---
type: Architecture
title: Tracker + doctor export
description: Scheduled new-paper checks, per-session email digest, auto-persisted sessions, per-session condensed 1-page print HTML.
tags: [pauli, tracker]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# Tracker + export

Scheduled in-app checks for new papers (`tracker/sync_cron.py`: re-extract terms from stored past questions of subscribed sessions via `extract.py`, same ID-first lookup `pageSize=100`/`HIT_LIMIT=50000`, PMCID-filter against `papers(pmcid)`, download+digest missing only; global `sync_state(last_run)` for status; decided 2026-10-12, no query log, no `FIRST_PDATE` date-window filter — sorting by `FIRST_PDATE_D` still required); cadence is a Settings choice from `daily|weekly|monthly` in `data/config.json` (`mail_freq`, default `weekly`). Wiring (decided 2026-10-15): `web/app.py` lifespan starts `APScheduler`; `sync_cron.run_once()` builds `chat_fn` from `Settings` + `ollama_api_key()` at run time, holds an in-memory overlapping-run lock, updates `sync_state(last_run)`; `POST /tracker/run` calls the same `run_once()` and returns `{run_at,new_pmcids,affected}`.

Sessions auto-persist: every Ask writes `sessions (id uuid4-hex, title UNIQUE, created_at unix seconds, subscribed)` + `session_answers (session_id, question snapshot, answer_id, position 0-based contiguous)` — no manual save, no save/list/unsave API, single-user no auth. Canonical DDL lives in `pauli/db.py:SCHEMA_SQL`. Session lists use `ORDER BY created_at DESC` (newest first); any session data change (ask, question edit/move/delete, rename, subscription toggle) refreshes `created_at` (unix seconds; mockup `Date.now()` ms converts via `ms // 1000`) so the active session moves to the top. Move = swap the two rows' `position` then renumber `0..n-1` in one transaction. Each session has a Subscribe toggle (Ask menu button, `aria-pressed`); only subscribed sessions are covered by mail. Tests: FastAPI `TestClient` for API asserts; playwright only vs static `ui-mockup/` + tmp-DB fixture (frozen 2026-10-15 per user Q&A).

Notify (`tracker/notify.py`) re-runs each subscribed session's past questions with the current strictness/`TOP_K=15`; a session is **affected** when re-retrieval top-K contains >=1 PMCID absent from `papers` at last run (newly synced papers surface in top-K under current strictness). Mail is sent only when >=1 subscribed session is affected: one combined multipart email (`text/plain` + `text/html` mirroring the doctor-printout sections) via local no-auth SMTP, no TLS/STARTTLS in MVP (frozen 2026-10-15; recipient/sender/SMTP `host:port` explicit-port-required via `config.is_valid_smtp`/`validate_mail_form` from `data/config.json`; bare host without port is a 422 validation error) with subject `PAULI digest <date ISO YYYY-MM-DD>: <N> session(s) with new papers`, one section per affected session (session title + digest line + regenerated LLM output in doctor-printout shape with the frozen 5 headings); new-papers-only MVP (no deleted/updated marks). Minimal skeleton per section — text part: `{title}\n{digest line}\n{short answer}\nCitations: {PMC ids}\nUnknowns: {...}\nAsk your doctor: {...}`; HTML part mirrors it with `<h2>{title}</h2><p>{digest line}</p><p>{short answer}</p><p>Citations: {links}</p><p>Unknowns: ...</p><p>Ask your doctor: ...</p>`. SMTP failure is reported loudly in `#mail-status` in Settings and retried at the next run (no backoff in MVP).

Renaming a session updates only its `title` (same session id, history and subscription preserved). Deleting a session removes the session entirely (plus its history and subscription).

Export (`tracker/export.py`): single-LLM-summary 1-page dialog per session in Ask (`GET /sessions/{id}/doctor` -> `#doctor-dialog`, Print via `window.print()`): session title + one condensed summary across ALL Q&As with exactly these 5 headings in order (frozen 2026-10-15 per user Q&A, mirrors `prompts.py:DOCTOR_SUMMARY_PROMPT`) — 1. Short answer, 2. Citations (`[PMCID]` in retrieval set), 3. Unknowns, 4. Ask your doctor, 5. Digest line; whole summary ~500 words max by whitespace-split count (truncate prose with ellipsis, never drop citations). Answer HTML via `web/sanitize.py:escape_and_linkify`. Verify `tests/test_export.py` asserts 5 headings in order + word cap + TDD (agent writes test first).

User view: [tracking](/workflows/tracking-doctor-visit.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
