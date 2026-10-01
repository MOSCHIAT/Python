from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .analyzer import build_report
from .report import write_html, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="datareport",
        description="Analyze CSV files and generate HTML/JSON reports.",
    )
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--html", type=Path, help="Output HTML report")
    parser.add_argument("--json", type=Path, help="Output JSON report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = build_report(args.csv_file)
        print(f"Rows: {report['rows']}")
        print(f"Columns: {report['columns']}")
        for profile in report["column_profiles"]:
            print(
                f"- {profile['name']}: {profile['kind']}, "
                f"missing={profile['missing']}, unique={profile['unique']}"
            )

        if args.html:
            write_html(report, args.html)
            print(f"HTML: {args.html}")
        if args.json:
            write_json(report, args.json)
            print(f"JSON: {args.json}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
