# Roadmap — Audita

## Fase 01 — Ambiente, motor tributário e parser XML

**Objetivo:** criar a fundação determinística e juridicamente defensável.

**Entregas:** `.venv`, estrutura Python, modelos Pydantic, regras NCM versionadas, cálculo Anexo I, parser resiliente e auditoria em lote.

**Critério de saída:** testes do cálculo, classificação, namespaces e consolidação aprovados.

## Fase 02 — Auditor OpenAI, Copilot e relatórios

**Objetivo:** transformar achados em explicações e artefatos úteis sem depender da IA.

**Entregas:** Responses API, fallback local, Copilot, XLSX e PDF de memória/checklist.

**Critério de saída:** serviços funcionam com chave ausente e geram arquivos válidos.

## Fase 03 — API REST FastAPI

**Objetivo:** expor o fluxo completo por endpoints seguros e estáveis.

**Entregas:** upload XML/ZIP, demo, Copilot, exportações, healthcheck, chave em memória e assets estáticos.

**Critério de saída:** testes de integração cobrem sucesso, validação e segurança de ZIP.

## Fase 04 — Frontend SPA premium

**Objetivo:** entregar uma demo memorável, acessível e transparente.

**Entregas:** dropzone, demo, contador/confetti, KPIs, gráfico, abas, tabela/evidências, Copilot e configuração OpenAI.

**Critério de saída:** jornada completa utilizável em desktop e mobile, inclusive por teclado.

## Fase 05 — Dataset, execução e pitch

**Objetivo:** tornar a apresentação reproduzível em um comando.

**Entregas:** cinco XMLs sintéticos + ZIP, fixtures extras, valor exato de R$ 1.840,00, scripts, README e pitch.

**Critério de saída:** clone limpo sobe localmente e a demo é fiel aos limites jurídicos.

## Fase 06 — Testes e validação visual

**Objetivo:** provar o fluxo de ponta a ponta e corrigir falhas antes do pitch.

**Entregas:** 17+ testes verdes, inspeção no navegador, evidências de QA e registros de debug.

**Critério de saída:** todos os controles críticos e downloads verificados, sem erro bloqueante.

## Sequência

`01 Core → 02 IA/Relatórios → 03 API → 04 SPA → 05 Demo/Docs → 06 Validação`
