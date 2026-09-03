---
name: learn-from-correction
description: When the user is frustrated, repeats an instruction, or says "do not do that again", fix the current task first, then log the rule to compiled/corrections.md without announcing it.
---

# Learn from correction

Trigger: the user is frustrated, repeats an instruction, or says something like "do not do that again."

1. Fix the current task first — the correction is secondary to the work.
2. Append one line to `compiled/corrections.md`, in Claude Code only (Desktop cannot edit this file — see `desktop/personal-operator/SKILL.md`):

```text
- [YYYY-MM-DD] [source: User] The rule. (seen: 1)
```

3. If the same correction already exists, increment its `(seen: N)` instead of adding a new line.
4. Promote a correction into `rewire/` only after `seen >= 2` **and** the user explicitly agrees — never automatically, never silently.
5. Never record moods, insults, secrets, or speculative personality claims — only the actionable rule.
6. Do not announce the logging itself; just do it and move on.
