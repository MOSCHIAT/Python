# DataReport

CLI em Python para transformar arquivos CSV em análises estruturadas e relatórios HTML/JSON.

## O que demonstra

- Leitura e validação de CSV
- Normalização de dados
- Estatísticas numéricas e categóricas
- Detecção básica de valores ausentes
- Geração de JSON
- Geração de relatório HTML sem dependências externas
- Interface CLI com `argparse`
- Type hints e `dataclasses`
- Testes automatizados com `pytest`

## Fluxo

```text
CSV
 │
 ├── valida cabeçalho e linhas
 ├── normaliza valores
 ├── identifica colunas numéricas
 ├── calcula métricas
 │     ├── quantidade
 │     ├── média
 │     ├── mínimo
 │     ├── máximo
 │     └── valores ausentes
 ├── analisa categorias
 └── gera
       ├── report.json
       └── report.html
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

```bash
python -m datareport.cli examples/vendas.csv --html reports/report.html --json reports/report.json
```

Depois de instalar o projeto:

```bash
datareport examples/vendas.csv --html reports/report.html --json reports/report.json
```

## Como explicar em uma entrevista

**Problema:** arquivos CSV frequentemente precisam ser conferidos e resumidos manualmente antes de virar informação útil.

**Solução:** uma ferramenta de linha de comando que recebe um CSV e produz um relatório reproduzível.

**Decisões técnicas:** usei apenas a biblioteca padrão para manter o projeto simples e portátil; separei leitura, análise e apresentação em módulos; criei funções testáveis e tratei erros de entrada.

**Próximas evoluções:** suporte a XLSX/Excel, gráficos, filtros por período, exportação para PDF, banco SQLite e execução agendada.
