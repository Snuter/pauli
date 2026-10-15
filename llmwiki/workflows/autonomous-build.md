---
type: Workflow
title: Autonomous build loop
description: Implement implementation ledger tasks one by one autonomously — test first (TDD), implement, run tests, commit if green, next task.
tags: [pauli, workflow, autonomous]
status: draft
generated: {by: agent/opencode, at: 2026-10-15T00:00:00Z}
---

# Autonomous build loop

Executes the task ledger in `/implementation/` one task at a time, in order `S -> P0 -> P1 -> P2 -> P3`. Each ledger bullet is `ID -> owner file(s) -> TDD test -> Verify: exact pytest command -> Forbidden: negative check`.

1. Pick next task — the next undone ID from `phase-S.md` through `phase-P3.md`. State ID + owner files + exact `Verify` command + `Forbidden` line before touching code.
2. Test first (TDD) — write the named test before the implementation. Run it, confirm RED (fails as expected). Never implement before the failing test exists.
3. Implement — minimal code that makes the test pass. Surgical changes only: touch what the task requires, match existing style, no speculative features or adjacent refactors.
4. Test RUN — run the named test file, then the full suite (`poetry run pytest -q`). Both must be green. Loop on implement + test until green; do not start the next task while red.
5. Commit after each task — mandatory when all green: `git add` only touched files (plus wiki touch if behavior changed per `AGENTS.md` §5). One commit per task, message `"IMPL-Agent: <ID> <short desc>"` (e.g. `"IMPL-Agent: S1 Deps in pyproject.toml"`). Do not batch tasks into one commit; do not start the next task uncommitted. If red: no commit — fix, or stop and report.
6. Next task — return to step 1.

Stop conditions: red suite that does not converge, ambiguous spec (stop and ask per `AGENTS.md` §1), or phase complete.

Related: [implementation](/implementation/), [schema](/schema.md).
