---
type: Architecture
title: RAG chat + anti-hallucination
description: Rewrite-retrieve-generate pipeline with code-enforced citations and abstention. Sessions are UI threads over one shared corpus.
tags: [pauli, rag]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# RAG chat

Rewrite (`pauli/questionanswering/retrieve.py`) → retrieve top-k above threshold (`retrieve.py` + `pauli/index/store.py`, `TOP_K=15`, `SCORE_THRESHOLD=0.3`, strictness `0–100` → `threshold = strictness/100*0.6` linear, cosine similarity via sqlite-vec, decided 2026-10-12; `TOP_K` fixed) → generate from chunks only via user-configured Ollama (`pauli/questionanswering/generate.py` via `ollama-python` on `OLLAMA_HOST` + `OLLAMA_CHAT_MODEL`; `OLLAMA_API_KEY` only for cloud; never via `ollama launch opencode` harness) → code post-check (`citations.py`, `abstain.py`) → render.[^tech-concept] Missing model / cloud key = hard misconfiguration with setup hint, reported instead of answering.[^tech-concept]

Guidelines: chunks-only system prompt (`questionanswering/prompts.py:GENERATE_SYSTEM`), no general knowledge; every factual sentence ends `[PMCID]` to Europe PMC; citations must be in retrieval set or fail closed; below-threshold / unsupported → unknown template (`ABSTAIN_TEMPLATE`), never guess; split no-papers / no-answer / conflicting (both cited sides, no auto contradiction detection); rewrite via `REWRITE_PROMPT`; citation-presence, validity, abstention tests.[^tech-concept]

Unknown: `I don't know from your cached papers — [what is missing, what term to add, what to ask your doctor]`.[^tech-concept]

Sessions: asking sessions are presentation-layer threads only. Rewrite → retrieve → generate is identical for every session against the shared global corpus; only the user-prompt history differs. No per-session index, terms, strictness, or system prompt. The daily notify job only *reads* each session's history for matching — it never forks the corpus.

User view: [asking](/workflows/asking-question.md).

[^tech-concept]: P.A.U.L.I. Technical Concept
