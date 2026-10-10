---
type: Workflow
title: Asking a question
description: Short cited answers under 150 words or honest unknown with 3-way split.
tags: [pauli, qa]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: user-journey
    resource: /docs/concept-user-journey.md
    title: P.A.U.L.I. User-Journey Concept
---

# Asking

1. Ask in chat, e.g. `What triggers PEM?`[^user-journey]
2. Short answer (`<150` words) with every fact linked to a Europe PMC paper `[PMCID]`.[^user-journey]
3. No answer in saved papers → honest unknown, never a guess: `I don't know from your saved papers — [what is missing, what term to add, what to ask your doctor]`.[^user-journey]
4. Three-way split: no papers cached yet / papers cached but no answer / conflicting papers shown as both cited sides (no automatic contradiction detection in MVP).[^user-journey]

Related: [language](/workflows/language-toggle.md), [gating](/workflows/sensitive-gating.md).

[^user-journey]: P.A.U.L.I. User-Journey Concept
