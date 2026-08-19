# Plano 02 — IA, Copilot e relatórios

## Objetivo

Explicar os achados e gerar artefatos profissionais, mantendo o produto íntegro sem chave ou rede.

## Tarefas

### 02-01 — Auditor OpenAI com fallback

- implementar OpenAI Python SDK usando Responses API e `gpt-4o-mini`;
- solicitar estrutura `resumo`, `fundamentacao`, `plano_acao`, `alertas`;
- validar a resposta e retornar fallback local fundamentado em qualquer falha;
- não permitir que a IA altere números ou classificação determinística.

**Commit:** `feat(02-01): add AI auditor with local fallback`

### 02-02 — Copilot seguro

- implementar FAQ local e chat OpenAI opcional;
- incluir fontes, limites, transição CBS e próximos passos;
- impedir promessas de restituição e orientar validação do contador.

**Commit:** `feat(02-02): implement evidence-aware tax copilot`

### 02-03 — Excel executivo

- gerar três abas, estilos Slate/Emerald, filtros, congelamento, moeda e fórmulas SUM;
- registrar premissas de RBT12, faixa, segregação e status de revisão;
- validar reabertura do workbook.

**Commit:** `feat(02-03): generate auditable Excel workbook`

### 02-04 — PDF de memória e checklist

- gerar memória formal com identificação da simulação/empresa, cálculo, itens, base legal, riscos e checklist;
- explicitar que não é petição, parecer ou garantia;
- validar assinatura `%PDF` e conteúdo extraído.

**Commit:** `feat(02-04): generate calculation memo PDF`

### 02-05 — Testes de serviços

- testar fallback, proteção de chave, XLSX e PDF;
- atualizar estado e resumo da fase.

**Commit:** `test(02-05): verify AI fallbacks and reports`
