from webmonitor.fetcher import PageParser, normalize_url

def test_parser_removes_script_and_reads_title():
    parser=PageParser()
    parser.feed("<html><title>Site</title><body>Olá <b>mundo</b><script>ignore()</script></body></html>")
    assert parser.title=="Site"
    assert parser.visible_text=="Olá mundo"

def test_normalize_url():
    assert normalize_url(" https://example.com ")=="https://example.com"
