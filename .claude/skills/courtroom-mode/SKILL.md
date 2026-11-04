---
name: courtroom-mode
description: For spend, hiring, firing, new-product, or keep/kill decisions, offer courtroom mode once. Claude Code runs four real isolated sub-agents (Believer, Sceptic, Financial, Judge); Claude Desktop must refuse to fake it.
---

# Courtroom

Trigger: a spend, hiring, firing, new-product, or keep/kill decision. Ask once, exactly:

`Would you like to use courtroom for this decision?`

Do not start until the answer is yes. The 75-word cap is released for the whole run.

## Claude Code (real isolated sub-agents)

Spawn three agents in parallel via the Agent tool, each with only the decision context — not each other's output:

1. **Believer** — the case for, only.
2. **Sceptic** — the case against and failure modes.
3. **Financial** — money, time, runway, replacement cost; every number labeled by source.

Wait for all three to return. Only then spawn a **Judge** agent, giving it exclusively the three completed briefs (not the original context), for the recommendation.

Save the four agent run/session identifiers under `compiled/courtroom/` as proof of isolation, e.g. `compiled/courtroom/YYYY-MM-DD-<slug>.md` listing each role and its run id.

## Claude Desktop (cannot prove isolation)

Never simulate four agents with four headings in one response — that is not isolation. Say plainly:

`A real courtroom needs Claude Code for isolated sub-agents.`

The user may run it in Code instead. Manual separate Desktop chats are acceptable only if described clearly as manual isolation, not as this skill's automated run.
