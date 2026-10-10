---
type: Workflow
title: Settings — setup and preferences
description: Unified Settings screen — Ollama setup, 1-5 buzzwords OR-union with validation + full OA fetch, plus sensitivity, strictness, simplicity.
tags: [pauli, settings]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: user-journey
    resource: /docs/concept-user-journey.md
    title: P.A.U.L.I. User-Journey Concept
---

# Settings — setup and preferences

All first-run setup and all preference controls live on one Settings screen — no separate Setup page.

## Setup (first run)

1. Pick Ollama setup once: local models (default, private, no key) or Ollama cloud models (needs your `OLLAMA_API_KEY`, stored locally only, never shipped). Without the configured model (or cloud key for cloud) the app reports misconfiguration instead of answering.[^user-journey]
2. Enter 1–5 buzzwords, e.g. `myalgic encephalomyelitis`, `PEM`. Terms combine with OR-union into one topic.[^user-journey] Buzzwords are configured once globally for all asking sessions — every session retrieves from this same corpus.
3. App checks each term against Europe PMC: empty, too short, or too broad (`>50k` hits) gets a narrow-down hint.[^user-journey]
4. Valid topic fetches all matching Open Access papers (no 500-paper cap; paged with progress, resumable). Answers come from your configured Ollama model; cached papers stay local (local mode) or follow Ollama cloud terms (cloud mode).[^user-journey]

No built-in default topics — library starts from what you enter.[^user-journey]

## Preferences (same screen)

* Sensitivity (gating): `low / standard / hide details` — see [gating](/workflows/sensitive-gating.md).
* Retrieval strictness: `0–100` slider → threshold `0.0–0.6` (default `0.3`, `TOP_K=15` fixed) — see [gating](/workflows/sensitive-gating.md).
* Simplicity of wording: `10–15` slider (default `12`) — see [language](/workflows/language-toggle.md).

Next: [ask a question](/workflows/asking-question.md).

[^user-journey]: P.A.U.L.I. User-Journey Concept
