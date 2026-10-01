from pathlib import Path

from datareport.analyzer import build_report, infer_kind, load_csv


def test_load_csv_and_build_report(tmp_path: Path):
    source = tmp_path / "vendas.csv"
    source.write_text(
        "produto,categoria,valor\n"
        "Teclado,Perifericos,120.50\n"
        "Mouse,Perifericos,80\n"
        "Fone,Audio,150\n",
        encoding="utf-8",
    )

    headers, rows = load_csv(source)
    assert headers == ["produto", "categoria", "valor"]
    assert len(rows) == 3

    report = build_report(source)
    assert report["rows"] == 3
    assert report["columns"] == 3
    valor = next(item for item in report["column_profiles"] if item["name"] == "valor")
    assert valor["kind"] == "numeric"
    assert valor["minimum"] == 80.0
    assert valor["maximum"] == 150.0


def test_infer_kind():
    assert infer_kind(["10", "20.5", "30"]) == "numeric"
    assert infer_kind(["A", "B", "A"]) == "text"
    assert infer_kind(["", ""]) == "empty"
