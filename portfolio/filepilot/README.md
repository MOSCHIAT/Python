# FilePilot

Python CLI para automatizar tarefas reais de arquivos: organizar por tipo, analisar um diretório e criar backups incrementais.

## O que demonstra

- Python moderno com `pathlib`, `dataclasses` e type hints
- CLI com `argparse`
- Operações seguras com modo de planejamento (`dry-run`)
- Hash SHA-256 para detectar alterações e duplicatas
- Relatórios CSV/JSON
- Backup incremental com manifesto
- Tratamento de erros
- Testes automatizados com `pytest`

## Arquitetura

```text
filepilot/
├── src/filepilot/
│   ├── cli.py         # interface de terminal
│   ├── organizer.py   # organização por extensão
│   ├── analyzer.py    # inventário, hashes e duplicatas
│   └── backup.py      # backup incremental
└── tests/
    ├── test_organizer.py
    └── test_analyzer.py
```

## Instalação

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
pip install pytest
```

## Fluxo 1 — organizar arquivos

Primeiro planeje:

```bash
filepilot organize ./Downloads
```

Depois aplique:

```bash
filepilot organize ./Downloads --apply
```

Categorias: `images`, `videos`, `audio`, `documents`, `spreadsheets`, `archives`, `code` e `other`.

## Fluxo 2 — analisar um diretório

```bash
filepilot analyze ./projeto --csv reports/files.csv --json reports/summary.json
```

O relatório calcula tamanho, extensão, data de modificação e SHA-256. Arquivos com o mesmo hash são agrupados como possíveis duplicatas.

## Fluxo 3 — backup incremental

Teste primeiro:

```bash
filepilot backup ./projeto /backup/projeto --dry-run
```

Execute:

```bash
filepilot backup ./projeto /backup/projeto
```

O manifesto `.filepilot-manifest.json` registra o hash de cada arquivo para evitar recópia de conteúdo inalterado.

## Como explicar em uma entrevista

**Problema:** tarefas de organização, inventário e backup consomem tempo e geram erros manuais.

**Solução:** uma CLI única que transforma essas tarefas em operações reproduzíveis.

**Decisões técnicas:** `pathlib` para manipulação de caminhos; SHA-256 para comparação de conteúdo; `dry-run` para reduzir risco; CSV/JSON para integração com outras ferramentas; testes para validar regras críticas.

**Próximas evoluções:** configuração via TOML/JSON, logs estruturados, exclusão por padrão de arquivos sensíveis, execução agendada e integração com armazenamento em nuvem.
