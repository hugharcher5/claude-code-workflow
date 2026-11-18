# Personal Claude Kit

My personal AI assistant, built on Claude Code. It reads my email, keeps my to-do list in order, saves my ideas, drafts my replies and helps me make decisions. It follows one set of rules and one memory across every project I work on.

I built it because I run a day job, a startup, my own ventures and a job search at the same time, and I wanted one assistant that knows all of it without me repeating myself. The kit holds no employer data, no API keys and no project secrets, and all personal memory stays on my machine. Clone it, run the installer and it becomes yours.

## How it runs my day

**One inbox.** Every address I use forwards into a single Gmail inbox. Claude reads it through the Gmail connector. It searches by sender, date and topic, opens the threads that matter and skips receipts and promotions. When I ask "any new emails?", I get a short summary of what changed since the last check: rejections, interview invites, deadlines, security alerts, tax letters.

**Email becomes tasks.** Anything that needs action becomes a Todoist task. Claude judges how urgent each one is, sets the priority (P1 to P4), adds due dates from the email, and orders each list from most to least urgent, so I can work straight down it.

**The to-do list follows my life.** Todoist is split into my core areas: day job, startup, my own ventures, job search and life admin, with the Inbox for anything that doesn't fit. Busy areas get sections instead of more projects.

**Notion is the long-term memory.** Ideas get saved to Notion when they come up. Structured work lives there too. For example, my internship tracker records every application's status, deadlines, assessment dates and odds. When an email changes a status (a rejection, a test invite, a missed deadline), Claude updates the right row.

**Claude drafts, I send.** Replies are written as Gmail drafts in my voice. Nothing goes out until I read it and press send.

**It checks before it acts.** It plans before editing files, asks before anything public or hard to undo, and won't push personal data to a public place without asking.

## Connectors

| Connector | What it does for me |
|---|---|
| **Gmail** | Reads and searches my single inbox, summarises new mail, writes drafts for me to send. |
| **Todoist** | My to-do list. Tasks are created from emails and conversations, prioritised and ordered by urgency across my life areas. |
| **Notion** | Ideas, notes and trackers, such as the internship application database. |
| **Google Drive** | Finds and reads my documents (CVs, notes, statements) for context. |
| **Google Calendar** | Schedules and deadlines alongside tasks. |
| **Claude Docs** | Shareable living documents when something needs to be written up properly. |

## The thirteen features

These are implemented once here and used in every project.

1. **A short, plain voice (about 60 words, 85 at most).** Answers stay brief unless I ask for detail. A Stop hook enforces this: it counts the words in every reply, ignoring code and tables, and makes Claude rewrite anything over the cap. Saying "in detail" lifts the limit.
2. **Plan before code.** Claude sets out what it will change and waits for "go ahead" before editing any file. A hook enforces this too, so the assistant can't skip the step even on a request I've already made.
3. **Reviewed memory compiler.** A script turns raw chat exports and my journal into candidate memory. Nothing becomes trusted until I've seen it as a diff and accepted it, so the assistant never "remembers" something I didn't approve.
4. **Memory lint.** Before compiled memory is relied on, a linter checks it for broken links, leaked secrets and junk entries.
5. **Learning from corrections.** When I correct the assistant, it fixes the task first and then quietly logs the rule with a count. Repeated corrections stand out and can be promoted into permanent rules.
6. **Sources on request.** Claude keeps a private ledger of where each claim came from (something I said, a file or a web page, with a trust rating). It shows the ledger only when I ask, and anything unsourced is labelled a guess.
7. **Safe secret handling.** API keys go into a project's `.env` through a silent prompt. They're never echoed, logged or stored in this kit.
8. **UI/UX Pro Max.** A searchable design library (styles, palettes, font pairings, UX rules, chart types) that's loaded before any frontend work, so interfaces start from good design defaults.
9. **Humanizer.** User-facing writing is rewritten to remove the usual signs of AI text: inflated claims, filler, stock phrases, repetitive structure.
10. **Courtroom decision mode.** For decisions about spending, hiring, product or keep/kill, four isolated sub-agents argue the case. The Believer and Sceptic make opposing cases, the Financial agent runs the numbers, and the Judge sees only their briefs before ruling. Verdicts come with conditions and are saved as records.
11. **Model routing.** Everyday work runs on a fast model. Hard architecture, security, high-stakes decisions and large builds are handed automatically to a stronger model running as a sub-agent.
12. **Public APIs for data.** When a project needs data (market prices, fundamentals, macro, weather), Claude checks the [public-apis](https://github.com/public-apis/public-apis) catalogue first and prefers free or no-key APIs over scrapers or paid feeds.
13. **MarkItDown.** Before reading a PDF, Office file, web page or YouTube link, Claude converts it to Markdown with Microsoft's [markitdown](https://github.com/microsoft/markitdown), which is easier for AI to read. It runs from its own pinned install, only on files I point it at, with third-party plugins off.

There is also a reduced **Claude Desktop companion skill**. It brings the same voice and decision habits to Claude Desktop and sends anything that needs local files back to Claude Code.

## The split

- **Claude Code** (this repo, cloned locally) is the main version. It edits memory, runs lint, installs secrets and runs the real, isolated courtroom sub-agents.
- **Claude Desktop** gets a reduced skill (`desktop/personal-operator/`) for reading, discussion and decisions. It never claims to edit local memory, run local lint, install a local secret or run isolated courtroom agents. Those go back to Claude Code.

## Layout

- `rewire/`: deliberate personal rules. Never edited by any script or compiler, only by hand.
- `compiled/`: your personal memory (index, journal, corrections, people, projects, decisions, courtroom records). Git-ignored, so it never leaves your machine. Written only through reviewed diffs.
- `templates/compiled/`: the blank versions that ship with the repo. The installer copies them into `compiled/` on first run.
- `raw/`: imported exports and transcripts. Git-ignored and never rewritten.
- `scripts/`: `lint_memory.py`, `compile_memory.py`, `set_secret.sh`, `install_global.sh`, and the brevity and coding-gate hooks.
- `.claude/skills/`: personal wrapper skills, plus unmodified copies of the upstream UI/UX Pro Max and Humanizer skills.
- `desktop/personal-operator/`: the packaged Claude Desktop skill.

## Install (Claude Code, global)

```bash
scripts/install_global.sh
```

On a fresh clone this first creates `compiled/` from the blank templates. It then writes `~/.claude/CLAUDE.md` (short always-on rules plus the path to this kit) and copies `.claude/skills/*` into `~/.claude/skills/` as real copies, not symlinks. Each project keeps its own `CLAUDE.md`, code and `.env`. This kit stays separate.

## Install (Claude Desktop)

Zip `desktop/personal-operator/` and upload it under **Customize → Skills** on the personal account. When Desktop needs context, upload a reviewed `compiled/MEMORY.md` to the relevant Claude Project. Desktop's own account memory is separate from this kit's reviewed memory.

## Secrets

Never stored here. See `.env.example` and `scripts/set_secret.sh`. Project databases are configured per project, not in this kit.

## Credits

UI/UX Pro Max is by Next Level Builder and Humanizer is by Siqi Chen. Both are included unmodified under their licences (see the `LICENSE` file in each skill folder).
