---
type: Workflow
title: Sensitive topics stay gated
description: Six gated categories, blur card click-to-reveal, sensitivity plus strictness sliders.
tags: [pauli, safety]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: user-journey
    resource: /docs/concept-user-journey.md
    title: P.A.U.L.I. User-Journey Concept
---

# Gating

Gate categories: prognosis/mortality, suicidality, severe disability, pregnancy/children, medical trauma, PEM crash risk.[^user-journey]

Sensitivity lives under Preferences on the Settings page alongside simplicity; retrieval strictness sits with the Ollama setup in Initial Setup (it controls how much context reaches the model) — optional subscription email is also in Initial Setup (see [settings](/workflows/onboarding-buzzwords.md)).

1. Blurred card first: `This answer contains [category] — Show / Skip / Why am I seeing this?`[^user-journey]
2. Nothing reveals without your click. Simpler slider settings use gentler wording.[^user-journey]
3. Every gated answer shows `Research info only, not medical advice`, plus local crisis resources where relevant.[^user-journey]
4. Sensitivity stored locally (single-user, no auth): `low` = gate only suicidality/self-harm, `standard` = gate all 6, `hide details` = title-only gate requiring double-confirm.[^user-journey] Retrieval strictness is separate: `strictness 0–100` slider → threshold `0.0–0.6` (default `0.3`, `TOP_K=15` fixed).[^user-journey]

[^user-journey]: P.A.U.L.I. User-Journey Concept
