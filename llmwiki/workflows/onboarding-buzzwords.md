---
type: Workflow
title: Onboarding with buzzwords
description: Ollama setup once, 1-5 buzzwords OR-union, per-term validation, full OA fetch.
tags: [pauli, onboarding]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: user-journey
    resource: /docs/concept-user-journey.md
    title: P.A.U.L.I. User-Journey Concept
---

# Onboarding

1. Pick Ollama setup once: local models (default, private, no key) or Ollama cloud models (needs your `OLLAMA_API_KEY`, stored locally only, never shipped). Without the configured model (or cloud key for cloud) the app reports misconfiguration instead of answering.[^user-journey]
2. Enter 1–5 buzzwords, e.g. `myalgic encephalomyelitis`, `PEM`. Terms combine with OR-union into one topic.[^user-journey]
3. App checks each term against Europe PMC: empty, too short, or too broad (`>50k` hits) gets a narrow-down hint.[^user-journey]
4. Valid topic fetches all matching Open Access papers (no 500-paper cap; paged with progress, resumable). Answers come from your configured Ollama model; cached papers stay local (local mode) or follow Ollama cloud terms (cloud mode).[^user-journey]

No built-in default topics — library starts from what you enter.[^user-journey]

Next: [ask a question](/workflows/asking-question.md).

[^user-journey]: P.A.U.L.I. User-Journey Concept
