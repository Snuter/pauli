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

Detector: generation prompt instructs the Ollama chat model to emit inline tags at sensitive points, LLM-only with no keyword fallback (decided 2026-10-12). Allowlist (frozen tokens): `[GATE:suicidality]` `[GATE:prognosis]` `[GATE:disability]` `[GATE:pregnancy]` `[GATE:trauma]` `[GATE:pem-crash]`. `safety/gate.py` parses allowlisted tags, strips them from display, and renders a whole-answer single blurred card (decided 2026-10-12; one card per answer regardless of tag count). Missing tags = no gate (accepted false-negative risk). UI: blurred card headline from `safety/resources.py:gate_intro(category,simplicity)` + `Show / Skip / Why am I seeing this?` (`SHOW_LABEL/SKIP_LABEL/WHY_LABEL`), `Why` text = `WHY_STANDARD` (or `WHY_HIDE` in hide mode), click-to-reveal only, gentler wording at simplicity 10-11 via `gate_intro`. Always frozen copy (frozen 2026-10-15 per user Q&A in `safety/resources.py`): `DISCLAIMER = Research info only, not medical advice.` + suicidality crisis line `CRISIS_LINE = Crisis: call 112` (EU-generic, no national numbers in MVP).[^tech-concept] Sensitivity stored locally (single-user): `low` = honor suicidality/self-harm tags only, `standard` = honor all 6, `hide details` = title-only + double-confirm. Log shown/skipped (no PHI: category+action only). Tests per category incl. tag-strip + missing-tag tests; gate fires at every slider setting.[^tech-concept]

User view: [gating](/workflows/sensitive-gating.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
