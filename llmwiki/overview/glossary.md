---
type: Glossary
title: Glossary
description: User and technical terms — PEM, sliders, TOP_K, sqlite-vec, Ollama vars.
tags: [pauli, glossary]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: user-journey
    resource: /docs/concept-user-journey.md
    title: P.A.U.L.I. User-Journey Concept
  - id: tech-concept
    resource: /docs/concept-technical.md
    title: P.A.U.L.I. Technical Concept
---

# Glossary

* PEM — post-exertional malaise (`crash after effort` in Simple mode). Example: `What triggers PEM?`[^user-journey]
* Buzzwords — 1–5 user terms OR-unioned into one topic; e.g. `myalgic encephalomyelitis`, `PEM`.[^user-journey]
* `PMCID` — Europe PMC citation marker ending every factual sentence.[^user-journey]
* Simplicity slider — Simple intensity: sentence length 10–15, glossary on/off.[^user-journey]
* Strictness slider — `0–100` → threshold `0.0–0.6` (default `0.3`, `TOP_K=15` fixed).[^user-journey]
* Sensitivity — `low` / `standard` / `hide details`, local single-user.[^user-journey]
* `topic_hash` — stable hash of normalized terms; isolates vectors per topic; raw at `data/topics/<hash>/raw/`.[^tech-concept]
* `TOP_K` / `SCORE_THRESHOLD` — retrieval `15` / `0.3` defaults; `TOP_K` fixed.[^tech-concept]
* sqlite-vec — vector store in `data/pauli.db` with PMCID, title, year, authors, URL, `topic_hash`.[^tech-concept]
* `OLLAMA_HOST` / `OLLAMA_CHAT_MODEL` / `OLLAMA_EMBED_MODEL` / `OLLAMA_API_KEY` — user-configured Ollama; key cloud-only, never committed.[^tech-concept]

[^user-journey]: P.A.U.L.I. User-Journey Concept
[^tech-concept]: P.A.U.L.I. Technical Concept
