---
type: Schema
title: LLMWIKI Schema + Workflows
description: Conventions and ingest/query/lint workflows for the P.A.U.L.I. wiki.
tags: [pauli, llmwiki, schema]
status: stable
generated: {by: agent/opencode, at: 2026-10-10T00:00:00Z}
---

# Schema

Three layers (Karpathy): `docs/` = immutable raw sources (never edited by wiki ops); `llmwiki/` = LLM-owned wiki; this file = schema. After all `docs/` sources are ingested (log confirms), `docs/` may be deleted — `llmwiki/sources/*-summary.md` then become canonical, with git history as provenance.

# Conventions

* One concept per file. Path is identity (Concept ID = path without `.md`).
* Frontmatter: `type` REQUIRED. Recommended `title`, `description`, `tags`, `status`. Provenance via `sources[] {id, resource}`. Trust via `generated: {by, at}`, `verified: [{by, at}]`.
* Actors: `agent/opencode`, `human:<id>`, `process:<id>`.
* Per-claim attribution: footnotes joining to `sources` entry ids.
* Links: absolute bundle-relative `/overview/vision.md` preferred; relationship conveyed by surrounding prose.
* Reserved: `index.md` (no frontmatter except root `okf_version`), `log.md` (`## YYYY-MM-DD`, newest first).
* `references/` mirrors external material. No `Attested Computation` in this bundle.
* Types used here: `Overview|Concept|Architecture|Workflow|Phase|Glossary|Schema|Reference`.

# Workflows

## Ingest (on user command only)

1. Read one `docs/` source. Discuss takeaways if requested.
2. Write/update `sources/<name>-summary.md`, then touch affected concepts (5-10 pages).
3. Update subdir + root `index.md` descriptions. Append `log.md` entry. Keep `status: draft` until reviewed.

## Query

1. Read `llmwiki/index.md`, drill into relevant pages. Synthesize with citations to wiki pages + `sources`.
2. File valuable answers back as new pages under appropriate section.

## Lint

Check: missing `type`, broken links, orphans with no inbound links, contradictions between pages, stale `generated.at`, missing `sources` on factual claims.
