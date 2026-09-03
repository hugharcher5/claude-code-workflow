#!/usr/bin/env python3
"""Personal memory compiler (Feature 2).

Turns raw/ exports plus compiled/journal.md into candidate additions
under compiled/. Never touches rewire/. Always shows a diff. Never
writes to disk unless run with --apply, and even then the result stays
untrusted until scripts/lint_memory.py passes and the user reviews it.

Adapters exist for two known formats only:
  - claude_export   : Claude.ai conversation export JSON
  - claude_code     : Claude Code session transcript JSONL
Any other raw/ file is skipped, never guessed at.

Provider/model are configurable via .env (ANTHROPIC_API_KEY, COMPILE_MODEL).
No employer key is hardcoded. Uses only the stdlib (urllib) so this script
runs without installing the anthropic SDK.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_memory import SECRET_PATTERNS  # reuse the same secret detector

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "raw"
COMPILED = REPO / "compiled"
JOURNAL = COMPILED / "journal.md"
STATE_FILE = RAW / ".compile_state.json"  # local bookkeeping only; raw/ is git-ignored
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"

SYSTEM_PROMPT = """You compile personal memory for one person from their own \
raw transcripts and journal notes. Extract only durable, concrete facts about \
people, projects, and decisions that are actually stated in the source text.

Rules:
- Never invent or infer beyond what is written. If unsure, omit it.
- Never include secrets, API keys, passwords, tokens, or full credentials.
- Never include private third-party data (other people's personal details \
they wouldn't expect recorded).
- Attach a short source reference to every claim (file name and rough \
location, e.g. "raw/export.json convo 3").
- Output strict JSON only, matching this shape, nothing else:
{"people": [{"slug": "kebab-name", "name": "...", "fact": "...", "source": "..."}],
 "projects": [{"slug": "kebab-name", "fact": "...", "source": "..."}],
 "decisions": [{"slug": "kebab-name", "fact": "...", "source": "..."}]}
