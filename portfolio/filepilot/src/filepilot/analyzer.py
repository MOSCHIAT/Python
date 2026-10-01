from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
from typing import Iterable


def iter_files(source: Path, recursive: bool = True) -> Iterable[Path]:
    pattern = "**/*" if recursive else "*"
    for path in source.glob(pattern):
        if path.is_file():
            yield path


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def analyze_directory(source: Path) -> list[dict[str, object]]:
    source = source.expanduser().resolve()
    if not source.is_dir():
        raise ValueError(f"Source directory does not exist: {source}")

    rows: list[dict[str, object]] = []
    for path in iter_files(source):
        stat = path.stat()
        modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
        rows.append(
            {
                "path": str(path.relative_to(source)),
                "extension": path.suffix.lower() or "[none]",
                "size_bytes": stat.st_size,
                "modified_utc": modified,
                "sha256": sha256(path),
            }
        )
    return sorted(rows, key=lambda row: str(row["path"]).lower())


def duplicate_groups(rows: list[dict[str, object]]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        groups[str(row["sha256"])].append(str(row["path"]))
    return {digest: paths for digest, paths in groups.items() if len(paths) > 1}


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    by_extension: dict[str, int] = defaultdict(int)
    total_bytes = 0
    for row in rows:
        by_extension[str(row["extension"])] += 1
        total_bytes += int(row["size_bytes"])
    duplicates = duplicate_groups(rows)
    return {
        "files": len(rows),
        "total_bytes": total_bytes,
        "extensions": dict(sorted(by_extension.items())),
        "duplicate_groups": len(duplicates),
    }


def write_csv(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["path", "extension", "size_bytes", "modified_utc", "sha256"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
