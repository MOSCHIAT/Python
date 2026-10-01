from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .analyzer import analyze_directory, duplicate_groups, summary, write_csv
from .backup import backup_directory
from .organizer import apply_operations, plan_organization


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="filepilot", description="Practical file automation toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    organize = sub.add_parser("organize", help="Organize files by type")
    organize.add_argument("source", type=Path)
    organize.add_argument("--recursive", action="store_true")
    organize.add_argument("--apply", action="store_true", help="Actually move files")

    analyze = sub.add_parser("analyze", help="Create a file inventory and duplicate report")
    analyze.add_argument("source", type=Path)
    analyze.add_argument("--csv", type=Path, help="Write a CSV report")
    analyze.add_argument("--json", type=Path, help="Write a JSON summary")

    backup = sub.add_parser("backup", help="Create an incremental backup")
    backup.add_argument("source", type=Path)
    backup.add_argument("destination", type=Path)
    backup.add_argument("--dry-run", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "organize":
            operations = plan_organization(args.source, recursive=args.recursive)
            for operation in operations:
                print(f"{operation.source} -> {operation.destination}")
            count = apply_operations(operations, dry_run=not args.apply)
            mode = "moved" if args.apply else "planned"
            print(f"\n{count} file(s) {mode}.")
            return 0

        if args.command == "analyze":
            rows = analyze_directory(args.source)
            report = summary(rows)
            duplicates = duplicate_groups(rows)
            print(json.dumps(report, indent=2, ensure_ascii=False))
            if duplicates:
                print("\nDuplicates:")
                for digest, paths in duplicates.items():
                    print(f"{digest[:12]}: {', '.join(paths)}")
            if args.csv:
                write_csv(rows, args.csv)
                print(f"\nCSV: {args.csv}")
            if args.json:
                args.json.parent.mkdir(parents=True, exist_ok=True)
                args.json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
                print(f"JSON: {args.json}")
            return 0

        if args.command == "backup":
            result = backup_directory(args.source, args.destination, dry_run=args.dry_run)
            print(f"Copied: {result.copied}")
            print(f"Skipped: {result.skipped}")
            print(f"Manifest: {result.manifest}")
            return 0

    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    parser.error("Unknown command")
    return 2
