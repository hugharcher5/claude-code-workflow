---
name: model-router
description: Default to Sonnet 5. For genuinely hard architecture, security, high-stakes decisions, stubborn multi-system debugging, large builds, or a courtroom Judge verdict, auto-delegate to an Opus 5 subagent — Code cannot switch its own running model, so delegation is how the upgrade actually happens.
---

# Model recommendation

Default model: Sonnet 5. Use it for routine edits, formatting, short research, ordinary notes, and simple code without comment.

Auto-delegate to an Opus 5 subagent (Agent tool, `model: "opus"`), without asking first, for:

- difficult architecture with meaningful trade-offs
- high-stakes decisions
- security or privacy design
- stubborn, multi-system debugging
- large builds requiring long-horizon reasoning
- a courtroom Judge verdict, when the decision warrants it (the courtroom skill already spawns its own real sub-agents)

Claude Code cannot switch its own running model mid-session — only the user can, via `/model`. So the mechanism here is delegation, not a self-switch: hand the qualifying work to a subagent running Opus 5, brief it with full context per the Agent tool's guidance, and report back what it found or built. Never claim to "now be running Opus" in the main thread.

If the work genuinely can't be delegated (it has to happen turn-by-turn in the primary conversation, not as a self-contained task), fall back to the old behavior: say `I would use Opus 5 for this`, one plain-language sentence why, and wait for the user to `/model` — once per task, not every turn.

If Opus 5 is unavailable on the account, say so and continue with the best available model.
