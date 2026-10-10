---
type: Architecture
title: Language modes
description: Standard/Simple implementation, simplicity slider, textstat verification.
tags: [pauli, language]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# Language modes

Toggle `Standard / Simple` + `simplicity` slider (sentence length 10–15, glossary on/off). Same chunks and citations, different wording.[^tech-concept]

* Standard: grade 8–10, term + short definition, e.g. `post-exertional malaise (crash after effort)`.[^tech-concept]
* Simple: grade 5–6, `<15`-word sentences, expand acronyms, glossary (`PEM -> crash after effort`), `What this means:` line.[^tech-concept]

Simplification adds no facts; citation check applies to both; default Simple for first answer; verify per-mode with `textstat` Flesch-Kincaid.[^tech-concept]

User view: [language toggle](/workflows/language-toggle.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
