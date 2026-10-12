---
type: Architecture
title: Safety gating
description: Six categories, LLM-tag gate, blur card, sensitivity, event logging, tests.
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

Detector: generation prompt instructs the Ollama chat model to emit inline tags at sensitive points, LLM-only with no keyword fallback (decided 2026-10-12). Allowlist (assumed simple tokens): `[GATE:suicidality]` `[GATE:prognosis]` `[GATE:disability]` `[GATE:pregnancy]` `[GATE:trauma]` `[GATE:pem-crash]`. `safety/gate.py` parses allowlisted tags, strips them from display, and renders one blurred card per span. Missing tags = no gate (accepted false-negative risk). UI: blurred card `This answer contains [category] — Show / Skip / Why am I seeing this?`, click-to-reveal only, gentler wording at simpler slider settings. Always `Research info only, not medical advice` + crisis resources where relevant.[^tech-concept] Sensitivity stored locally (single-user): `low` = honor suicidality/self-harm tags only, `standard` = honor all 6, `hide details` = title-only + double-confirm. Log shown/skipped (no PHI: category+action only). Tests per category incl. tag-strip + missing-tag tests; gate fires at every slider setting.[^tech-concept]

User view: [gating](/workflows/sensitive-gating.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
