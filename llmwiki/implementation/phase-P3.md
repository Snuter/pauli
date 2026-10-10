---
type: Phase
title: Phase P3 — tracker + printout
description: Library, digest, export, sync/library routes (P3.1-P3.4).
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

* P3.1 `tracker/library.py`: save answers/papers (PMCID + answer id). Verify save/list/unsave round-trip.[^impl-plan]
* P3.2 `tracker/digest.py`: manual plain-language digest since `last_sync`. Verify only newer papers (e.g. `3 new papers since 2026-09-30`).[^impl-plan]
* P3.3 `tracker/export.py`: 1-page print-view HTML with question, answer, citations, unknowns, doctor questions. Verify `test_export.py` 5 sections, ~500 words max.[^impl-plan]
* P3.4 `web/routes_sync.py` + `routes_library.py`: check-new-papers button, follow, library, export page. Verify manual count + download.[^impl-plan]
* P3-gate: full `pytest` green, manual export review.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
