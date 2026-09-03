#!/usr/bin/env python3
"""Stop hook: hard-enforces the 75-word voice cap (Feature 1, rewire/voice.md).

Reads the Stop hook's JSON on stdin, inspects the session transcript, and
blocks the turn (feeding Claude an instruction to rewrite shorter) when the
cap applies and was not honored. Never blocks the same turn twice.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WORD_CAP = 75

RELEASE_RE = re.compile(
    r"\b(in detail|use detail|do this in detail|more detail|more words|"
    r"longer answer|go into detail|explain further|no word limit|"
    r"\d+\s*words?)\b",
    re.IGNORECASE,
)
COURTROOM_RE = re.compile(r"\bcourtroom\b", re.IGNORECASE)
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


def last_message_text(entries: list[dict], role: str) -> str:
    for entry in reversed(entries):
        if entry.get("type") != role:
            continue
        blocks = text_blocks(entry)
        if blocks:
            return "\n".join(blocks)
    return ""


def strip_non_prose(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    return text


def word_count(text: str) -> int:
    return len(strip_non_prose(text).split())


def recent_mentions_courtroom(entries: list[dict], lookback: int = 6) -> bool:
    for entry in entries[-lookback:]:
        for block in text_blocks(entry):
            if COURTROOM_RE.search(block):
                return True
    return False


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}

    if payload.get("stop_hook_active"):
        return 0  # already retried once this turn - never loop

    transcript_path = payload.get("transcript_path")
    if not transcript_path:
        return 0

    entries = load_transcript(transcript_path)
    if not entries:
        return 0

    assistant_text = last_message_text(entries, "assistant")
    if not assistant_text.strip():
        return 0  # pure tool-call turn, nothing to check

    user_text = SYSTEM_REMINDER_RE.sub("", last_message_text(entries, "user"))

    if RELEASE_RE.search(user_text):
        return 0
    if recent_mentions_courtroom(entries):
        return 0

    count = word_count(assistant_text)
    if count <= WORD_CAP:
        return 0

    print(json.dumps({
        "decision": "block",
        "reason": (
            f"Your last response was {count} words, over the 75-word voice cap "
            "(rewire/voice.md). Rewrite it under 75 words - finish the thought, "
            "don't cut a sentence short, just say less. Only skip this if the "
            "user actually asked for detail or more words."
        ),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
