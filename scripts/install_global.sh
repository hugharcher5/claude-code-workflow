#!/usr/bin/env bash
# Global Claude Code installer (Feature: "Global Claude Code use").
# Writes ~/.claude/CLAUDE.md (short, always-on rules + path to this kit)
# and copies .claude/skills/* into ~/.claude/skills/ as real copies, not
# symlinks, so the global install survives this repo moving or being
# temporarily unavailable.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GLOBAL_DIR="$HOME/.claude"
GLOBAL_CLAUDE_MD="$GLOBAL_DIR/CLAUDE.md"
GLOBAL_SKILLS="$GLOBAL_DIR/skills"

mkdir -p "$GLOBAL_SKILLS"

# Personal memory lives in compiled/, which is git-ignored. On a fresh clone,
# seed it from the blank templates; never overwrite existing personal files.
if [[ ! -d "$REPO_DIR/compiled" ]]; then
  cp -r "$REPO_DIR/templates/compiled" "$REPO_DIR/compiled"
  echo "Created compiled/ from templates/compiled/"
fi

if [[ -f "$GLOBAL_CLAUDE_MD" ]]; then
  BACKUP="$GLOBAL_CLAUDE_MD.bak.$(date +%Y%m%d%H%M%S)"
  cp "$GLOBAL_CLAUDE_MD" "$BACKUP"
  echo "Backed up existing $GLOBAL_CLAUDE_MD to $BACKUP"
fi

cat > "$GLOBAL_CLAUDE_MD" <<EOF
# Personal operator

My personal kit is at \`${REPO_DIR}\`.

- Aim for about 60 words (85 is the hard cap) unless I ask for detail or more words (\`in detail\`,
  \`use detail\`, \`do this in detail\`, or more words). This applies in plain
  terminal conversation too, not just task work.
- Keep sources privately; show them only when I ask (\`sources\`,
  \`show sources\`, \`where did that come from\`).
- Record explicit corrections in the kit without announcing it
  (compiled/corrections.md), and increment \`seen\` on repeats.
- For old personal work, read the kit journal and memory index first
  (compiled/journal.md, compiled/MEMORY.md).
- Use Sonnet 5 normally. For genuinely difficult reasoning, architecture,
  security, or a large build, auto-delegate to an Opus 5 subagent (Code
  can't switch its own running model, so a subagent is how the upgrade
  happens) (see .claude/skills/model-router/).
- Before frontend/design work, load ui-ux-pro-max. For user-facing prose,
  apply humanizer, still inside the word cap unless released.
- Before spend, hiring, firing, new product, or keep/kill decisions, offer
  courtroom mode once; do not start until I say yes.
- When a project needs external data, check the public-apis list first
  (see .claude/skills/public-apis/).
- Project-specific CLAUDE.md instructions override these general
  preferences when they concern that project's code or commands.
EOF
echo "Wrote $GLOBAL_CLAUDE_MD"

for skill_dir in "$REPO_DIR"/.claude/skills/*/; do
  name="$(basename "$skill_dir")"
  rm -rf "${GLOBAL_SKILLS:?}/${name}"
  cp -r "$skill_dir" "$GLOBAL_SKILLS/$name"
  echo "Installed skill: $name"
done

echo "Done. Real copies installed under $GLOBAL_SKILLS — re-run this script after updating the kit to sync changes."
