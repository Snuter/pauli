---
type: Phase
title: Phase P2 — trigger warnings
description: Detector, gate, events, wiring (P2.1-P2.4).
tags: [pauli, phase-P2]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: impl-plan
    resource: /docs/implementation-plan.md
    title: P.A.U.L.I. Implementation Plan
---

# Phase P2

Implements [safety gating](/architecture/safety-gating.md). Depends on P1.2 GATE emission + P1.5 simplicity + P1.6 service hook. LLM-only tags; no keyword scan anywhere (negative test enforced). Crisis resources static list in `resources.py`.[^impl-plan]

* P2.1 `safety/detector.py`: `parse_tags(text)->list[str]` (allowlist `suicidality|prognosis|disability|pregnancy|trauma|pem-crash`, regex `\[GATE:([a-z-]+)\]`) + `strip_tags(text)->str`; unknown tags stripped, missing tags=no gate (accepted false-negative), case-sensitive, multi-tag supported, whole-answer single gate regardless of count. Verify: `poetry run pytest tests/test_warnings.py -q` (6 categories +/- incl. unknown-strip + missing-no-gate + multi-tag + case). Forbidden: no regex keyword scan (`grep -r suicid pauli/safety` must be allowlist/tests only).
* P2.2 `safety/gate.py` + `safety/resources.py`: `should_gate(tags,sensitivity)->bool` (`low`=suicidality-only, `standard`=all 6, `hide`=title-only+double-confirm) + `render_card(category,simplicity)->html` (whole-answer single blurred card `Show/Skip/Why`, `aria-hidden`+inert until revealed, gentler wording at low simplicity via `language.py`) + `CRISIS_RESOURCES` (static EU-generic: call 112 + `Research info only` disclaimer; no national numbers in MVP). Copy variants per simplicity band stored as constants. Verify: `poetry run pytest tests/test_gate.py -q` (parametrized sensitivity x simplicity 10/12/15). Forbidden: no per-tag multi-cards, no auto-reveal.
* P2.3 `safety/events.py`: `log_event(category,action,mode,db_path)->None` (`warning_events(category,action,mode,at)` only — assert no question/answer text in DB). Verify: `poetry run pytest tests/test_warning_events.py -q` (PHI-leak negative). Forbidden: no query/answer logging.
* P2.4 Wire into `service.py` + Ask template before details: `answer()` calls detector->gate, blur card precedes content in DOM+SR order, question edit/move/delete resets gating. Verify: manual prognosis query gates at every slider setting + `poetry run pytest tests/test_service.py tests/test_warnings.py -q` + playwright gate-precedes-content assertion in `tests/ui/test_gating.py -q`. Forbidden: no keyword fallback reintroduced.
* P2-gate: `poetry run pytest tests/test_warnings.py tests/test_gate.py tests/test_warning_events.py tests/ui/test_gating.py -q` green.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
