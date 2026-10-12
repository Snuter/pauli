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

Implements [tracker](/architecture/tracker-export.md).[^impl-plan]

* P3.1 `tracker/sync_cron.py`: in-app scheduler at the Settings cadence (once a week by default); each run re-extracts terms from subscribed sessions' past questions, ID-first lookup + PMCID-filter, append-only. Verify new-only sync (no duplicates) + cadence default.[^impl-plan]
* P3.2 `tracker/notify.py`: per-session match by re-running past questions of subscribed sessions only with current strictness/`TOP_K=15`; send one combined email via local no-auth/TLS SMTP only for MVP (decided 2026-10-12; Settings recipient + sender/SMTP) only when at least one subscribed session is affected, one section per affected session with regenerated single-summary output. New-only MVP. Verify subscribed-only match + send-only-on-update + loud SMTP-failure status.[^impl-plan]
* P3.3 `tracker/export.py`: single-summary 1-page print-view HTML across ALL Q&As (session title + condensed summary: short answer, citations, unknowns, doctor questions). Verify `test_export.py` 5 sections, ~500 words max for the summary.[^impl-plan]
* P3.4 `web/routes_settings.py`: update-check email fields (cadence, recipient, sender, SMTP) + scheduler/job status, export page. Verify status + download.[^impl-plan]
* P3-gate: full `pytest` green, manual export review.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
