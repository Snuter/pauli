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

Implements [RAG](/architecture/rag-chat.md) + [language](/architecture/language-modes.md). Depends on P0.7 store + S4 sessions tables. Prompts canonical in `questionanswering/prompts.py` (never invent wording). Mock Ollama via injected `chat_fn(prompt)->str`.[^impl-plan]

* P1.1 `questionanswering/retrieve.py`: `rewrite(question,history,chat_fn)->str` (`REWRITE_PROMPT`) + `retrieve(query_vec,strictness:int,db_path)->list[dict]` (`TOP_K=15` fixed, `threshold=strictness/100*0.6` linear cosine via sqlite-vec, default strictness 50 → 0.3). Verify: `poetry run pytest tests/test_retrieve.py -q` (empty->abstain signal, strictness 0/50/100 mapping to 0.0/0.3/0.6). Forbidden: no per-session index, no `topic_hash` arg, no `max()` floor.
* P1.2 `questionanswering/generate.py`: `generate(question,chunks,settings,chat_fn)->str` chunks-only via `ollama-python` (`OLLAMA_HOST`+`OLLAMA_CHAT_MODEL`), system=`get_generate_system()` (rendered `GENERATE_SYSTEM.format(vocab=GATE_VOCAB)` — never hand-format, never leak `{vocab}`). Verify: `poetry run pytest tests/test_generate.py tests/test_prompts.py -q` (mocked prompt contains GATE+CITE, no key in captured logs). Forbidden: no keyword fallback, no general knowledge.
* P1.3 `questionanswering/citations.py`: `check_citations(answer:str,retrieved:set[str])->list[str]` — the LLM decides which sentences are factual (checker never classifies); checker asserts every `[PMCID]` token (regex `\[PMC\d+\]`) is in the retrieval set, invented->fail (fail closed). Verify: `poetry run pytest tests/test_citations.py -q` (presence+validity, invented rejected, non-factual greetings pass through). Forbidden: no framework citation defaults, no keyword factuality heuristic.
* P1.4 `questionanswering/abstain.py`: `should_abstain(retrieved,threshold)->branch{no-papers|no-answer|conflicting}` + `render_unknown(missing,term,doctor_q)->str` (`ABSTAIN_TEMPLATE`, never guess; conflicting renders both cited sides). Verify: `poetry run pytest tests/test_abstain.py -q`. Forbidden: no guessing.
* P1.5 `questionanswering/language.py`: `simplify(text,simplicity:int)->str` slider 10-15 default 12 (sentence-length + glossary `PEM->crash after effort` low / `post-exertional malaise (crash after effort)` high + `What this means:` line at low end; citations unchanged, never adds facts; FK-grade targets 10→6, 12→8, 15→10). Verify: `poetry run pytest tests/test_language.py -q` (FK grade within ±1.5 of target + monotonic + citation preservation). Forbidden: no locale/i18n switch.
* P1.6 `questionanswering/service.py`: `answer(question,session_id,settings,db_path,chat_fn)->dict{html,plain,cite,unknown,doctor,gated}` pipeline rewrite->retrieve->generate->check->abstain->render (+misconfiguration branch reports setup hint instead of answering). Verify: `poetry run pytest tests/test_service.py -q` (mocked e2e + misconfig error). Forbidden: no PHI in logs beyond question.
* P1.7a `web/app.py` + `web/routes_sessions.py`: `GET /`, `GET /ask/{id}`, `GET /home`, `POST /sessions`, `POST /sessions/{id}/rename|delete|subscribe-toggle` — see [web API](/architecture/web-api.md) for fields/status/fragments. Verify: `poetry run pytest tests/test_web_sessions.py -q`.
* P1.7b `web/routes_chat.py` + Jinja templates: `POST /sessions/{id}/ask|questions/{pos}/refresh|move|edit|delete` with `incomplete-badge`+`digest-progress`+`refresh-answer` backfill polling (2s) replicating `ui-mockup/` IDs verbatim. Verify: `What triggers PEM?` -> `<150` words, 3+ `[PMC]` links or unknown; `poetry run pytest tests/test_web_chat.py tests/ui/test_mockup_smoke.py -q`. Forbidden: no React, no invented element IDs.
* P1-gate: `poetry run pytest tests/test_retrieve.py tests/test_generate.py tests/test_citations.py tests/test_abstain.py tests/test_language.py tests/test_service.py tests/test_web_sessions.py tests/test_web_chat.py -q` green, zero invented citations.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
