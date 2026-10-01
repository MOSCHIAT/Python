from pathlib import Path

from datareport.report import write_html, write_json


def test_report_files_are_created(tmp_path: Path):
    report = {
        "generated_at": "2026-10-01T00:00:00+00:00",
        "source": "/tmp/data.csv",
        "rows": 2,
        "columns": 1,
        "column_profiles": [
            {
                "name": "valor",
                "kind": "numeric",
                "missing": 0,
                "unique": 2,
                "mean": 15.0,
                "minimum": 10.0,
                "maximum": 20.0,
                "top_values": None,
            }
        ],
    }
    html = tmp_path / "report.html"
    json_file = tmp_path / "report.json"
    write_html(report, html)
    write_json(report, json_file)
    assert "DataReport" in html.read_text(encoding="utf-8")
    assert '"rows": 2' in json_file.read_text(encoding="utf-8")
