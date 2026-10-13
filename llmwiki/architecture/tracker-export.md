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

Scheduled in-app checks for new papers (`tracker/sync_cron.py`: re-extract terms from stored past questions of subscribed sessions via `extract.py`, same ID-first lookup `pageSize=100`/`HIT_LIMIT=50000`, PMCID-filter against `papers(pmcid)`, download+digest missing only; global `sync_state(last_run)` for status; decided 2026-10-12, no query log, no `FIRST_PDATE` window); cadence is a Settings choice from `daily|weekly|monthly` in `data/config.json` (`mail_freq`, default `weekly`).

Sessions auto-persist: every Ask writes `sessions (id, title, created_at, subscribed)` + `session_answers (session_id, question, answer_id, position)` — no manual save, no save/list/unsave API, single-user no auth. Canonical DDL lives in `pauli/db.py:SCHEMA_SQL`. Session lists use `ORDER BY created_at DESC` (newest first); any session data change (ask, question edit/move/delete, rename, subscription toggle) refreshes `created_at` so the active session moves to the top. Each session has a Subscribe toggle (Ask menu button, `aria-pressed`); only subscribed sessions are covered by mail.

Notify (`tracker/notify.py`) re-runs each subscribed session's past questions with the current strictness/`TOP_K=15`; a session is **affected** when re-retrieval top-K contains >=1 PMCID absent from `papers` at last run (newly synced papers surface in top-K under current strictness). Mail is sent only when >=1 subscribed session is affected: one combined email via local no-auth/TLS SMTP only for MVP (decided 2026-10-12; recipient/sender/SMTP/freq from `data/config.json`) with subject `PAULI digest <date>: <N> session(s) with new papers`, one section per affected session (session title + digest line + regenerated LLM output in doctor-printout shape); new-papers-only MVP (no deleted/updated marks). SMTP failure is reported loudly in `#mail-status` in Settings and retried at the next run (no backoff in MVP).

Renaming a session updates only its `title` (same session id, history and subscription preserved). Deleting a session removes the session entirely (plus its history and subscription).

Export (`tracker/export.py`): single-LLM-summary 1-page dialog per session in Ask (`GET /sessions/{id}/doctor` -> `#doctor-dialog`, Print via `window.print()`): session title + one condensed summary across ALL Q&As with exactly 5 parts — short answer, citations (`[PMCID]` in retrieval set), unknowns, suggested doctor questions, digest line; whole summary ~500 words max (truncate with ellipsis, never drop citations). Verify `tests/test_export.py` asserts 5 sections + word cap.

User view: [tracking](/workflows/tracking-doctor-visit.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
