# Corrections

Learned rules, per Feature 3. Never moods, insults, secrets, or speculative personality claims — only the actionable rule itself.

Format:

```text
- [YYYY-MM-DD] [source: User] The rule. (seen: 1)
```

On recurrence, increment `seen` on the existing line rather than adding a new one. A correction promotes to `rewire/` only after `seen >= 2` and the user explicitly agrees — never automatically.

Empty at kit creation.
- [2026-09-03] [source: User] Automated rules (like the 75-word cap) must be enforced with real code (hooks) wherever the platform allows it, not left as prompt-only instructions the model can ignore; when a platform genuinely has no enforcement mechanism (e.g. Claude Desktop skills), say so plainly instead of presenting it as a guarantee. (seen: 1)
- [2026-09-03] [source: User] Don't push rotation/security nagging on low-stakes personal API keys once the user says they don't care if it leaks — flag exposure once, then drop it if waved off. (seen: 1)
