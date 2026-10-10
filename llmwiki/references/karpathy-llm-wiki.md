---
type: Reference
title: Karpathy LLM Wiki pattern
description: Persistent compounding wiki between raw sources and queries.
tags: [llmwiki, pattern]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: karpathy-gist
    resource: https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/ac46de1ad27f92b28ac95459c782c07f6b8c964a/llm-wiki.md
    title: Karpathy LLM Wiki gist
---

# Karpathy LLM Wiki

Raw sources (immutable) → wiki (LLM-owned markdown) → schema (conventions). Operations: ingest, query (file answers back), lint. Navigation via `index.md` + `log.md`. LLM does bookkeeping; human curates sources and questions.
