# Personal Claude Kit

A portable personal kit for Claude Code and Claude Desktop: one voice, one memory, one set of rules, used across every unrelated project. It carries no employer data, no employer keys, and no project-specific secrets.

## What this is

Eleven always-on behaviours, implemented once here and reused in every project:

1. **75-word voice.** Replies stay short and plain unless you ask for detail, enforced by a hook rather than a polite request.
2. **Plan-first coding gate.** Claude lays out its plan and waits for a go-ahead before editing files, also enforced by a hook.
3. **Reviewed memory compiler.** Turns raw exports and the journal into candidate memory that you accept as a diff before it's trusted.
4. **Memory lint.** Checks compiled memory for broken links, secrets and junk before anything relies on it.
5. **Learning from corrections.** When you correct Claude, the rule is logged quietly and counted, so repeats are caught.
6. **Sources on request.** Claude keeps a private source list and shows it only when you ask.
7. **Safe secret handling.** A silent-prompt script installs API keys into a project's `.env` without echoing, logging or storing them here.
8. **UI/UX Pro Max.** A searchable design library (styles, palettes, fonts, UX rules) loaded before any frontend work.
9. **Humanizer.** Rewrites user-facing text to remove the usual signs of AI writing.
10. **Courtroom decision mode.** For spend, hiring or keep/kill decisions, four isolated sub-agents argue it out: Believer, Sceptic, Financial and Judge.
11. **Model routing.** Everyday work runs on Sonnet; hard architecture, security or large builds get handed to an Opus sub-agent.

There is also a reduced **Claude Desktop companion skill** that brings the same voice and decision habits to Claude Desktop, and routes anything needing local files back to Claude Code.

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

## Credits

UI/UX Pro Max is by Next Level Builder and Humanizer is by Siqi Chen. Both are included unmodified under their licences (see the `LICENSE` file in each skill folder).
