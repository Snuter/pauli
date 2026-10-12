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

* PEM — post-exertional malaise (`crash after effort` at simpler slider settings). Example: `What triggers PEM?`[^user-journey]
* Buzzwords — replaced by AI-extracted transient search terms from question + history (no cap, e.g. `myalgic encephalomyelitis`, `PEM`); terms are NOT persisted, they only drive Europe PMC lookup with PMCID-dedup against the growing vector DB.[^user-journey]
* `PMCID` — Europe PMC citation marker ending every factual sentence.[^user-journey]
* Simplicity slider — wording intensity 10–15 (default 12): sentence length, glossary on/off.[^user-journey]
* Strictness slider — `0–100` → `threshold = strictness/100*0.6` linear, cosine via sqlite-vec (default `0.3`, `TOP_K=15` fixed).[^user-journey]
* Sensitivity — `low` / `standard` / `hide details`, local single-user.[^user-journey]
* `topic_hash` — DROPPED 2026-10-12 (was stable hash for raw dirs; replaced by single shared `data/raw/<PMCID>.*`, global corpus).[^tech-concept]
* `TOP_K` / `SCORE_THRESHOLD` — retrieval `15` / `0.3` defaults; `TOP_K` fixed.[^tech-concept]
* sqlite-vec — vector store in `data/pauli.db` with PMCID, title, year, authors, URL (+ optional `topic_hash` provenance); retrieval is global, no `topic_hash` filter.[^tech-concept]
* `OLLAMA_HOST` / `OLLAMA_CHAT_MODEL` / `OLLAMA_EMBED_MODEL` / `OLLAMA_API_KEY` — user-configured Ollama; key cloud-only, never committed.[^tech-concept]

[^user-journey]: P.A.U.L.I. User-Journey Concept
[^tech-concept]: P.A.U.L.I. Technical Concept
