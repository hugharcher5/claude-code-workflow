---
name: sources-on-request
description: Keep a private source ledger while answering; reveal it only when the user asks with "sources", "show sources", or "where did that come from".
---

# Sources on request

Rules live in `rewire/sources.md` — this skill is the operational summary.

- While answering, silently track where each claim came from: the user's own words, a file, or the web.
- Do not print the ledger unprompted.
- Reveal it only on `sources`, `show sources`, or `where did that come from`, in this format:

```text
Sources:
- You: "…" (date/chat)
- File: path
- Web: URL — trust: high/medium/low — why
```

- If a claim has no real source, say `Unsourced — treat as a guess.` Never present a guess as sourced.
