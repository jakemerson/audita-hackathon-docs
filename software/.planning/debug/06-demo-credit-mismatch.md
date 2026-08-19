---
status: resolved
trigger: "Browser QA: Demo 3 min deve apresentar exatamente R$ 1.840,00"
created: 2026-08-19T15:18:05-03:00
updated: 2026-08-19T15:24:00-03:00
---

## Current Focus

hypothesis: Confirmada — a validação amostrou um frame intermediário da animação ease-out de 1.050 ms e o classificou incorretamente como valor final.
test: Concluído com inspeção do caminho API → JSON → `renderResults` → `animateMoney`, testes determinísticos e cálculo inverso do easing.
expecting: Confirmado — API e itens totalizam R$ 1.840,00; R$ 1.581,24 é compatível com ~407 ms da animação; o DOM chega a R$ 1.840,00 após o término.
next_action: Ajustar a validação de navegador para esperar o estado terminal (polling por R$ 1.840,00 ou sinal explícito de fim), se desejado em uma tarefa de correção separada.

## Symptoms

expected: Ao acionar "Demo 3 min — Oficina", o contador principal deve terminar em R$ 1.840,00.
actual: O contador principal termina em R$ 1.581,24, embora o toast/parecer mencione R$ 1.840,00.
errors: Nenhum erro JavaScript; há apenas o aviso conhecido do Tailwind CDN.
reproduction: Abrir http://127.0.0.1:8000, acionar "Demo 3 min — Oficina" e observar o banner após a animação.
started: Detectado na primeira execução da validação visual da Fase 06-02.

## Eliminated

- hypothesis: A API, o dataset e o frontend usam bases diferentes para o valor do contador e para os demais componentes.
  evidence: A rota impõe total 1840, os cinco itens somam 1840, o JSON testado contém `"1840.00"` e `renderResults` passa exatamente esse campo como alvo de `animateMoney`.
  timestamp: 2026-08-19T15:24:00-03:00

- hypothesis: O cálculo tributário ou o arredondamento das cinco fixtures produz R$ 1.581,24.
  evidence: A execução real retornou itens de R$ 320,00, R$ 420,00, R$ 260,00, R$ 340,00 e R$ 500,00, totalizando R$ 1.840,00; os cinco testes da demo passaram.
  timestamp: 2026-08-19T15:24:00-03:00

## Evidence

- timestamp: 2026-08-19T15:16:59-03:00
  checked: Estado inicial, console e DOM.
  found: Aplicação carregou sem erros; somente aviso do Tailwind CDN.
  implication: O problema não decorre de uma falha geral de carregamento.

- timestamp: 2026-08-19T15:17:34-03:00
  checked: Resultado visual imediatamente após acionar a demo.
  found: Confetti ativo, rótulo "Simulação sintética", cinco notas e contador em R$ 1.581,24; toast menciona R$ 1.840,00.
  implication: Há uma inconsistência determinística entre componentes da mesma resposta.

- timestamp: 2026-08-19T15:19:18-03:00
  checked: Busca estática inicial por valores e caminhos envolvidos na demo.
  found: A API contém uma guarda explícita para total igual a 1840; os testes exigem `estimated_overpayment == "1840.00"`; o frontend passa esse campo como alvo para `animateMoney`.
  implication: A divergência provavelmente não é entre fontes de dados; o próximo ponto de corte é o estado transitório da animação.

- timestamp: 2026-08-19T15:19:18-03:00
  checked: Nova medição temporal fornecida pela validação do navegador.
  found: Aos 250 ms o DOM exibiu R$ 1.581,24; aos 1,25 s exibiu R$ 1.840,00; os cinco itens somam R$ 1.840,00.
  implication: A observação original capturou um frame intermediário e não o estado terminal; falta confirmar o mecanismo e a duração no código.

- timestamp: 2026-08-19T15:21:00-03:00
  checked: Implementação integral da rota `demo_workshop`, do cálculo agregado e da função `animateMoney`.
  found: A rota calcula o lote e rejeita qualquer total diferente de 1840; o frontend recebe `report.estimated_overpayment` como alvo. `animateMoney` dura 1.050 ms e, a cada `requestAnimationFrame`, grava `target * (1 - (1 - progress)^4)` no mesmo nó; somente em `progress == 1` grava o alvo integral.
  implication: Durante aproximadamente um segundo é esperado observar valores menores que R$ 1.840,00. Não há segunda base de cálculo no frontend nem valor literal R$ 1.581,24.

- timestamp: 2026-08-19T15:22:00-03:00
  checked: Primeira tentativa de executar testes e cálculo isolado.
  found: O comando foi iniciado dentro de `software/`, mas referenciou erroneamente `software/.venv/bin/python`; nenhum teste nem código da aplicação chegou a executar.
  implication: Falha do comando de diagnóstico, sem relação com o produto; repetir com `.venv/bin/python`.

- timestamp: 2026-08-19T15:24:00-03:00
  checked: Suíte `tests/test_demo.py` no ambiente virtual e execução direta do auditor sobre as cinco fixtures.
  found: Cinco testes passaram. O resumo retornou R$ 1.840,00; os itens retornaram R$ 320,00, R$ 420,00, R$ 260,00, R$ 340,00 e R$ 500,00.
  implication: Dataset, parser, regras, agregação e rota de demo estão calibrados; a aplicação não termina em R$ 1.581,24.

- timestamp: 2026-08-19T15:24:00-03:00
  checked: Cálculo inverso da curva `eased = 1 - (1 - progress)^4` para alvo 1840 e observação 1581,24.
  found: R$ 1.581,24 equivale a 85,9369565% do alvo, ou `progress = 0,3876216`, isto é, aproximadamente 407 ms dentro da animação de 1.050 ms; em `progress = 1`, a função produz exatamente 1840.
  implication: O valor reportado é matematicamente um estado transitório plausível da animação, não uma divergência fiscal.

- timestamp: 2026-08-19T15:24:00-03:00
  checked: Amostra terminal do DOM registrada pela validação do navegador.
  found: Aos 1,25 s o nó do contador mostra exatamente R$ 1.840,00.
  implication: O sintoma original foi uma falsa detecção causada por timing da automação/inspeção.

## Resolution

root_cause: A validação visual leu `#potentialAmount` enquanto `animateMoney` ainda atualizava o nó via `requestAnimationFrame`. A função usa duração fixa de 1.050 ms e easing quartic-out; R$ 1.581,24 corresponde a aproximadamente 407 ms de progresso, enquanto o estado terminal é R$ 1.840,00. Não existe discrepância entre API, dataset e frontend.
fix: Não aplicado — investigação executada em modo `find_root_cause_only`. Direção recomendada: a automação deve aguardar `#potentialAmount` atingir `R$ 1.840,00`/estabilizar após a animação, ou a UI deve expor um marcador determinístico de término da animação para testes.
verification: Cinco testes da demo passaram; auditor direto somou R$ 1.840,00; cálculo inverso reproduziu R$ 1.581,24 como frame intermediário; navegador confirmou R$ 1.840,00 aos 1,25 s.
files_changed: []
