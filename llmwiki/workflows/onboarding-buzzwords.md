---
type: Workflow
title: Settings — Initial Setup and Preferences
description: Single Settings page split into Initial Setup (Ollama, retrieval strictness, AI auto-collected topics + digest status, optional subscription email) and Preferences (sensitivity, simplicity).
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

1. Pick Ollama setup once: local models (default, private, no key) or Ollama cloud models (needs your `OLLAMA_API_KEY`, stored locally only, never shipped). Without the configured model (or cloud key for cloud) the app reports misconfiguration instead of answering.[^user-journey] A `Test Ollama` button sends `Say hi briefly.` to the configured host/model (`{host}/api/chat`, `Bearer` key in cloud mode) and shows the model's greeting — or a fail-closed misconfiguration/unreachable error — inline.
2. No manual buzzwords — the AI extracts search terms from each question plus session history (`pauli/questionanswering/extract.py` via the configured Ollama chat model). Whatever the model returns (normalized, deduped) is accepted — no per-term hit-count gate. All terms feed one shared corpus used by every asking session.
3. New terms fetch a fast slice first (newest ~50–100 OA papers) so Ask can answer immediately, marked incomplete; the remaining matches backfill in the background with digest progress. The answer is refreshed manually in place via `Refresh answer`. Cached papers stay local (local mode) or follow Ollama cloud terms (cloud mode).[^user-journey]

No built-in default topics — the corpus starts from what you ask.[^user-journey]

Auto-collected topics live under Initial Setup as count + database statistics only — no per-term list (term count, digesting/complete split, total + avg papers/term, DB size + paper/chunk/vector rows via `get_db_stats()` to guide the limit choice). Term limit configurable, default 500; the cap is enforced only on the auto-prune schedule (`prune_freq` every day / week / month, default every day; no per-term age check — scheduled run drops least-recently-used terms down to the limit and their vectors are dropped).

* Retrieval strictness: `0–100` slider → threshold `0.0–0.6` (default `0.3`, `TOP_K=15` fixed) — see [gating](/workflows/sensitive-gating.md). It controls how much retrieved text is placed into the model's context window: lower strictness sends more passages and needs a larger window. Usable context size depends on the model (each model has a fixed maximum) and on your hardware (a local model needs enough RAM/VRAM to hold it; cloud models follow the provider's limits). If answers get cut off, turn incoherent, or everything gets very slow, raise strictness or switch to a model with a larger context window on hardware that can hold it.

### Optional setup: subscription email

Check cadence (once a week by default), recipient + sender/SMTP fields; one combined email per check, sent only when new papers match a subscribed session (Subscribe toggle in Ask); failures shown loudly — see [tracking](/workflows/tracking-doctor-visit.md).

## Preferences (`#preferences`)

* Sensitivity gating: `low / standard / hide details` — see [gating](/workflows/sensitive-gating.md).
* Simplicity of wording: `10–15` slider (default `12`) — see [language](/workflows/language-toggle.md).

Next: [ask a question](/workflows/asking-question.md).

[^user-journey]: P.A.U.L.I. User-Journey Concept
