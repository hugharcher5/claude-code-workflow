---
name: memory-compiler
description: Run the personal memory compiler (scripts/compile_memory.py) to turn raw/ exports and the journal into reviewed candidate memory under compiled/. Code only — writes only to compiled/, never trusted until diffed, linted, and accepted.
---

# Memory compiler

Two speeds:

1. **Immediate journal** — after a task ships, dies, or is deliberately parked, append one dated, sourced line to `compiled/journal.md`:
   `- [YYYY-MM-DD] [source: Code session] What happened.`
2. **Dream/compile** — run `python3 scripts/compile_memory.py` (Claude Code only) to turn new `raw/` material plus the journal into candidates. Requires a personal `ANTHROPIC_API_KEY` in `.env` (separate from any Claude subscription; see `.env.example`).

Contract, enforced by the script itself:

- Only two source formats are accepted — Claude.ai conversation exports and Claude Code session transcripts. Anything else is skipped, never guessed at.
- Writes only under `compiled/`. Never touches `rewire/`.
- Every candidate carries a source reference.
- Secret-shaped content is redacted before it's sent, and any candidate that still looks secret-shaped is dropped, not written.
- Always prints a diff first. Without `--apply` it's a dry run — nothing is written.
- After `--apply`, run `scripts/lint_memory.py` (or the `lint-memory` skill) before treating anything as trusted. The user must still review and accept the diff.

Claude Code's built-in auto-memory can stay enabled alongside this — it's convenience, not the source of truth. This compiler is the reviewed, portable layer.
