---
type: Architecture
title: Language modes
description: Simplicity-slider-only wording control, textstat verification.
tags: [pauli, language]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# Language modes

`simplicity` slider only (sentence length 10–15, glossary on/off). Same chunks and citations, different wording.[^tech-concept]

* Low end (10–11): very short sentences, expand acronyms, full glossary (`PEM -> crash after effort`), `What this means:` line.[^tech-concept]
* Mid (12–13, default 12): short sentences + glossary.[^tech-concept]
* High end (14–15): longer sentences, less glossary; keeps term + short definition, e.g. `post-exertional malaise (crash after effort)`.[^tech-concept]

Simplification adds no facts; citation check applies at every slider setting; verify with `textstat` Flesch-Kincaid across the slider range.[^tech-concept]

User view: [language toggle](/workflows/language-toggle.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
