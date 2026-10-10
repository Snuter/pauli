---
type: Concept
title: Implementation plan summary
description: Step-by-step build plan — phases S, P0-P3 with verify criteria, non-goals.
tags: [pauli, source, plan]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: impl-plan
    resource: /docs/implementation-plan.md
    title: P.A.U.L.I. Implementation Plan
---

# Implementation plan summary

Derived from [technical](/sources/concept-technical-summary.md) + [user-journey](/sources/concept-user-journey-summary.md) concepts. Stack: Python >=3.13, Poetry, pytest + python-playwright (`pytest-playwright`), FastAPI + Jinja + HTMX only, SQLite + sqlite-vec, user-configured Ollama. Each step is one unit of work with `Verify:` criteria; run `poetry run pytest tests/<file>` after each code step (`tests/ui` for UI steps) — full layers in [testing strategy](/architecture/testing.md).[^impl-plan]

Constraints: no default topics; OA-only; scheduled in-app sync+notify (cadence setting, weekly default), send-only-on-update; single-user no auth; fetch all matches paged + resumable; missing model/key is hard misconfiguration. `setup_dev_ai.sh` dev-only, never runtime; no shipped model, key, or SMTP secret.[^impl-plan]

# Phases

* S skeleton/config/DB — [phase S](/implementation/phase-S.md).
* P0 cache + search — [phase P0](/implementation/phase-P0.md).
* P1 RAG + anti-hallucination — [phase P1](/implementation/phase-P1.md).
* P2 warnings — [phase P2](/implementation/phase-P2.md).
* P3 tracker + printout — [phase P3](/implementation/phase-P3.md).
* Exclusions — [non-goals](/implementation/non-goals.md).

[^impl-plan]: P.A.U.L.I. Implementation Plan
