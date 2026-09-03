#!/usr/bin/env python3
"""Tests for lint_memory.py. Run: python3 scripts/test_lint_memory.py"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_memory as lm  # noqa: E402


class LintMemoryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.rewire = self.tmp / "rewire"
        self.compiled = self.tmp / "compiled"
        self.rewire.mkdir()
        self.compiled.mkdir()
        lm.REWIRE, self.orig_rewire = self.rewire, lm.REWIRE
        lm.COMPILED, self.orig_compiled = self.compiled, lm.COMPILED
        lm.REPO, self.orig_repo = self.tmp, lm.REPO

    def tearDown(self):
        lm.REWIRE = self.orig_rewire
        lm.COMPILED = self.orig_compiled
        lm.REPO = self.orig_repo
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _clean_memory(self):
        (self.compiled / "MEMORY.md").write_text("# index\n")
        (self.compiled / "journal.md").write_text("# journal\n")
        (self.compiled / "corrections.md").write_text("# corrections\n")

    def test_clean_repo_passes(self):
        self._clean_memory()
        result = lm.run()
        self.assertTrue(result.ok, result.failures)

    def test_seeded_secret_fails(self):
        self._clean_memory()
        (self.compiled / "people" / "leak.md").parent.mkdir(exist_ok=True)
        (self.compiled / "people" / "leak.md").write_text(
            "api_key: sk-ant-abc123def456ghi789jklmno\n"
        )
        result = lm.run()
        self.assertFalse(result.ok)
        self.assertTrue(any(f.check == "secret-shaped-value" for f in result.failures))

    def test_broken_memory_link_fails(self):
        self._clean_memory()
        (self.compiled / "MEMORY.md").write_text("[nope](does/not/exist.md)\n")
        result = lm.run()
        self.assertFalse(result.ok)
        self.assertTrue(any(f.check == "broken-memory-link" for f in result.failures))

    def test_missing_date_or_source_fails(self):
        self._clean_memory()
        (self.compiled / "journal.md").write_text("- shipped the thing\n")
        result = lm.run()
        self.assertFalse(result.ok)
        self.assertTrue(any(f.check == "missing-date-or-source" for f in result.failures))

    def test_well_formed_entry_passes(self):
        self._clean_memory()
        (self.compiled / "journal.md").write_text(
            "- [2026-09-01] [source: Code session] shipped the thing\n"
        )
        result = lm.run()
        self.assertTrue(result.ok, result.failures)

    def test_compiler_marker_in_rewire_fails(self):
        (self.rewire / "voice.md").write_text(f"{lm.COMPILER_MARKER}\nsome rule\n")
        self._clean_memory()
        result = lm.run()
        self.assertFalse(result.ok)
        self.assertTrue(any(f.check == "compiler-wrote-rewire" for f in result.failures))

    def test_stale_unreviewed_correction_fails(self):
        self._clean_memory()
        old = (date.today() - timedelta(days=45)).isoformat()
        (self.compiled / "corrections.md").write_text(
            f"- [{old}] [source: User] never do X. (seen: 1)\n"
        )
        result = lm.run()
        self.assertFalse(result.ok)
        self.assertTrue(any(f.check == "stale-unreviewed-correction" for f in result.failures))

    def test_recent_correction_not_stale(self):
        self._clean_memory()
        today = date.today().isoformat()
        (self.compiled / "corrections.md").write_text(
            f"- [{today}] [source: User] never do X. (seen: 1)\n"
        )
        result = lm.run()
        self.assertTrue(result.ok, result.failures)

    def test_seeded_secret_in_rewire_also_fails(self):
        (self.rewire / "voice.md").write_text("password=hunter2hunter2\n")
        self._clean_memory()
        result = lm.run()
        self.assertFalse(result.ok)
        self.assertTrue(any(f.check == "secret-shaped-value" for f in result.failures))


if __name__ == "__main__":
    unittest.main()
