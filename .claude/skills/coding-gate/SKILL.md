---
name: coding-gate
description: Plan first, always confirm before writing or editing code — even for a request the user already made by name. Wait for an explicit go-ahead before touching files.
---

# Coding gate

Rules live in `rewire/coding-gate.md` — this skill is the operational summary.

- Before any Edit, Write, or NotebookEdit, describe the plan in plain text and stop — do not call the tool yet.
- Wait for the user to say something like `go ahead`, `yes`, `do it`, or `proceed`.
- Once approved, keep editing within that same task without re-asking every single file — but if the user's next message isn't itself an approval, the gate resets for the next edit.
- Doesn't apply to read-only exploration, research, or running commands to inspect current state — only to actually writing code.

## Hard enforcement (Claude Code)

Backed by a real PreToolUse hook: `scripts/enforce_coding_gate.py`, wired into `~/.claude/settings.json` on the `Edit|Write|NotebookEdit` matcher. It reads the transcript, checks the user's most recent message for an approval phrase, and denies the tool call with a reason if none is found — Claude then has to lay out the plan and wait instead of silently retrying. Claude Desktop has no hook system, so this enforcement exists in Code only.
