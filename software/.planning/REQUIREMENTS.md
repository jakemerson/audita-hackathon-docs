# Requisitos — Audita

## Motor tributário

- [x] **TAX-01** Calcular alíquota efetiva do Anexo I pela fórmula `(RBT12 × alíquota nominal − parcela a deduzir) ÷ RBT12`, com `Decimal` e faixas oficiais.
- [x] **TAX-02** Calcular a parcela potencial de PIS/Cofins como alíquota efetiva × 15,5% nas faixas suportadas, vedando o uso de 3,65% fixos.
- [x] **TAX-03** Zerar o potencial quando o usuário informar que a receita já foi segregada no PGDAS-D.
- [x] **TAX-04** Manter regras NCM versionadas, com lei, vigência, descrição, exceções/destinação e status `CONFIRMADO`, `REVISAR`, `NAO_ENQUADRADO`.
- [x] **TAX-05** Cobrir os NCMs da demo nos segmentos de autopeças, bebidas frias e medicamentos/cosméticos, sem apresentar o subconjunto como lista legal completa.
- [x] **TAX-06** Detectar sinais em CST de PIS/Cofins sem confundir CSOSN de ICMS e sem considerar sinal isolado como prova.
- [x] **TAX-07** Gerar explicação e trilha de evidências para cada item.

## Documentos fiscais

- [x] **XML-01** Ler NF-e/NFC-e 4.00 com ou sem `nfeProc`, ignorando prefixos de namespace.
- [x] **XML-02** Extrair cabeçalho, emitente, destinatário, item, NCM, CFOP, valor, ICMS/CSOSN, PIS e Cofins/CST.
- [x] **XML-03** Auditar lote e consolidar notas, receita, receita monofásica, achados e potencial.
- [x] **XML-04** Rejeitar XML malformado e ZIP inseguro com mensagens úteis, sem path traversal ou arquivos arbitrários.

## IA e explicações

- [x] **AI-01** Usar OpenAI Responses API e `gpt-4o-mini` quando uma chave válida existir, solicitando saída estruturada.
- [x] **AI-02** Entregar parecer executivo, fundamentação e plano de ação por fallback local quando não houver chave ou a chamada falhar.
- [x] **AI-03** Responder no Copilot com fontes, premissas, aviso de validação profissional e recusa a garantias.
- [x] **AI-04** Manter chave dinâmica somente em memória e nunca retorná-la ou registrá-la.

## Relatórios

- [x] **REP-01** Gerar XLSX com `Resumo Executivo`, `Itens Auditados` e `Memória PGDAS-D`, fórmulas e visual C-Level.
- [x] **REP-02** Gerar PDF formal de memória de cálculo e checklist, com premissas, base normativa e assinatura de validação do contador.
- [x] **REP-03** Identificar os artefatos como apoio técnico, não petição, parecer jurídico ou garantia de crédito.

## API

- [x] **API-01** Expor `POST /api/audit/upload` para múltiplos XML/ZIP e contexto RBT12/PGDAS.
- [x] **API-02** Expor `POST /api/audit/demo-oficina` com simulação sintética determinística de R$ 1.840,00.
- [x] **API-03** Expor `POST /api/audit/copilot`, `POST /api/export/excel` e `POST /api/export/pdf`.
- [x] **API-04** Expor `GET /api/health` e `POST /api/config/set-key` seguro.
- [x] **API-05** Servir a SPA e os assets estáticos na raiz.

## Experiência do usuário

- [x] **UI-01** Implementar workspace responsivo em dark glassmorphism profissional, seguindo `design-system/audita`.
- [x] **UI-02** Oferecer dropzone acessível, progresso e botão `Demo 3 min — Oficina`.
- [x] **UI-03** Exibir potencial animado, confetti com redução de movimento, quatro KPIs e aviso visível de simulação/estimativa.
- [x] **UI-04** Exibir donut de distribuição, parecer em abas, tabela pesquisável/filtrável e trilha de evidências.
- [x] **UI-05** Implementar drawer do Copilot, perguntas rápidas e modal seguro da chave OpenAI.
- [x] **UI-06** Permitir downloads reais de Excel/PDF e navegação por teclado com estados de foco.

## Demo, documentação e qualidade

- [x] **DEMO-01** Criar cinco XMLs sintéticos de oficina e ZIP cujo cenário produza exatamente R$ 1.840,00.
- [x] **DEMO-02** Criar fixtures extras sintéticas de cervejaria e farmácia.
- [x] **DEMO-03** Criar `.venv` Python 3.12, dependências, `.env` placeholder, `.env.example`, `run.sh` e `start.py`.
- [x] **DOC-01** Documentar instalação, arquitetura Mermaid, modelo de cálculo, limites legais e fontes no README.
- [x] **DOC-02** Criar roteiro de pitch minuto a minuto sem alegações enganosas.
- [x] **QA-01** Implementar e aprovar pelo menos 17 testes unitários e de integração.
- [x] **QA-02** Validar no navegador demo, valor, abas, gráfico, busca, Copilot e downloads.
- [x] **QA-03** Registrar bugs encontrados em `.planning/debug/` e correções em commits atômicos.

## Matriz de rastreabilidade

| Fase | Requisitos |
|---|---|
| 01 — Core | TAX-01..07, XML-01..04, DEMO-03 parcial |
| 02 — IA e relatórios | AI-01..04, REP-01..03 |
| 03 — API | API-01..05 |
| 04 — Frontend | UI-01..06 |
| 05 — Demo e docs | DEMO-01..03, DOC-01..02 |
| 06 — Validação | QA-01..03 |
