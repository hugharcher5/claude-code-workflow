#!/usr/bin/env python3
"""PreToolUse hook: hard-enforces the coding gate (Feature 11, rewire/coding-gate.md).

Blocks Edit/Write/NotebookEdit unless the user's most recent message
contains an explicit go-ahead. Mirrors enforce_brevity.py's approach:
regex-gated, transcript-driven, fail-open on missing/unreadable data.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

GATED_TOOLS = {"Edit", "Write", "NotebookEdit"}

APPROVAL_RE = re.compile(
    r"\b(go ahead|go for it|approved?|proceed|do it|do that|make (the|that|those) "
    r"changes?|make it|build it|ship it|confirmed|sounds good|lgtm|correct|"
    r"yes|yep|yeah|yup|sure|ok(ay)?|please proceed|start coding|start building)\b",
    re.IGNORECASE,
)
SYSTEM_REMINDER_RE = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)


def load_transcript(path: str) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    entries = []
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def text_blocks(entry: dict) -> list[str]:
    content = entry.get("message", {}).get("content", "")
    if isinstance(content, str):
        return [content]
    if isinstance(content, list):
        return [
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        ]
    return []


def last_user_text(entries: list[dict]) -> str:
    for entry in reversed(entries):
        if entry.get("type") != "user":
            continue
        blocks = text_blocks(entry)
        if blocks:
            return "\n".join(blocks)
    return ""


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0

    if payload.get("tool_name") not in GATED_TOOLS:
        return 0

    transcript_path = payload.get("transcript_path")
    if not transcript_path:
        return 0

    entries = load_transcript(transcript_path)
    if not entries:
        return 0

    user_text = SYSTEM_REMINDER_RE.sub("", last_user_text(entries))
    if not user_text.strip():
        return 0  # nothing to check against - fail open

    if APPROVAL_RE.search(user_text):
        return 0

    deny(
        "Coding gate (rewire/coding-gate.md): no explicit go-ahead in the "
        "user's last message. Lay out the plan in plain text and wait for "
        "confirmation (e.g. 'go ahead', 'yes', 'do it') before editing files."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
