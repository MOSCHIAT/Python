from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv
import math
from typing import Any


@dataclass(frozen=True)
class ColumnProfile:
    name: str
    kind: str
    count: int
    missing: int
    unique: int
    mean: float | None = None
    minimum: float | None = None
    maximum: float | None = None
    top_values: list[dict[str, Any]] | None = None


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"CSV file does not exist: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV must contain a header row")

        headers = [header.strip() for header in reader.fieldnames]
        if any(not header for header in headers):
            raise ValueError("CSV contains an empty column name")
        if len(set(headers)) != len(headers):
            raise ValueError("CSV contains duplicated column names")

        rows: list[dict[str, str]] = []
        for raw in reader:
            row = {header: (raw.get(header) or "").strip() for header in headers}
            rows.append(row)

    return headers, rows


def parse_number(value: str) -> float | None:
    if not value:
        return None
    normalized = value.strip().replace(",", ".")
    try:
        number = float(normalized)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def infer_kind(values: list[str]) -> str:
    non_empty = [value for value in values if value]
    if not non_empty:
        return "empty"
    numeric = [parse_number(value) for value in non_empty]
    return "numeric" if all(value is not None for value in numeric) else "text"


def profile_column(name: str, rows: list[dict[str, str]]) -> ColumnProfile:
    values = [row.get(name, "") for row in rows]
    missing = sum(1 for value in values if not value)
    unique = len(set(value for value in values if value))
    kind = infer_kind(values)

    if kind == "numeric":
        numbers = [parse_number(value) for value in values if value]
        assert all(number is not None for number in numbers)
        cast_numbers = [float(number) for number in numbers if number is not None]
        return ColumnProfile(
            name=name,
            kind=kind,
            count=len(values),
            missing=missing,
            unique=unique,
            mean=sum(cast_numbers) / len(cast_numbers) if cast_numbers else None,
            minimum=min(cast_numbers) if cast_numbers else None,
            maximum=max(cast_numbers) if cast_numbers else None,
        )

    counter = Counter(value for value in values if value)
    top_values = [
        {"value": value, "count": count}
        for value, count in counter.most_common(5)
    ]
    return ColumnProfile(
        name=name,
        kind=kind,
        count=len(values),
        missing=missing,
        unique=unique,
        top_values=top_values,
    )


def build_report(path: Path) -> dict[str, Any]:
    headers, rows = load_csv(path)
    profiles = [profile_column(header, rows) for header in headers]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(path.expanduser().resolve()),
        "rows": len(rows),
        "columns": len(headers),
        "column_profiles": [profile.__dict__ for profile in profiles],
    }
