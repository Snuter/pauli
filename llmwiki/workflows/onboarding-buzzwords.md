---
type: Workflow
title: Settings — Initial Setup and Preferences
description: Single Settings page split into Initial Setup (Ollama, retrieval strictness, 1-5 buzzwords OR-union + full OA fetch, optional subscription email) and Preferences (sensitivity, simplicity).
tags: [pauli, settings]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: user-journey
    resource: /docs/concept-user-journey.md
    title: P.A.U.L.I. User-Journey Concept
---

# Settings — Initial Setup and Preferences

One Settings page split into two anchored groups — `#setup` Initial Setup first, `#preferences` Preferences below. `/` defaults to Settings.

## Initial Setup (`#setup`)

1. Pick Ollama setup once: local models (default, private, no key) or Ollama cloud models (needs your `OLLAMA_API_KEY`, stored locally only, never shipped). Without the configured model (or cloud key for cloud) the app reports misconfiguration instead of answering.[^user-journey]
2. Enter 1–5 buzzwords, e.g. `myalgic encephalomyelitis`, `PEM`. Terms combine with OR-union into one topic.[^user-journey] Buzzwords are configured once globally for all asking sessions — every session retrieves from this same corpus.
3. App checks each term against Europe PMC: empty, too short, or too broad (`>50k` hits) gets a narrow-down hint.[^user-journey]
4. Valid topic fetches all matching Open Access papers (no 500-paper cap; paged with progress, resumable). Answers come from your configured Ollama model; cached papers stay local (local mode) or follow Ollama cloud terms (cloud mode).[^user-journey]

No built-in default topics — the corpus starts from what you enter.[^user-journey]

* Retrieval strictness: `0–100` slider → threshold `0.0–0.6` (default `0.3`, `TOP_K=15` fixed) — see [gating](/workflows/sensitive-gating.md). It controls how much retrieved text is placed into the model's context window: lower strictness sends more passages and needs a larger window. Usable context size depends on the model (each model has a fixed maximum) and on your hardware (a local model needs enough RAM/VRAM to hold it; cloud models follow the provider's limits). If answers get cut off, turn incoherent, or everything gets very slow, raise strictness or switch to a model with a larger context window on hardware that can hold it.

### Optional setup: subscription email

Check cadence (once a week by default), recipient + sender/SMTP fields; one combined email per check, sent only when new papers match a subscribed session (Subscribe toggle in Ask); failures shown loudly — see [tracking](/workflows/tracking-doctor-visit.md).

## Preferences (`#preferences`)

* Sensitivity (gating): `low / standard / hide details` — see [gating](/workflows/sensitive-gating.md).
* Simplicity of wording: `10–15` slider (default `12`) — see [language](/workflows/language-toggle.md).

Next: [ask a question](/workflows/asking-question.md).

[^user-journey]: P.A.U.L.I. User-Journey Concept
