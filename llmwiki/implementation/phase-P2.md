---
type: Phase
title: Phase P2 — trigger warnings
description: Detector, gate, events, wiring (P2.1-P2.4).
tags: [pauli, phase-P2]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: impl-plan
    resource: /docs/implementation-plan.md
    title: P.A.U.L.I. Implementation Plan
---

# Phase P2

Implements [safety gating](/architecture/safety-gating.md).[^impl-plan]

* P2.1 `safety/detector.py`: parse LLM-only `[GATE:...]` tags (allowlist above, strip from display; no keyword scan). Verify `test_warnings.py` ± per category incl. unknown-tag strip + missing-tag no-gate.[^impl-plan]
* P2.2 `safety/gate.py` + `resources.py`: whole-answer single blur card Show/Skip/Why, simpler-slider wording, advice disclaimer + crisis resources, `low`/`standard`/`hide details` local (low honors suicidality tags only). Verify across slider range parametrized.[^impl-plan]
* P2.3 `safety/events.py`: shown/skipped log, category+action only. Verify no query text.[^impl-plan]
* P2.4 Wire into `service.py` + template before details. Verify manual prognosis query gates at every slider setting.[^impl-plan]
* P2-gate: `test_warnings.py` green, gate precedes content (unit + `tests/ui/` playwright assertion).[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
