from pathlib import Path

from filepilot.analyzer import analyze_directory, duplicate_groups


def test_analyze_and_find_duplicates(tmp_path: Path):
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "b.txt").write_text("hello", encoding="utf-8")
    rows = analyze_directory(tmp_path)
    assert len(rows) == 2
    duplicates = duplicate_groups(rows)
    assert len(duplicates) == 1
    assert sorted(next(iter(duplicates.values()))) == ["a.txt", "b.txt"]
