# Plano 05 — Dataset, execução e pitch

## Objetivo

Empacotar uma demonstração reproduzível, honesta e pronta para os três minutos.

## Tarefas

### 05-01 — Fixtures sintéticas calibradas

- criar cinco XMLs de venda de oficina, com CNPJs fictícios e declaração de fixture;
- incluir pastilha, amortecedor, filtro, vela e pneu com regras/estados coerentes;
- gerar ZIP e fixtures extras de bebida/farmácia;
- provar em teste que o lote retorna exatamente `1840.00`.

**Commit:** `test(05-01): add synthetic tax audit fixtures`

### 05-02 — Execução em um comando

- criar `start.py`, `run.sh` executável e configuração local robusta;
- verificar porta 8000 e mensagens de inicialização.

**Commit:** `chore(05-02): add one-command local runner`

### 05-03 — README e arquitetura

- documentar instalação, Mermaid, endpoints, cálculo, privacidade, limites e fontes;
- explicar dados sintéticos e operação com/sem OpenAI.

**Commit:** `docs(05-03): document Audita architecture and safeguards`

### 05-04 — Pitch de três minutos

- criar roteiro minuto a minuto orientado a problema, prova, diferencial e próximos passos;
- proibir “crédito garantido”, “Pix imediato” e alegações de notas reais;
- atualizar estado e resumo.

**Commit:** `docs(05-04): add responsible hackathon pitch`
