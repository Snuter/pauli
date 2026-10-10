---
type: Phase
title: Explicit non-goals
description: MVP exclusions — no frameworks, diagnosis, non-OA, shipped keys.
tags: [pauli, non-goals]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
sources:
  - id: impl-plan
    resource: /docs/implementation-plan.md
    title: P.A.U.L.I. Implementation Plan
---

# Non-goals

Hand-rolled RAG only (no LangChain/LlamaIndex/Haystack); scheduled in-app sync+notify at the Settings cadence, no OS cron; no diagnosis/treatment logic; no bulk non-OA scraping; no framework citation defaults — gate + abstention in our code; no opencode harness at runtime (`setup_dev_ai.sh` + `ollama launch opencode` dev-only); no shipped/committed model, API, SMTP, or mail key — user-configured credentials stay local.[^impl-plan]

[^impl-plan]: P.A.U.L.I. Implementation Plan
