---
type: Concept
title: Technical concept summary
description: Scope, pipeline, RAG, language, safety, tracker, stack, phases, success criteria.
tags: [pauli, source, technical]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# Technical concept summary

Source: Europe PMC Open Access subset; companion to [user-journey summary](/sources/concept-user-journey-summary.md).[^tech-concept]

# Scope and constraints

Cached OA subset keyed by patient buzzwords, no built-in defaults; chat Q&A over cache; gated warning cards; local app + RAG (Python >=3.13, Poetry, pytest), single-user no auth, FastAPI + Jinja + HTMX only; weekly manual sync, no auto-cron; OA-only, no non-OA scraping.[^tech-concept]

# Pipeline

OR-union query, per-term validation, full paged ingest with resume, 512/50 chunking, Ollama embeddings, sqlite-vec with `topic_hash`, `last_sync` sync — [data pipeline](/architecture/data-pipeline.md).[^tech-concept]

# RAG + safety + language

Rewrite→retrieve (`TOP_K=15`, `0.3` + strictness slider)→chunks-only generate→code citation/abstain gates — [RAG](/architecture/rag-chat.md). Simplicity slider only (10–15), `textstat`-verified — [language](/architecture/language-modes.md). Six-category keyword gate, blur card, sensitivity profiles — [safety](/architecture/safety-gating.md). Library, digest, 1-page print export — [tracker](/architecture/tracker-export.md).[^tech-concept]

# Stack + phases + success criteria

Hand-rolled RAG, user-configured Ollama, `pauli/` layout — [stack](/architecture/tech-stack.md). P0 cache, P1 chat, P2 warnings, P3 tracker; MVP gates: P0 real-topic fetch with cache hit + resolvable links, P1 `What triggers PEM?` → <150 words simplicity-appropriate 3+ Europe PMC links or explicit unknown, P2 prognosis query gates before details, P3 follow + digest + export; all verified with `pytest`.[^tech-concept]

Success criteria (technical §9, must all hold): all factual sentences cited and resolvable to cached PMCID; zero invented citations on abstention tests; warning gate appears before gated content at every slider setting; sync adds only new PMCIDs, no duplicates; readability scores meet slider targets (`textstat` Flesch-Kincaid).[^tech-concept]

[^tech-concept]: P.A.U.L.I. Technical Concept
