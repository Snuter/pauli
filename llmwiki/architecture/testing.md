---
type: Architecture
title: Testing strategy
description: pytest unit/integration plus python-playwright UI tests — layers, layout, commands, conventions.
tags: [pauli, testing]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: impl-plan
    resource: /docs/implementation-plan.md
    title: P.A.U.L.I. Implementation Plan
---

# Testing strategy

Two layers. Unit/integration: `pytest` over `tests/test_*.py` with mocked HTTP (Europe PMC) and mocked Ollama vectors/generation; each [implementation](/implementation/index.md) step names its `Verify:` test.[^impl-plan] UI: `python-playwright` via `pytest-playwright` over `tests/ui/` against the static `ui-mockup/` (Chromium `page` fixture, session `mockup_url` file-URL fixture); seed coverage is `test_mockup_smoke.py` — settings (unified setup + preferences) visible by default, nav to Ask, example answer renders with resolvable Europe PMC citation links, sessions driven by the sidebar list (Ask heading is the active session title, `No session yet` when empty, plus two side-by-side icon buttons below the title for doctor-summary dialog and modal-confirmed delete; no Doctor nav item, no sidebar delete button, no per-view dropdowns).

# Layout + deps

Backend tests live in `tests/test_*.py` (temp DB, mocked vectors); UI tests in `tests/ui/` (`conftest.py` fixtures + `test_*.py`). Dev deps in `pyproject.toml`: `pytest`, `playwright`, `pytest-playwright` (see [stack](/architecture/tech-stack.md)). The browser binary is not in git — install per machine with `poetry run python -m playwright install chromium`. Artifacts `test-results/` and `playwright-report/` are gitignored.

# Commands

```bash
poetry install --with dev
poetry run python -m playwright install chromium
poetry run pytest tests/ -q        # everything
poetry run pytest tests/ui -v      # UI only
```

Run `poetry run pytest tests/<file>` after each implementation step.[^impl-plan]

# Conventions

Role-based locators (`get_by_role`) over CSS where possible; `exact=True` on ambiguous names (e.g. nav `Ask` vs `Continue to Ask`); `wait_for` before asserting visibility; gate tests assert the blur card precedes content at every slider setting ([safety gating](/architecture/safety-gating.md)); UI answer tests assert citations resolve to Europe PMC ([RAG](/architecture/rag-chat.md)).

# Phase mapping

* P0 cache/search: mocked-HTTP unit tests (paging, PMCID dedup); gate adds real-fetch manual check + `pytest` green.[^impl-plan]
* P1 RAG chat: citation/abstain/language unit tests + playwright smoke on ask → answer → citation links.[^impl-plan]
* P2 warnings: per-category detector tests, slider-parametrized gate tests, UI assertion that the gate precedes content.[^impl-plan]
* P3 tracker: library/digest/export unit tests; gate is full `pytest` green + manual export review.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
