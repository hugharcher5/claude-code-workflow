#!/usr/bin/env python3
"""Memory lint for the personal Claude kit. Canonical in Claude Code.

Exit 0 = clean. Exit 1 = at least one failure. Run after every
compile and before trusting generated memory (see compiled/MEMORY.md).
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REWIRE = REPO / "rewire"
COMPILED = REPO / "compiled"

COMPILER_MARKER = "<!-- compiled-by: compile_memory.py -->"
ENTRY_RE = re.compile(r"^- \[(\d{4}-\d{2}-\d{2})\] \[source: ([^\]]+)\] (.+)$")
SEEN_RE = re.compile(r"\(seen:\s*(\d+)\)")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
STALE_DAYS = 30

SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Anthropic API key", re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")),
    ("OpenAI-style API key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("Slack token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        "Assigned secret-shaped value",
        re.compile(r"(?i)\b(secret|token|password|api_?key)\b\s*[:=]\s*\S{8,}"),
    ),
]


@dataclass
class Failure:
    check: str
    path: str
    detail: str


@dataclass
class LintResult:
    failures: list[Failure] = field(default_factory=list)

    def fail(self, check: str, path: str, detail: str) -> None:
        self.failures.append(Failure(check, path, detail))

    @property
    def ok(self) -> bool:
        return not self.failures


def strip_fenced_code(text: str) -> str:
    """Drop ``` fenced blocks so format examples in docs aren't linted as entries."""
    return re.sub(r"```.*?```", "", text, flags=re.S)


def all_md_files(*roots: Path) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(sorted(root.rglob("*.md")))
    return files


def check_secrets(result: LintResult) -> None:
    for path in all_md_files(REWIRE, COMPILED):
        text = path.read_text(encoding="utf-8")
        for name, pattern in SECRET_PATTERNS:
            m = pattern.search(text)
            if m:
                result.fail(
                    "secret-shaped-value",
                    str(path.relative_to(REPO)),
                    f"{name} pattern matched: {m.group(0)[:12]}…",
                )


def check_rewire_immutable(result: LintResult) -> None:
    for path in all_md_files(REWIRE):
        text = path.read_text(encoding="utf-8")
        if COMPILER_MARKER in text:
            result.fail(
                "compiler-wrote-rewire",
                str(path.relative_to(REPO)),
                "file carries the compile_memory.py marker but rewire/ is manual-only",
            )


def check_entry_format(result: LintResult, path: Path) -> None:
    if not path.exists():
        return
    raw = path.read_text(encoding="utf-8")
    stripped = strip_fenced_code(raw)
    for lineno, line in enumerate(stripped.splitlines(), start=1):
        if not line.startswith("- "):
            continue
        if not ENTRY_RE.match(line):
            result.fail(
                "missing-date-or-source",
                f"{path.relative_to(REPO)}:{lineno}",
                f"entry line does not match '- [YYYY-MM-DD] [source: X] ...': {line!r}",
            )


def check_memory_links(result: LintResult) -> None:
    path = COMPILED / "MEMORY.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for m in LINK_RE.finditer(text):
        target = m.group(1)
        if target.startswith(("http://", "https://", "#")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            result.fail(
                "broken-memory-link",
                str(path.relative_to(REPO)),
                f"link target does not exist: {target}",
            )


def check_stale_corrections(result: LintResult, today: date | None = None) -> None:
    path = COMPILED / "corrections.md"
    if not path.exists():
        return
    today = today or date.today()
    stripped = strip_fenced_code(path.read_text(encoding="utf-8"))
    for lineno, line in enumerate(stripped.splitlines(), start=1):
        m = ENTRY_RE.match(line)
        if not m:
            continue
        entry_date = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        seen_m = SEEN_RE.search(line)
        seen = int(seen_m.group(1)) if seen_m else 1
        age = (today - entry_date).days
        if age > STALE_DAYS and seen < 2:
            result.fail(
                "stale-unreviewed-correction",
                f"{path.relative_to(REPO)}:{lineno}",
                f"{age}d old, seen={seen}, never promoted or dismissed: {line!r}",
            )


_STOPWORDS = {
    "the", "a", "an", "to", "of", "in", "on", "for", "and", "or", "it",
    "this", "that", "with", "unless", "only", "when", "is", "are", "be",
}


def _keywords(line: str) -> set[str]:
    words = re.findall(r"[a-z']+", line.lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 2}


def check_contradictions(result: LintResult) -> None:
    """Best-effort heuristic: flags Always/Never (or Do/Don't) lines in rewire/
    that share substantial wording, since a real contradiction check needs
    judgment this script doesn't have. False negatives are expected; treat
    a hit as 'go read these two lines', not as proof."""
    always_lines: list[tuple[str, int, str, set[str]]] = []
    never_lines: list[tuple[str, int, str, set[str]]] = []
    for path in all_md_files(REWIRE):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            low = line.strip().lower()
            if low.startswith(("- always", "always", "- do ")):
                always_lines.append((str(path.relative_to(REPO)), lineno, line, _keywords(line)))
            elif low.startswith(("- never", "never", "- don't", "- do not")):
                never_lines.append((str(path.relative_to(REPO)), lineno, line, _keywords(line)))
    for a_path, a_no, a_line, a_kw in always_lines:
        for n_path, n_no, n_line, n_kw in never_lines:
            shared = a_kw & n_kw
            if len(shared) >= 3:
                result.fail(
                    "possible-contradiction",
                    f"{a_path}:{a_no} vs {n_path}:{n_no}",
                    f"share {sorted(shared)}: {a_line!r} / {n_line!r}",
                )


def run() -> LintResult:
    result = LintResult()
    check_secrets(result)
    check_rewire_immutable(result)
    check_entry_format(result, COMPILED / "journal.md")
    check_entry_format(result, COMPILED / "corrections.md")
    check_memory_links(result)
    check_stale_corrections(result)
    check_contradictions(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    result = run()
    if result.ok:
        print("lint_memory: clean")
        return 0
    print(f"lint_memory: {len(result.failures)} failure(s)")
    for f in result.failures:
        print(f"  [{f.check}] {f.path}: {f.detail}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
