---
type: Workflow
title: Asking a question
description: Short cited answers under 150 words or honest unknown with 3-way split. Multiple asking sessions on one shared corpus.
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
3. No answer in cached papers → honest unknown, never a guess: `I don't know from your cached papers — [what is missing, what term to add, what to ask your doctor]`.[^user-journey]
4. Three-way split: no papers cached yet / papers cached but no answer / conflicting papers shown as both cited sides (no automatic contradiction detection in MVP).[^user-journey]

## Asking sessions

* Multiple asking sessions share one global corpus (see [settings](/workflows/onboarding-buzzwords.md)). Only the user prompts / history differentiate sessions — no per-session system prompt, retrieval config, or buzzwords.
* Sessions are freely user-creatable. Seed examples: `ME/CFS therapies and details`, `ME/CFS cure research`. No other defaults. Deleting a session (Ask `Delete this session` button → modal confirm) removes the session entirely, including seeds; deleting the last session leaves an empty state prompting a new title in the sidebar.
* Each session keeps its own Q&A history, auto-persisted on every Ask. Retrieval, strictness, and simplicity live under Settings and stay global.
* Each session has its own Subscribe toggle for the email digest (Ask menu button, `aria-pressed`, next to doctor-summary and delete; mail icon, filled active state when on) — only subscribed sessions are matched and mailed (see [tracking](/workflows/tracking-doctor-visit.md)).
* Each session gets its own condensed 1-page printout via the Ask `Doctor summary / print` button dialog (see [tracking](/workflows/tracking-doctor-visit.md)).
* UI: the sidebar `Research Sessions` list is the single session picker and the only entry point to chat — there is no `Ask` or `Doctor` nav item. The Ask heading is the active session title (`No session yet` when empty); three buttons (`Subscribe`, `Doctor summary / print`, `Delete this session` in red outline) sit side by side below the title for per-session actions. The sidebar has only new-title input + create button (no delete button); deletion requires modal confirmation. New titles are limited to 60 chars; long titles truncate with ellipsis (no sidebar stacking on small screens).

Related: [language](/workflows/language-toggle.md), [gating](/workflows/sensitive-gating.md).

[^user-journey]: P.A.U.L.I. User-Journey Concept
