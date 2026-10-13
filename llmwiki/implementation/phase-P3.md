---
type: Phase
title: Phase P3 — tracker + printout
description: Scheduled checks, email digest, export, settings mail routes (P3.1-P3.4).
tags: [pauli, phase-P3]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: impl-plan
    resource: /docs/implementation-plan.md
    title: P.A.U.L.I. Implementation Plan
---

# Phase P3

Implements [tracker](/architecture/tracker-export.md). Depends on P0.8 `sync.py` (P3.1 calls it; no duplicate re-extract logic) + P1.2 generator (reuse `GENERATE_SYSTEM`/`DOCTOR_SUMMARY_PROMPT`) + `data/config.json` (`mail_to/from/smtp/freq`, `APScheduler` in-app only). `affected` = re-retrieval top-K contains >=1 PMCID new since last run under current strictness. SMTP local no-auth/TLS only.[^impl-plan]

* P3.1 `tracker/sync_cron.py`: `schedule(freq)->job` (`APScheduler`, `daily|weekly|monthly`, default `weekly` from `data/config.json`) + `run_once()->{new_pmcids:int,at:str}` (calls `ingest/sync.py:sync_subscribed`, updates `sync_state(last_run)`, overlapping-run guard via job lock). Verify: `poetry run pytest tests/test_cron.py -q` (new-only, no duplicates, cadence default weekly). Forbidden: no OS cron, no `FIRST_PDATE` window filter (`FIRST_PDATE_D` sort still required).
* P3.2a `tracker/notify.py:match`: `find_affected(db_path,strictness)->list[session_id]` (re-run subscribed sessions' past questions, `TOP_K=15` current strictness, top-K overlap vs pre-run `papers`). Verify: `poetry run pytest tests/test_notify_match.py -q` (subscribed-only, unsubscribed ignored). Forbidden: no matching unsubscribed.
* P3.2b `tracker/notify.py:send`: `send_digest(affected,settings)->{sent:bool}` (one combined email subject `PAULI digest <date>: <N> session(s) with new papers`, one section/session: title+digest line+regenerated doctor-shape summary; send only if >=1 affected; `smtplib` local no-auth/TLS; failure writes loud `#mail-status` + retry next run, no backoff). Verify: `poetry run pytest tests/test_notify_send.py -q` (send-only-on-update, `smtplib` faked, failure status set). Forbidden: no auth/OAuth/cloud mailer, no per-session emails.
* P3.3 `tracker/export.py`: `render_export(session_id,db_path,chat_fn)->html` single-summary 1-page `#doctor-dialog` across ALL Q&As (title + 5 parts: short answer, citations, unknowns, doctor-Qs, digest line; `DOCTOR_SUMMARY_PROMPT`; ~500w max truncate w/ ellipsis, citations never dropped; `window.print()`). Verify: `poetry run pytest tests/test_export.py -q` (5 sections + word cap). Forbidden: no top-nav session picker, current-session-only.
* P3.4 `web/routes_settings.py`: `POST /settings/mail(to,smtp,from,freq)` + `GET /settings/db-stats` + `GET /sessions/{id}/doctor` + scheduler/job status (`POST /tracker/run` manual trigger returns `{run_at,new_pmcids,affected}`). Verify: `poetry run pytest tests/test_web_settings.py -q` (status+download, validation errors 422). Forbidden: no secrets in responses/logs.
* P3-gate: `poetry run pytest tests/test_cron.py tests/test_notify_match.py tests/test_notify_send.py tests/test_export.py tests/test_web_settings.py -q` green + manual export review checklist (5 parts, cites resolve, <=500w, prints 1 page).[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
