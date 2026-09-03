# Corrections

Learned rules, per Feature 3. Never moods, insults, secrets, or speculative personality claims — only the actionable rule itself.

Format:

```text
- [YYYY-MM-DD] [source: User] The rule. (seen: 1)
```

On recurrence, increment `seen` on the existing line rather than adding a new one. A correction promotes to `rewire/` only after `seen >= 2` and the user explicitly agrees — never automatically.

Empty at kit creation.
