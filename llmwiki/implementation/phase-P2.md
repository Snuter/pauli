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

* P2.1 `safety/detector.py`: keyword scan of chunks + draft, 6 categories. Verify `test_warnings.py` ± per category.[^impl-plan]
* P2.2 `safety/gate.py` + `resources.py`: blur card Show/Skip/Why, Simple wording, advice disclaimer + crisis resources, `low`/`standard`/`hide details` local. Verify both modes parametrized.[^impl-plan]
* P2.3 `safety/events.py`: shown/skipped log, category+action only. Verify no query text.[^impl-plan]
* P2.4 Wire into `service.py` + template before details. Verify manual prognosis query gates in both modes.[^impl-plan]
* P2-gate: `test_warnings.py` green, gate precedes content.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
