---
type: Architecture
title: Safety gating
description: Six categories, keyword detector, blur card, sensitivity, event logging, tests.
tags: [pauli, safety]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# Safety gating

Categories: prognosis/mortality, suicidality, severe disability, pregnancy/children, medical trauma, PEM crash risk.[^tech-concept]

Detector: keyword + classifier on retrieved chunks and draft answer. UI: blurred card `This answer contains [category] — Show / Skip / Why am I seeing this?`, click-to-reveal only, gentler wording at simpler slider settings. Always `Research info only, not medical advice` + crisis resources where relevant.[^tech-concept] Sensitivity stored locally (single-user): `low` = suicidality/self-harm only, `standard` = all 6, `hide details` = title-only + double-confirm. Log shown/skipped (no PHI). Tests per category; gate fires at every slider setting.[^tech-concept]

User view: [gating](/workflows/sensitive-gating.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
