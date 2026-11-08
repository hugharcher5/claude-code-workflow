"""Slugs come from a model reading untrusted transcripts; only plain kebab names may become paths."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import compile_memory as m


def test_unsafe_slugs_are_dropped():
    bad = ["../../evil", "a/b", "..", "", "Matt", "x.md", "a\\b", None, 7]
    candidates = {"people": [{"slug": s, "fact": "f", "source": "s"} for s in bad]}
    assert m.build_diffs(candidates) == {}


def test_kebab_slug_is_kept():
    diffs = m.build_diffs({"projects": [{"slug": "geo-grail-2", "fact": "f", "source": "s"}]})
    assert [p.name for p in diffs] == ["geo-grail-2.md"]


if __name__ == "__main__":
    test_unsafe_slugs_are_dropped()
    test_kebab_slug_is_kept()
    print("ok")
