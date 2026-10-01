from pathlib import Path
from webmonitor.models import PageSnapshot
from webmonitor.monitor import check_urls, read_urls

def fake_fetch(url,timeout): return PageSnapshot(url,200,"Example","hello","hash-1")
def fake_fetch_changed(url,timeout): return PageSnapshot(url,200,"Example","changed","hash-2")

def test_new_then_unchanged(tmp_path: Path):
    urls=tmp_path/"urls.txt"; urls.write_text("# public pages\\nhttps://example.com\\nhttps://example.com\\n",encoding="utf-8")
    state=tmp_path/"state.json"
    assert read_urls(urls)==["https://example.com"]
    first=check_urls(["https://example.com"],state,fetcher=fake_fetch)
    second=check_urls(["https://example.com"],state,fetcher=fake_fetch)
    assert first[0].status=="NEW"; assert second[0].status=="UNCHANGED"

def test_changed_page(tmp_path: Path):
    state=tmp_path/"state.json"
    check_urls(["https://example.com"],state,fetcher=fake_fetch)
    results=check_urls(["https://example.com"],state,fetcher=fake_fetch_changed)
    assert results[0].status=="CHANGED"
