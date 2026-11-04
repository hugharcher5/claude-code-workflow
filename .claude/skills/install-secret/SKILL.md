---
name: install-secret
description: Install a secret into the current PROJECT's .env via scripts/set_secret.sh — silent prompt, never echoed, never journaled, never stored in this kit. Code only.
---

# Safe secret installation

Secrets belong to coding projects, not this kit.

- Every project keeps its own git-ignored `.env`; commit only `.env.example` with variable names.
- To set one: `scripts/set_secret.sh VAR_NAME [path/to/.env]`, run from the target project (Claude Code only — it refuses to run against this kit's own `.env`).
- The script prompts silently (hidden input), writes only `NAME=value`, sets file mode 600, and warns if the `.env` isn't git-ignored. It never echoes, logs, or journals the value, and this skill must not either.
- If a secret is ever pasted into any chat (Code or Desktop), treat it as exposed and rotate it immediately — don't just delete the message.
- A future project needing its own database (e.g. Supabase) configures it inside that project, in that project's `.env`, with a project-local skill/router — never in this kit's global memory.

Claude Desktop cannot run this script. It should name the required variable and point the user to Claude Code or a local editor — never encourage pasting a secret into Desktop chat.
