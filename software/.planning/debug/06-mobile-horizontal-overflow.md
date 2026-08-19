---
status: resolved
trigger: "Browser QA responsivo: viewport 390 px não deve ter rolagem horizontal"
created: 2026-08-19T15:26:00-03:00
updated: 2026-08-19T15:39:00-03:00
---

## Current Focus

hypothesis: Confirmada — `min-width:0` e `minmax(0,1fr)` permitem ao grid encolher até 366 px.
test: Concluído em 390 × 844 após reload, demo e screenshot.
expecting: Atingido — documento com 390 px e ambos os cards contidos entre 12 e 378 px.
next_action: Nenhuma; regressão resolvida.

## Symptoms

expected: `documentElement.scrollWidth` deve ser igual a `clientWidth` em 390 × 844.
actual: `scrollWidth=503`, `clientWidth=390`; a legenda do gráfico aparece cortada à direita.
errors: Nenhum erro JavaScript.
reproduction: Executar a demo, aplicar viewport 390 × 844 e medir a largura do documento.
started: Detectado na primeira validação responsiva da Fase 06-02.

## Eliminated

- hypothesis: Os controles do topo ou o launcher do Copilot causam o overflow.
  evidence: Suas bordas direita ficaram em 359, 370 e 378 px, dentro do viewport de 390 px.
  timestamp: 2026-08-19T15:27:00-03:00

## Evidence

- timestamp: 2026-08-19T15:25:45-03:00
  checked: Geometria do documento e screenshot em 390 × 844.
  found: Documento com 503 px de largura rolável; controles principais permanecem dentro de 390 px, mas parte da área de evidências é cortada.
  implication: O overflow nasce em conteúdo descendente, não na largura dos controles do topo.

- timestamp: 2026-08-19T15:27:00-03:00
  checked: Caixas renderizadas que ultrapassam o viewport.
  found: Os dois filhos de `.evidence-grid` mediam 491 px e seu conteúdo 453 px, embora `#results` medisse 366 px; o breakpoint usava uma faixa `1fr` com mínimo intrínseco automático.
  implication: O canvas/conteúdo define um mínimo intrínseco e expande a única coluna além do contêiner.

- timestamp: 2026-08-19T15:35:00-03:00
  checked: Correção CSS e teste estático de regressão.
  found: Filhos de `.evidence-grid` agora têm `min-width:0` e o breakpoint móvel usa `minmax(0,1fr)`.
  implication: A trilha pode encolher abaixo do mínimo intrínseco do canvas sem expandir o documento.

- timestamp: 2026-08-19T15:39:00-03:00
  checked: Demo completa após reload em 390 × 844.
  found: `clientWidth=390`, `scrollWidth=390`; os dois cards medem 366 px e terminam em 378 px; contador em R$ 1.840,00.
  implication: O overflow horizontal foi eliminado sem regressão do resultado.

## Resolution

root_cause: A única coluna responsiva de `.evidence-grid` usava `1fr`, cujo mínimo automático preservava a largura intrínseca de 491 px dos cards/canvas dentro de um contêiner de 366 px.
fix: Adicionado `min-width:0` aos filhos do grid e override móvel com `grid-template-columns:minmax(0,1fr)`.
verification: Browser in-app confirmou ausência de overflow em 390 px, cards contidos e 7/7 testes estáticos aprovados.
files_changed: ["app/static/styles.css", "tests/test_frontend_static.py"]
