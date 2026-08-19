# Plano 03 — API FastAPI

## Objetivo

Orquestrar auditoria, demo, Copilot e exportações por uma API segura e simples.

## Tarefas

### 03-01 — Aplicação e configuração

- criar FastAPI, healthcheck, tratamento de erros e store em memória para chave;
- montar estáticos e rota raiz;
- nunca logar ou retornar a chave.

**Commit:** `feat(03-01): bootstrap FastAPI application`

### 03-02 — Upload e ZIP seguro

- aceitar múltiplos XML/ZIP, limites de tamanho/quantidade e contexto RBT12/PGDAS;
- validar extensão, membros ZIP, compactação e path traversal;
- retornar relatório serializável e parecer.

**Commit:** `feat(03-02): add secure batch audit endpoint`

### 03-03 — Demo e Copilot

- expor demo sintética determinística e chat;
- incluir metadados de simulação, premissas e avisos em toda resposta.

**Commit:** `feat(03-03): expose demo and copilot endpoints`

### 03-04 — Exportações e testes

- streaming XLSX/PDF com nomes seguros;
- testar rotas, erros, ZIP e conteúdo dos downloads;
- atualizar estado e resumo.

**Commit:** `test(03-04): cover API audit and exports`
