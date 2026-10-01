from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
from typing import Iterable

CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".svg"},
    "videos": {".mp4", ".mov", ".mkv", ".avi", ".webm", ".wmv"},
    "audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"},
    "documents": {".pdf", ".doc", ".docx", ".odt", ".txt", ".rtf"},
    "spreadsheets": {".csv", ".xls", ".xlsx", ".ods"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "code": {".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".yaml", ".yml", ".md"},
}


@dataclass(frozen=True)
class Operation:
    source: Path
    destination: Path


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "other"


def iter_files(source: Path, recursive: bool = False) -> Iterable[Path]:
    pattern = "**/*" if recursive else "*"
    for path in source.glob(pattern):
        if path.is_file():
            yield path


def unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination
    index = 1
    while True:
        candidate = destination.with_name(f"{destination.stem} ({index}){destination.suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def plan_organization(source: Path, recursive: bool = False) -> list[Operation]:
    source = source.expanduser().resolve()
    if not source.is_dir():
        raise ValueError(f"Source directory does not exist: {source}")

    operations: list[Operation] = []
    for file_path in iter_files(source, recursive=recursive):
        category = category_for(file_path)
        destination_dir = source / category
        destination = unique_destination(destination_dir / file_path.name)
        operations.append(Operation(file_path, destination))
    return operations


def apply_operations(operations: Iterable[Operation], dry_run: bool = True) -> int:
    count = 0
    for operation in operations:
        if not dry_run:
            operation.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(operation.source), str(operation.destination))
        count += 1
    return count
