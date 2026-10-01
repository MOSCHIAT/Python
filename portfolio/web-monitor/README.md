# Web Monitor

CLI em Python para monitorar páginas públicas e detectar mudanças de conteúdo entre execuções.

## O que demonstra
- HTTP com a biblioteca padrão do Python
- parsing de HTML com `HTMLParser`
- SHA-256 como fingerprint do conteúdo
- histórico persistente em JSON
- comparação entre execuções
- estados `NEW`, `CHANGED`, `UNCHANGED` e `ERROR`
- CLI com `argparse`
- timeout e tratamento de erros HTTP
- testes sem depender de internet

## Fluxo
```text
URLs -> validação -> HTTP GET -> HTMLParser -> texto normalizado
     -> SHA-256 -> compara histórico -> NEW/CHANGED/UNCHANGED
     -> salva estado -> relatório JSON
```

## Instalação
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
pip install pytest
```

## Uso
Crie `urls.txt`:
```text
# páginas públicas
https://example.com
https://www.python.org
```

Execute:
```bash
web-monitor urls.txt
web-monitor urls.txt --report reports/check.json
web-monitor urls.txt --state state/pages.json
```

Na primeira execução uma página é `NEW`. Sem alteração passa a `UNCHANGED`; quando o fingerprint muda, passa a `CHANGED`.

## Limitações
O monitor analisa o HTML recebido pelo servidor e o texto visível extraído. Conteúdo carregado exclusivamente por JavaScript pode exigir Playwright.

Use somente em páginas públicas e respeite termos de uso, `robots.txt`, limites de requisição e políticas do site. Não há login, bypass ou coleta de áreas privadas.

## Como explicar em entrevista
**Problema:** verificar manualmente se páginas públicas foram alteradas é repetitivo.

**Solução:** uma CLI que coleta, normaliza, cria um fingerprint, compara com o histórico e classifica mudanças.

**Decisões:** `HTMLParser` sem dependência pesada, SHA-256 para fingerprint determinístico e JSON para estado entre execuções.

**Próximas evoluções:** agendamento, webhook/e-mail, seletor de seção, SQLite, histórico de diffs, métricas de latência e Playwright.
