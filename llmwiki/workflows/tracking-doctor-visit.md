---
type: Workflow
title: Tracking and doctor visit
description: Scheduled checks, per-session email digest, auto-persisted sessions, per-session condensed 1-page print export.
tags: [pauli, tracker]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: user-journey
    resource: /docs/concept-user-journey.md
    title: P.A.U.L.I. User-Journey Concept
---

# Tracking

* Scheduled checks for new papers (in-app scheduler, per-topic `last_sync`, new PMCIDs only; cadence is a Settings choice, once a week by default).[^user-journey]
* Email digest in plain language, sent only when new papers match at least one session: one combined email with one section per affected session — a session is affected when new papers land in its top-K on re-retrieval with the current strictness/`TOP_K=15`. Each section carries the regenerated LLM output in doctor-printout shape. New-papers-only MVP (no deleted/updated marks). Recipient + sender/SMTP + cadence live in Settings (stored locally); delivery failure is shown loudly in Settings status.[^user-journey]
* Sessions auto-persist — every Ask is kept in its session history, no manual save step. Single-user local, no auth.[^user-journey]
* Doctor export: condensed 1-page dialog in Ask (`#doctor-dialog`: session title, short answer, citations, unknowns, suggested doctor questions, Print / save as PDF) per asking session, opened from the `Doctor summary / print` button below the session title.[^user-journey] It always shows the current Ask session — no top-nav Doctor entry, no separate picker.

[^user-journey]: P.A.U.L.I. User-Journey Concept
