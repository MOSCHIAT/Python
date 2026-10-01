# AI API Toolkit

CLI em Python para integrar uma aplicação com um modelo generativo via API, com validação de entrada, timeout, tratamento de erros, logging e modo mock.

O exemplo incluído usa a API Gemini por HTTP. A documentação oficial da Google descreve o endpoint `models.generateContent` e o uso do cabeçalho `x-goog-api-key`. Para projetos novos, a documentação atual recomenda avaliar a API Interactions; este repositório mantém o fluxo HTTP simples para fins de estudo e portfólio. citeturn450131search4turn450131search8

## O que demonstra

- Integração com API REST
- Autenticação por variável de ambiente
- JSON request/response
- Timeout de rede
- Tratamento de erros HTTP
- Logging
- Separação entre cliente HTTP e regra da aplicação
- CLI com `argparse`
- Modo `mock` para desenvolvimento sem custo/chave
- Testes sem dependência de internet

## Fluxo

```text
PROMPT
  │
  ├── valida entrada
  │
  ├── seleciona provider
  │     ├── mock
  │     └── Gemini HTTP
  │
  ├── monta payload JSON
  │
  ├── envia POST
  │
  ├── trata timeout / HTTP / JSON
  │
  ├── extrai resposta
  │
  └── salva resultado + log
```

## Instalação

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -e .
pip install pytest
```

## Executar sem API

```bash
ai-toolkit "Explique Python em 3 frases" --mock
```

## Usar Gemini

A documentação atual da Google orienta manter a chave fora do código e disponibilizá-la por variável de ambiente. citeturn450131search0turn450131search1

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="SUA_CHAVE"
```

macOS/Linux:

```bash
export GEMINI_API_KEY="SUA_CHAVE"
```

Depois:

```bash
ai-toolkit "Crie 5 ideias de automação com Python"
```

O modelo pode ser configurado:

```bash
ai-toolkit "Explique APIs REST" --model gemini-3.8-flash
```

A documentação oficial apresenta modelos Gemini no formato `models/...:generateContent`; o nome do modelo deve ser ajustado conforme os modelos disponíveis na sua conta. citeturn450131search4turn450131search9

## Logs e salvamento

```bash
ai-toolkit "Resuma automação de arquivos" --save outputs/response.json --log-file logs/app.log
```

O JSON salvo contém:

- provider
- model
- prompt
- resposta
- timestamp

## Como explicar em uma entrevista

**Problema:** aplicações precisam consumir serviços de IA sem misturar autenticação, rede e regra de negócio em um único arquivo.

**Solução:** criei uma CLI que valida a entrada, seleciona um provider, monta a requisição, trata falhas de rede e transforma a resposta da API em um resultado utilizável.

**Decisões técnicas:** mantive o cliente HTTP separado da CLI; usei variáveis de ambiente para segredo; implementei timeout explícito; criei modo mock para testes e desenvolvimento sem chamadas externas.

**Próximas evoluções:** retry com backoff, múltiplos providers, streaming, cache, métricas de latência, schema de saída e integração com banco.

## Segurança

Nunca coloque chaves em código, README ou commits. Use variáveis de ambiente e mantenha arquivos locais de configuração fora do Git.

A documentação da Gemini também descreve a evolução das chaves de API e recomenda práticas de autenticação atualizadas. citeturn450131search0turn450131search1
