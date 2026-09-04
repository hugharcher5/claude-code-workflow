# Personal Claude Kit

A portable personal kit for Claude Code and Claude Desktop: one voice, one memory, one set of rules, used across every unrelated project. It carries no employer data, no employer keys, and no project-specific secrets.

## What this is

Eleven always-on behaviors — 75-word voice, a reviewed memory compiler, learning from corrections, sources on request, memory lint, safe secret handling, UI/UX Pro Max, Humanizer, courtroom decision mode, Sonnet/Opus model routing, and a plan-first coding gate — implemented once here and reused everywhere.

## The split

- **Claude Code** (this repo, cloned locally) is canonical: it edits memory, runs lint, installs secrets, and spawns real isolated courtroom sub-agents.
- **Claude Desktop** gets a reduced skill (`desktop/personal-operator/`) for reading, discussion, and decisions. It never claims to edit local memory, run local lint, install a local secret, or spawn isolated courtroom agents — those route back to Claude Code.

## Layout

- `rewire/` — deliberate personal rules. Never edited by any script or compiler, only by hand.
- `compiled/` — reviewed facts: memory index, journal, corrections, people, projects, decisions, courtroom records. Written only via reviewed diffs.
- `raw/` — imported exports/transcripts, git-ignored, never rewritten.
- `scripts/` — `lint_memory.py`, `compile_memory.py`, `set_secret.sh`, `install_global.sh`.
- `.claude/skills/` — personal wrapper skills, plus genuine unmodified copies of the upstream UI/UX Pro Max and Humanizer skills.
- `desktop/personal-operator/` — the packaged Claude Desktop skill.

## Install (Claude Code, global)

```bash
scripts/install_global.sh
```

Writes `~/.claude/CLAUDE.md` (short, always-on rules + path to this kit) and copies `.claude/skills/*` into `~/.claude/skills/` as real copies, not symlinks. Each project keeps its own `CLAUDE.md`, code, and `.env` — this kit stays separate.

## Install (Claude Desktop)

Zip `desktop/personal-operator/` and upload under **Customize → Skills**, enabled on the personal account. Periodically upload a reviewed `compiled/MEMORY.md` to the relevant Claude Project when Desktop needs that context — Desktop's own account memory is not the same as this kit's reviewed memory.

## Secrets

Never stored here. See `.env.example` and `scripts/set_secret.sh`. Project databases (e.g. a future Supabase project) are configured per-project, not in this kit.
