---
type: Workflow
title: Language toggle
description: Standard grade 8-10 vs Simple grade 5-6 plus simplicity slider; citations unchanged.
tags: [pauli, language]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: user-journey
    resource: /docs/concept-user-journey.md
    title: P.A.U.L.I. User-Journey Concept
---

# Language toggle

Toggle `Standard / Simple` plus `simplicity` slider. Same papers and citations, different wording.[^user-journey]

* Standard: grade 8–10, keeps term + short definition, e.g. `post-exertional malaise (crash after effort)`.[^user-journey]
* Simple (default for first answer): grade 5–6, sentences `<15` words, expands all acronyms, glossary (`PEM -> crash after effort`), adds `What this means:` line. Slider adjusts sentence length (10–15) and glossary use.[^user-journey]

Simplification never adds new facts. Verified with `textstat` Flesch-Kincaid.[^user-journey]

[^user-journey]: P.A.U.L.I. User-Journey Concept
