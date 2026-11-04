---
name: lint-memory
description: Run scripts/lint_memory.py after every memory compile and before trusting generated memory. Code only — canonical here; Desktop must not claim to have run local lint without a real local tool.
---

# Memory lint

Run `python3 scripts/lint_memory.py` (Claude Code only). It fails (exit 1) on:

- secret-shaped values anywhere in `rewire/` or `compiled/`
- compiler output that leaked into `rewire/` (rewire/ is manual-only)
- journal or correction lines missing a date or a source
- broken links from `compiled/MEMORY.md`
- corrections older than 30 days that were never promoted or dismissed (`seen < 2`)
- rewire/ lines that look contradictory (Always/Never pairs sharing wording) — a heuristic, not proof; read the flagged lines yourself

Always run this after `memory-compiler`, and before treating any compiled memory as trustworthy. `scripts/test_lint_memory.py` covers the linter's own behavior — run it after editing `lint_memory.py`.

Claude Desktop has no local tool to run this. It must say so plainly rather than claim a lint pass — see `desktop/personal-operator/SKILL.md`.
