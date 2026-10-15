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

`simplicity` slider only (sentence length 10–15, glossary on/off). Same chunks and citations, different wording. Implementation is LLM rewrite only (decided 2026-10-15 per user Q&A): `questionanswering/language.py:simplify(text,simplicity,chat_fn)` calls the Ollama chat model with canonical `prompts.py:SIMPLIFY_PROMPT` (never hand-written); no code sentence-splitting or glossary map.[^tech-concept]

* Low end (10–11): very short sentences, expand acronyms, full glossary (`PEM -> crash after effort`), `What this means:` line.[^tech-concept]
* Mid (12–13, default 12): short sentences + glossary.[^tech-concept]
* High end (14–15): longer sentences, less glossary; keeps term + short definition, e.g. `post-exertional malaise (crash after effort)`.[^tech-concept]

Simplification adds no facts; citation check applies at every slider setting; verify with `textstat` Flesch-Kincaid across the slider range — frozen targets (grade level): 10→6, 12→8 (default), 15→10; assert monotonic increase with slider and citations preserved. `SIMPLIFY_PROMPT` takes `{text}` + `{simplicity}` (10-15) and instructs short sentences + glossary per band below; model must preserve every `[PMC\d+]` token verbatim.[^tech-concept]

User view: [language toggle](/workflows/language-toggle.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
