# Architecture

* [Data Pipeline](data-pipeline.md) - Transient terms, ID-first dedup, fast-slice + backfill, 512/50 chunks, global corpus.
* [RAG Chat](rag-chat.md) - Rewrite-retrieve-generate with code citation/abstain gates.
* [Language Modes](language-modes.md) - Simplicity-slider-only wording, textstat.
* [Safety Gating](safety-gating.md) - 6 categories, LLM GATE tags, blur card, sensitivity, logging.
* [Tracker Export](tracker-export.md) - Scheduled checks, email digest, auto-persisted sessions, all-Q condensed 1-page print HTML.
* [Tech Stack](tech-stack.md) - FastAPI/HTMX, sqlite-vec global, hand-rolled RAG, Ollama config, layout.
* [Web API](web-api.md) - Draft HTMX endpoint table replicating mockup IDs (needs approval).
* [Testing Strategy](testing.md) - pytest unit/integration + python-playwright UI, layout, commands.
