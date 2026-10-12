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

Scheduled in-app checks for new papers (`tracker/sync_cron.py`: re-extract terms from stored past questions of subscribed sessions via `extract.py`, same ID-first lookup `pageSize=100`/`HIT_LIMIT=50000`, PMCID-filter against `papers(pmcid)`, download+digest missing only; global `sync_state(last_run)` for status; decided 2026-10-12, no query log, no `FIRST_PDATE` window); cadence is a Settings choice, once a week by default. Sessions auto-persist: every Ask writes `sessions (id, title, created_at, subscribed)` + `session_answers (session_id, question, answer_id)` — no manual save, no save/list/unsave API, single-user no auth. Session lists use `ORDER BY created_at DESC` (newest first); any session data change (ask, question edit/move/delete, rename, subscription toggle) refreshes `created_at` so the active session moves to the top. Each session has a Subscribe toggle (Ask menu button, `aria-pressed`); only subscribed sessions are covered by mail. Notify (`tracker/notify.py`) re-runs each subscribed session's past questions with the current strictness/`TOP_K=15`; a session is affected when new papers land in its top-K. Mail is sent only when at least one subscribed session is affected: one combined email via local no-auth/TLS SMTP only for MVP (decided 2026-10-12; recipient + sender/SMTP from Settings config file, stored locally) with one section per affected session: digest line + regenerated LLM output in doctor-printout shape; new-papers-only MVP (no deleted/updated marks). SMTP failure is reported loudly in Settings status and retried at the next run. Renaming a session updates only its `title` (same session id, history and subscription preserved). Deleting a session removes the session entirely (plus its history and subscription). Export: single-LLM-summary 1-page dialog per session in Ask (print to PDF, decided 2026-10-12): session title + one condensed summary across ALL Q&As (short answer, citations, unknowns, suggested doctor questions; `test_export.py` 5 sections, ~500 words max for the summary).[^tech-concept]

User view: [tracking](/workflows/tracking-doctor-visit.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
