---
type: Phase
title: Phase P1 — RAG chat
description: Retrieve, generate, citations, abstain, language, service, web UI (P1.1-P1.7).
tags: [pauli, phase-P1]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: impl-plan
    resource: /docs/implementation-plan.md
    title: P.A.U.L.I. Implementation Plan
---

# Phase P1

Implements [RAG](/architecture/rag-chat.md) + [language](/architecture/language-modes.md).[^impl-plan]

* P1.1 `questionanswering/retrieve.py`: rewrite + top-k (`TOP_K=15`) + threshold (`0.3`, strictness → `0.0–0.6`). Verify empty→abstain, slider mapping.[^impl-plan]
* P1.2 `questionanswering/generate.py`: chunks-only via `ollama-python` + `OLLAMA_CHAT_MODEL`, never opencode, fail closed. Verify mocked prompt, no key in logs.[^impl-plan]
* P1.3 `questionanswering/citations.py`: factual sentences end `[PMCID]` ∈ retrieval set. Verify presence + validity (invented rejected).[^impl-plan]
* P1.4 `questionanswering/abstain.py`: unknown template, 3 branches, never guess. Verify `test_abstain.py`.[^impl-plan]
* P1.5 `questionanswering/language.py`: simplicity slider only (10–15, default 12), same citations. Verify `textstat` + preservation.[^impl-plan]
* P1.6 `questionanswering/service.py`: rewrite→retrieve→generate→check→abstain→render. Verify mocked e2e incl. misconfiguration error.[^impl-plan]
* P1.7 `web/app.py` + `routes_topics.py` + `routes_chat.py`: FastAPI + Jinja + HTMX chat, toggles + sliders + auto-collected topics list + incomplete/refresh. Verify `What triggers PEM?` → `<150` words, 3+ links or unknown; UI smoke via `tests/ui/` (playwright: nav, example answer, citation links resolve).[^impl-plan]
* P1-gate: `pytest` green, zero invented citations.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