Use [] for any category with nothing durable to add.
"""


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    env_path = REPO / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"processed_raw": [], "journal_watermark": ""}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def detect_format(path: Path) -> str | None:
    try:
        if path.suffix == ".jsonl":
            first = path.read_text(encoding="utf-8").splitlines()[0]
            obj = json.loads(first)
            if "type" in obj and "message" in obj:
                return "claude_code"
            return None
        if path.suffix == ".json":
            obj = json.loads(path.read_text(encoding="utf-8"))
            data = obj[0] if isinstance(obj, list) and obj else obj
            if isinstance(data, dict) and "chat_messages" in data:
                return "claude_export"
            return None
    except (json.JSONDecodeError, IndexError, UnicodeDecodeError):
        return None
    return None


def adapt_claude_export(path: Path) -> str:
    obj = json.loads(path.read_text(encoding="utf-8"))
    convos = obj if isinstance(obj, list) else [obj]
    chunks = []
    for i, convo in enumerate(convos):
        for msg in convo.get("chat_messages", []):
            sender = msg.get("sender", "?")
            text = msg.get("text", "")
            chunks.append(f"[convo {i} · {sender}] {text}")
    return "\n".join(chunks)


def adapt_claude_code(path: Path) -> str:
    chunks = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        role = obj.get("type", "?")
        content = obj.get("message", {}).get("content", "")
        if isinstance(content, list):
            content = " ".join(
                part.get("text", "") for part in content if isinstance(part, dict)
            )
        chunks.append(f"[{role}] {content}")
    return "\n".join(chunks)


ADAPTERS = {"claude_export": adapt_claude_export, "claude_code": adapt_claude_code}


def redact_secrets(text: str) -> str:
    for _, pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text


def gather_source_material(state: dict) -> tuple[str, list[str]]:
    parts: list[str] = []
    touched: list[str] = []
    for path in sorted(RAW.glob("*")):
        if path.name in (".gitkeep", ".compile_state.json"):
            continue
        rel = str(path.relative_to(REPO))
        if rel in state["processed_raw"]:
            continue
        fmt = detect_format(path)
        if fmt is None:
            print(f"skip (unknown format, refusing to guess): {rel}")
            continue
        text = redact_secrets(ADAPTERS[fmt](path))
        parts.append(f"=== {rel} ({fmt}) ===\n{text}")
        touched.append(rel)

    if JOURNAL.exists():
        journal_text = JOURNAL.read_text(encoding="utf-8")
        new_lines = [
            line for line in journal_text.splitlines()
            if line > state.get("journal_watermark", "") or not state.get("journal_watermark")
        ]
        if state.get("journal_watermark"):
            # keep only lines lexically after the watermark line (dated lines sort chronologically)
            new_lines = [l for l in journal_text.splitlines() if l > state["journal_watermark"]]
        if new_lines:
            parts.append("=== compiled/journal.md (new entries) ===\n" + "\n".join(new_lines))

    return "\n\n".join(parts), touched


def call_anthropic(api_key: str, model: str, source_material: str) -> dict:
    body = json.dumps({
        "model": model,
        "max_tokens": 4096,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": source_material}],
    }).encode("utf-8")
    req = urllib.request.Request(
        ANTHROPIC_URL,
        data=body,
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        payload = json.loads(resp.read())
    text = "".join(block.get("text", "") for block in payload.get("content", []))
    return json.loads(text)


def candidate_has_secret(candidate: dict) -> bool:
    blob = json.dumps(candidate)
    return any(pattern.search(blob) for _, pattern in SECRET_PATTERNS)


def render_entry(item: dict, category: str) -> str:
    today = datetime.now(timezone.utc).date().isoformat()
    return (
        f"- [{today}] [source: {item['source']}] {item['fact']}\n"
    )


def build_diffs(candidates: dict) -> dict[Path, tuple[str, str]]:
    diffs: dict[Path, tuple[str, str]] = {}
    for category in ("people", "projects", "decisions"):
        for item in candidates.get(category, []):
            if candidate_has_secret(item):
                print(f"dropped candidate (secret-shaped content): {item.get('slug')}")
                continue
            target = COMPILED / category / f"{item['slug']}.md"
            before = target.read_text(encoding="utf-8") if target.exists() else ""
            addition = render_entry(item, category)
            after = before + (("\n" if before and not before.endswith("\n") else "") + addition)
            diffs[target] = (before, after)
    return diffs


def print_diff(path: Path, before: str, after: str) -> None:
    rel = path.relative_to(REPO)
    diff = difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=f"a/{rel}",
        tofile=f"b/{rel}",
    )
    sys.stdout.writelines(diff)
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write candidates to compiled/ (default: dry-run diff only)")
    parser.add_argument("--model", default=None, help="override COMPILE_MODEL")
    args = parser.parse_args()

    env = load_env()
    api_key = env.get("ANTHROPIC_API_KEY") or ""
    model = args.model or env.get("COMPILE_MODEL", "claude-sonnet-5")
    if not api_key:
        print("No ANTHROPIC_API_KEY set (see .env.example). Set a personal key — API billing is separate from a Claude subscription.")
        return 1

    state = load_state()
    source_material, touched = gather_source_material(state)
    if not source_material.strip():
        print("Nothing new in raw/ or compiled/journal.md to compile.")
        return 0

    try:
        candidates = call_anthropic(api_key, model, source_material)
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"compile failed: {e}")
        return 1

    diffs = build_diffs(candidates)
    if not diffs:
        print("No durable candidates extracted.")
        return 0

    for path, (before, after) in diffs.items():
        print_diff(path, before, after)

    if not args.apply:
        print("Dry run only — nothing written. Review the diff above, then re-run with --apply.")
        return 0

    for path, (_before, after) in diffs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(after, encoding="utf-8")

    state["processed_raw"] = sorted(set(state["processed_raw"]) | set(touched))
    journal_lines = JOURNAL.read_text(encoding="utf-8").splitlines() if JOURNAL.exists() else []
    if journal_lines:
        state["journal_watermark"] = journal_lines[-1]
    save_state(state)

    print("Written to compiled/. Still untrusted — run scripts/lint_memory.py, then review before relying on it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
