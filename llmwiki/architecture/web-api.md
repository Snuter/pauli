---
type: Architecture
title: Web API (HTMX endpoint table)
description: FastAPI + Jinja + HTMX routes replicating ui-mockup IDs/flows; approved 2026-10-12.
tags: [pauli, web, htmx]
status: stable
generated: {by: agent/opencode, at: 2026-10-12T00:00:00Z}
---

# Web API — approved 2026-10-12, templates frozen 2026-10-15 (per user Q&A)

Backend replicates `ui-mockup/index.html` element IDs. All pages server-rendered Jinja; mutations return HTMX fragments.

## Templates (frozen 2026-10-15)

`pauli/web/`: `app.py` (FastAPI + lifespan), `routes_sessions.py`, `routes_chat.py`, `routes_settings.py`, `templates/base.html`, `templates/settings.html`, `templates/ask.html`, `templates/fragments/session_li.html`, `templates/fragments/answer_li.html`, `templates/fragments/status.html`. Full pages extend `base.html` (Pico CSS, `.layout` grid, sidebar `#session-list` + `main`). Mutations return only the fragment file (same IDs as mockup, no layout wrapper).

Fragment example (`answer_li.html`, HTMX):

```html
<li>
<div class="q">{{ question }}</div>
<div class="q-actions no-print"><!-- move/edit/delete buttons, data-act=up|down|edit|del --></div>
<div class="a">{{ answer_html|safe }}</div>
</li>
```

```html
<form id="ask-form" hx-post="/sessions/{{ session_id }}/ask" hx-target="#history-list" hx-swap="beforeend">
<input id="ask-input" name="q" maxlength="500" required>
<button type="submit">Ask</button>
</form>
```

Polling: `<div hx-get="/sessions/{{ session_id }}/digest-progress" hx-trigger="every 2s" hx-target="this">` until `{digesting:false}`.

## Views

* `GET /` -> Settings (`#view-settings`: `#setup` + `#preferences`). 200 HTML.
* `GET /ask/{session_id}` -> Ask view (`#ask-title` = session title, `#history-list`, `#ask-form`+`#ask-input`, menu `#menu-sub[aria-pressed]` `#menu-doctor` `#menu-rename` `#menu-delete`). 404 HTML when unknown id.
* `GET /home` -> Home empty state (`#view-home`, Ask hidden incl. `#ask-form`). 200 HTML.

## Sessions (sidebar `#session-list`, newest-first `ORDER BY created_at DESC`)

| Method+path | Request (form) | Success | Errors |
|---|---|---|---|
| `POST /sessions` | `title: str, trim, 1-60 chars` | 200 fragment (prepend `#session-list li`) + `HX-Redirect: /ask/{id}` | 422 fragment (inline hint, dialog stays open) on empty/duplicate |
| `POST /sessions/{id}/rename` | `title: str, trim, 1-60` (`#rename-dialog #rename-input maxlength=60`) | 200 fragment (updated title) + bump `created_at` | 422 hint on empty/duplicate; 404 unknown id |
| `POST /sessions/{id}/delete` | confirm via `#delete-dialog` (no fields) | 200 fragment (remove li); empty list -> `HX-Redirect: /home` | 404 unknown id |
| `POST /sessions/{id}/subscribe-toggle` | none | 200 fragment `#menu-sub[aria-pressed=true|false]` + bump `created_at` | 404 unknown id |

Any session data change bumps `created_at` (ask/edit/move/delete-q/rename/sub-toggle).

## Q&A (`#history-list li`, per-Q `.q-actions`)

| Method+path | Request (form) | Success | Errors |
|---|---|---|---|
| `POST /sessions/{id}/ask` | `q: str, trim, 1-500` | 200 append `#history-list li` (fast-slice answer; while backfill: `data-testid=incomplete-badge` + `data-testid=digest-progress` + `data-testid=refresh-answer`); misconfig -> 200 setup-hint fragment instead of answer | 422 on empty/overlong `q`; 404 unknown session |
| `POST /sessions/{id}/questions/{pos}/refresh` | `pos: int, 0-based \`session_answers.position\`` | 200 replace `li` in place, clear incomplete | 404 bad pos |
| `POST /sessions/{id}/questions/{pos}/move` | `dir: up\|down` (swap `position`; boundary buttons `disabled`) | 200 reorder fragment; doctor sheet follows new first | 422 bad `dir`; 404 bad pos |
| `POST /sessions/{id}/questions/{pos}/edit` | `q: str, 1-500` (`#qedit-dialog`, rerun retrieve+generate, reset gating) | 200 replace in place | 422 on empty/overlong; 404 bad pos |
| `POST /sessions/{id}/questions/{pos}/delete` | confirm `#qdelete-dialog` | 200 remove `li` session-locally (corpus untouched) | 404 bad pos |

Backfill polling: `GET /sessions/{id}/digest-progress` (2s interval, `{digesting:bool,count:int}`) until complete; manual `refresh-answer` triggers refresh endpoint above.

## Settings (`#view-settings`)

| Method+path | Request (form) | Success | Errors |
|---|---|---|---|
| `POST /settings/ollama` | `host: url, chat_model: str (required, no default), embed_model: str (=nomic-embed-text), mode: local\|cloud, key: str (cloud-only, never echoed)` | 200 `#ollama-hello-status` saved note (key never returned) | 422 bad host/empty chat_model in cloud without key |
| `POST /settings/ollama/test` | none (uses saved) | 200 `#ollama-hello-status` greeting (`Say hi briefly.`, 15s timeout) | 200 fail-closed string (missing model/key, unreachable/timeout) — never 500 |
| `POST /settings/strictness` | `strictness: int 0-100` -> `threshold=strictness/100*0.6` | 200 value echo | 422 out of range |
| `POST /settings/simplicity` | `simplicity: int 10-15` | 200 value echo | 422 out of range |
| `POST /settings/sensitivity` | `sensitivity: low\|standard\|hide` | 200 value echo | 422 bad value |
| `GET /settings/db-stats` | none | 200 `#terms-stats` `{db_bytes,papers,chunks,vectors,last_run}` via `get_db_stats()` | 200 zeros when no DB |
| `POST /settings/mail` | `to: email, from: email, smtp: host[:port], freq: daily\|weekly\|monthly` | 200 `#mail-status` (`N subscribed` / failure text loudly) | 422 bad email/freq; SMTP failure -> 200 loud status (retry next run) |

## Doctor export / mail

| Method+path | Request | Success | Errors |
|---|---|---|---|
| `GET /sessions/{id}/doctor` | none | 200 `#doctor-dialog` single LLM summary across ALL Q&As (title + short + cites + unknowns + doctor-Qs; ~500w max) + Print | 404 unknown id |
| `POST /tracker/run` | none (manual; scheduler `APScheduler` `mail_freq` default `weekly`) | 200 `{run_at, new_pmcids:int, affected:[session_id]}`; email only if >=1 affected | SMTP failure -> 200 `{sent:false}` + loud `#mail-status` |

Content-type: full pages `text/html`; HTMX mutations return HTML fragments with the same element IDs listed above. Mutations return `HX-Redirect` only where noted. 500s render fail-closed fragment, never leak keys.
