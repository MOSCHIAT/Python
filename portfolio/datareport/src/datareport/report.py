from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any
import json


def write_json(report: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _metric(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:,.2f}"
    return str(value)


def write_html(report: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    cards = "".join(
        f'<div class="card"><strong>{escape(str(label))}</strong><span>{escape(_metric(value))}</span></div>'
        for label, value in [
            ("Registros", report["rows"]),
            ("Colunas", report["columns"]),
            ("Gerado em", report["generated_at"]),
        ]
    )

    rows = []
    for profile in report["column_profiles"]:
        top = ", ".join(
            f'{item["value"]} ({item["count"]})'
            for item in profile.get("top_values") or []
        )
        rows.append(
            "<tr>"
            f'<td>{escape(str(profile["name"]))}</td>'
            f'<td>{escape(str(profile["kind"]))}</td>'
            f'<td>{profile["missing"]}</td>'
            f'<td>{profile["unique"]}</td>'
            f'<td>{escape(_metric(profile.get("mean")))}</td>'
            f'<td>{escape(_metric(profile.get("minimum")))}</td>'
            f'<td>{escape(_metric(profile.get("maximum")))}</td>'
            f'<td>{escape(top)}</td>'
            "</tr>"
        )

    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DataReport</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:1200px;margin:40px auto;padding:0 20px;background:#f5f5f5;color:#171717}}
h1{{margin-bottom:6px}} .muted{{color:#666}}
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:24px 0}}
.card{{background:white;padding:18px;border-radius:12px;box-shadow:0 2px 10px #00000012}}
.card span{{display:block;font-size:1.25rem;margin-top:8px;word-break:break-word}}
table{{width:100%;border-collapse:collapse;background:white;border-radius:12px;overflow:hidden}}
th,td{{padding:10px;border-bottom:1px solid #eee;text-align:left;vertical-align:top}}
th{{background:#fafafa}}
@media(max-width:800px){{.cards{{grid-template-columns:1fr}}table{{font-size:.9rem;display:block;overflow:auto}}}}
</style>
</head>
<body>
<h1>DataReport</h1>
<p class="muted">Fonte: {escape(report["source"])}</p>
<div class="cards">{cards}</div>
<table>
<thead><tr><th>Coluna</th><th>Tipo</th><th>Ausentes</th><th>Únicos</th><th>Média</th><th>Mínimo</th><th>Máximo</th><th>Top valores</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</body>
</html>
"""
    output.write_text(html, encoding="utf-8")
