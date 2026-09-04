# Personal Claude Kit — repo instructions

This file governs work done *inside this repo* (maintaining the kit itself). The short always-on file loaded into every other project is `~/.claude/CLAUDE.md`, installed by `scripts/install_global.sh` — see `README.md`.

## Rules for editing this repo

- `rewire/` is deliberate and manual. Never write to it from a script or on the compiler's own initiative — only when the user directly asks, and only after a correction has been seen twice (see `compiled/corrections.md`).
- `compiled/` is written only as a reviewed diff. Nothing here is trusted until the user accepts the diff and `scripts/lint_memory.py` passes.
- `raw/` is git-ignored and never rewritten — treat it as read-only source material.
- Never put employer data, employer API keys, work Supabase config, Blackkite/OpenClaw content, or company memory in this repo. This kit must work identically dropped into any unrelated project.
- Never put project-specific secrets or database credentials here. Those belong in that project's own `.env` and project-local skill/router — see `compiled/decisions/` only if a boundary decision about this needs recording.
- Vendor skills (`.claude/skills/humanizer/`, `.claude/skills/ui-ux-pro-max/`) are copied in unmodified from upstream. Personal routing rules for them live in `.claude/skills/model-router/` and `~/.claude/CLAUDE.md`, not inside the vendor files, so upstream updates never conflict with personal rules.

## The eleven features

1. 75-word voice — `rewire/voice.md`, `.claude/skills/brevity-check/`
2. Memory compiler — `scripts/compile_memory.py`, `.claude/skills/memory-compiler/`
3. Learn from corrections — `compiled/corrections.md`, `.claude/skills/learn-from-correction/`
4. Sources on request — `rewire/sources.md`, `.claude/skills/sources-on-request/`
5. Memory lint — `scripts/lint_memory.py`, `.claude/skills/lint-memory/`
6. Safe secret installation — `scripts/set_secret.sh`, `.claude/skills/install-secret/`
7. UI/UX Pro Max — `.claude/skills/ui-ux-pro-max/` (vendor, unmodified)
8. Humanizer — `.claude/skills/humanizer/` (vendor, unmodified)
9. Courtroom — `.claude/skills/courtroom-mode/`, records under `compiled/courtroom/`
10. Model recommendation — `.claude/skills/model-router/`
11. Coding gate — `rewire/coding-gate.md`, `.claude/skills/coding-gate/`, hard-enforced via `scripts/enforce_coding_gate.py`

Supabase and Hermes are intentionally omitted from this kit.
