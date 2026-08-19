# Plano 01 — Core tributário e XML

## Objetivo

Entregar uma base Python 3.12 determinística que parseia NF-e/NFC-e e calcula potencial de PIS/Cofins com regras versionadas e explicáveis.

## Contexto obrigatório

Ler `../../PROJECT.md`, `../../REQUIREMENTS.md`, `../../STATE.md` e `../../../design-system/audita/MASTER.md`. Consultar os documentos jurídicos na raiz do repositório, sobretudo `NCM_MONOFASICO_REGRAS_E_FONTES.md`.

## Tarefas

### 01-01 — Ambiente e esqueleto

- criar `.venv` com `python3.12` e instalar as dependências obrigatórias;
- criar `requirements.txt`, `.env`, `.env.example`, `.gitignore` local e pacotes `app/`;
- garantir que segredos e `.venv` não sejam versionados.

**Commit:** `chore(01-01): bootstrap Python environment`

### 01-02 — Modelos e motor tributário

- implementar modelos Pydantic para nota, item, achado, premissas e resumo;
- implementar faixas do Anexo I, fórmula efetiva e fração PIS/Cofins com `Decimal`;
- implementar regras NCM versionadas com fonte, descrição, vigência, exceções e nível de confiança;
- separar sinais CST PIS/Cofins de CSOSN/ICMS e produzir explicações.

**Commit:** `feat(01-02): add versioned tax rules engine`

### 01-03 — Parser e auditoria em lote

- parsear `NFe`, `nfeProc` e namespaces variados com lxml;
- extrair campos fiscais detalhados e tolerar opcionais;
- consolidar lote usando receita de venda e contexto PGDAS, nunca compra isolada;
- validar XML malformado com erro controlado.

**Commit:** `feat(01-03): implement resilient NFe batch parser`

### 01-04 — Testes do core

- cobrir faixas, arredondamento, segregação, status NCM, CST/CSOSN, namespaces e lote;
- executar pytest e corrigir falhas.

**Commit:** `test(01-04): cover tax engine and NFe parser`

## Verificação

- `.venv/bin/python --version` deve ser 3.12.x;
- nenhum segredo versionado;
- testes do core verdes;
- atualizar `../../STATE.md` e criar `01-SUMMARY.md`.
