---
type: Architecture
title: Tracker + doctor export
description: Follow topics, manual digest, SQLite library, sessions, per-session condensed 1-page print HTML.
tags: [pauli, tracker]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# Tracker + export

Follow topics; weekly manual digest in plain language. Library: save answers/papers (SQLite relations to PMCID + answer id), single-user no auth, no retention/delete in MVP. Sessions: `sessions (id, title, created_at)` + `session_answers (session_id, question, answer_id)`; library entries tagged with `session_id`; deleting a session removes the session entirely (plus its history). Export: condensed 1-page dialog per session in Ask (print to PDF) with session title, short answer, citations, unknowns, suggested doctor questions.[^tech-concept]

User view: [tracking](/workflows/tracking-doctor-visit.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
