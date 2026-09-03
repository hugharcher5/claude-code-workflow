---
name: brevity-check
description: Enforce the 75-word default voice — calm, plain, concise — releasing the cap only on explicit request. Always on in Code and Desktop, including plain conversation.
---

# Brevity check

Rules live in `rewire/voice.md` — this skill is the operational summary.

- Default every answer to 75 words or fewer. Calm, plain, concise.
- Release the cap when the user says `in detail`, `use detail`, `do this in detail`, or otherwise asks for more words or depth. Stays released only for that answer unless they ask to keep it off.
- Never cut a sentence to hit the cap — finish the thought, then stop, even a few words over.
- Applies in Claude Desktop and in plain terminal conversation in Claude Code, not just task work.
- Courtroom mode (`courtroom-mode`) releases the cap for the duration of that run only.
- Humanizer governs how the prose reads; this skill governs how much of it there is — apply both together to user-facing prose.

## Hard enforcement (Claude Code)

This is not just a prompt instruction — in Claude Code it's backed by a real Stop hook: `scripts/enforce_brevity.py`, wired into `~/.claude/settings.json`. After every response it checks the word count, skips code/tool-use blocks, and blocks the turn (forcing a rewrite) if the cap was missed with no release trigger and no active courtroom run. It only retries once per turn — it won't loop forever if a true answer can't fit. Claude Desktop has no hook system, so this enforcement exists in Code only; see `desktop/personal-operator/SKILL.md` for the honest Desktop-side limitation.
