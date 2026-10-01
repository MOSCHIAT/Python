from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import shutil


@dataclass(frozen=True)
class BackupResult:
    copied: int
    skipped: int
    manifest: Path


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return {str(key): str(value) for key, value in data.items()}


def backup_directory(source: Path, destination: Path, dry_run: bool = False) -> BackupResult:
    source = source.expanduser().resolve()
    destination = destination.expanduser().resolve()
    if not source.is_dir():
        raise ValueError(f"Source directory does not exist: {source}")
    if source == destination or source in destination.parents:
        raise ValueError("Destination must not be inside the source directory")

    manifest_path = destination / ".filepilot-manifest.json"
    previous = load_manifest(manifest_path)
    current: dict[str, str] = {}
    copied = skipped = 0

    for source_file in sorted(source.glob("**/*")):
        if not source_file.is_file():
            continue
        relative = str(source_file.relative_to(source))
        digest = sha256(source_file)
        current[relative] = digest
        target = destination / relative

        if previous.get(relative) == digest and target.exists():
            skipped += 1
            continue

        copied += 1
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target)

    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
        with manifest_path.open("w", encoding="utf-8") as handle:
            json.dump(current, handle, indent=2, ensure_ascii=False, sort_keys=True)

    return BackupResult(copied=copied, skipped=skipped, manifest=manifest_path)
