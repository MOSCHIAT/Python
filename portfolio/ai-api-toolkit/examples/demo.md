# Demonstração

## Sem internet

```bash
ai-toolkit "Crie um nome para um projeto Python" --mock
```

## Com Gemini

```bash
ai-toolkit "Transforme esta ideia em 5 tarefas técnicas" --save outputs/task.json
```

## Com logs

```bash
ai-toolkit "Analise este texto" --log-file logs/app.log
```

O projeto propositalmente separa:

- configuração
- cliente da API
- serviço
- interface de terminal
- testes

Isso facilita trocar o provider sem reescrever a CLI.
