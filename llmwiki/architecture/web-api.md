---
type: Architecture
title: Web API (HTMX endpoint table)
description: FastAPI + Jinja + HTMX routes replicating ui-mockup IDs/flows; approved 2026-10-12.
tags: [pauli, web, htmx]
status: stable
generated: {by: agent/opencode, at: 2026-10-12T00:00:00Z}
---

# Web API — approved 2026-10-12 (fragments resolved during P1.7)

Backend replicates `ui-mockup/index.html` element IDs. All pages server-rendered Jinja; mutations return HTMX fragments.

## Views

* `GET /` → Settings (`#view-settings`: `#setup` + `#preferences`).
* `GET /ask/{session_id}` → Ask view (`#ask-title` = session title, `#history-list`, `#ask-form`+`#ask-input`, menu `#menu-sub[aria-pressed]` `#menu-doctor` `#menu-rename` `#menu-delete`).
* `GET /home` → Home empty state (`#view-home`, Ask hidden incl. `#ask-form`).

## Sessions (sidebar `#session-list`, newest-first `ORDER BY created_at DESC`)

* `POST /sessions` (form `title≤60` trim, reject empty/duplicate with hint, 422) → prepend fragment + `HX-Redirect:/ask/{id}`.
* `POST /sessions/{id}/rename` (same validation, `#rename-dialog`) → update title + bump `created_at`.
* `POST /sessions/{id}/delete` (`#delete-dialog` confirm) → remove + history + subscription; empty → Home.
* `POST /sessions/{id}/subscribe-toggle` → flip `subscribed`, bump `created_at`, return `#menu-sub[aria-pressed]`.
* Any session data change bumps `created_at` (ask/edit/move/delete-q/rename/sub-toggle).

## Q&A (`#history-list li`, per-Q `.q-actions`)

* `POST /sessions/{id}/ask` (`q`) → extract transient terms → ID-first Europe PMC lookup → fast-slice answer (incomplete badge `data-testid=incomplete-badge` + `digest-progress` + `refresh-answer` while backfill runs) → append fragment.
* `POST /sessions/{id}/questions/{pos}/refresh` → replace answer in place, clear incomplete.
* `POST /sessions/{id}/questions/{pos}/move` (`dir=up|down`, swap `position`, boundary disabled) → reorder fragment; doctor sheet follows new first.
* `POST /sessions/{id}/questions/{pos}/edit` (`q≤500`, `#qedit-dialog`, rerun retrieve+generate, reset gating) → replace in place.
* `POST /sessions/{id}/questions/{pos}/delete` (`#qdelete-dialog` confirm) → remove session-locally.

## Settings (`#view-settings`)

* `POST /settings/ollama` (`host, chat_model, embed_model, mode, key`) + `POST /settings/ollama/test` (`#ollama-hello` → `#ollama-hello-status`, fail-closed strings).
* `POST /settings/strictness` (`0–100` → `threshold = strictness/100*0.6` linear), `POST /settings/simplicity` (`10–15`), `POST /settings/sensitivity` (`low|standard|hide`).
* `GET /settings/db-stats` → `#terms-stats` (`get_db_stats()`: bytes/papers/chunks/vectors; no term limit/prune UI).
* `POST /settings/mail` (`to,smtp,from,freq`) → `#mail-status`; SMTP failures surface here.

## Doctor export / mail

* `GET /sessions/{id}/doctor` → `#doctor-dialog` single LLM summary across ALL Q&As (title + short answer + citations + unknowns + doctor-questions; ~500 words max) + Print.
* `POST /tracker/run` (APScheduler weekly default) → re-extract terms from subscribed sessions' past questions + ID-first sync (`pageSize=100`/`HIT_LIMIT=50000`) + per-session top-K re-retrieval → single combined email only if ≥1 affected.

Open: exact fragment HTML, `position` migration (both resolved during P1.7; `#ollama-embed` already in mockup).
