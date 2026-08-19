# QA no navegador — Audita

**Data:** 19/08/2026  
**Ambiente:** Codex in-app browser, aplicação local em `http://127.0.0.1:8000`  
**Viewports:** desktop 1280 × 720 e mobile 390 × 844  
**Resultado:** APROVADO após correções

## Critérios de aceitação

| Área | Evidência observada | Resultado |
|---|---|---|
| Carregamento e console | SPA carregou com título “Audita — Inteligência fiscal explicável”; zero erros JavaScript. O único aviso é o conhecido do Tailwind Play CDN, aceitável para o protótipo do hackathon. | Aprovado |
| Demo 3 min | Botão “Demo 3 min — Oficina” processou cinco notas e abriu a área de resultados. | Aprovado |
| Transparência | Rótulos “Simulação sintética” e “5 notas sintéticas · cenário didático” visíveis; copy afirma que não é crédito garantido nem valor disponível. | Aprovado |
| Contador | Após a animação de 1.050 ms, o contador estabilizou em **R$ 1.840,00**. Os itens exibidos somam 320 + 420 + 260 + 340 + 500 = 1.840. | Aprovado |
| Confetti | Canvas fixo do `canvas-confetti` apareceu com 95 partículas no modo normal. O código respeita `prefers-reduced-motion` e elimina animação/confetti nesse modo. | Aprovado |
| KPIs | Cinco notas; receita auditada R$ 125,6 mil; receita confirmada R$ 125,6 mil; alíquota PIS/Cofins 1,4648%. | Aprovado |
| Gráfico | Canvas Chart.js visível, com nome acessível “Distribuição dos valores estimados por segmento”; fallback textual existe para indisponibilidade da CDN. | Aprovado |
| Parecer | Abas Resumo, Base legal e Plano de ação alternaram `aria-selected` e conteúdo corretamente. Base legal cita LC 123/2006, Leis 10.147/2000, 10.485/2002, 13.097/2015, CTN, Resolução CGSN 140 e IN RFB 2.055. | Aprovado |
| Busca | Busca por `87083090` reduziu a tabela à pastilha de freio; limpeza restaurou cinco linhas. | Aprovado |
| Filtros | “Confirmados” exibiu cinco linhas; “Revisar” exibiu o estado vazio; “Todos” restaurou a tabela. | Aprovado |
| Trilha de evidências | Cinco linhas com produto/nota, NCM/CFOP, CST de PIS/Cofins, CSOSN identificado separadamente como ICMS, fonte legal, pendência, status e potencial. | Aprovado |
| Copilot | Drawer abriu, recebeu foco e respondeu às perguntas rápidas “Pastilhas de freio” e “Prazo de restituição” com fontes, limites e próximo passo. Escape fechou o drawer e devolveu foco ao launcher. | Aprovado |
| Modal OpenAI | Campo `type=password`, `autocomplete=off`, copy de retenção somente em memória. Cancelar e Escape fecham o diálogo e devolvem foco a “Configurar OpenAI”. No mobile o botão mantém nome acessível por `aria-label`. | Aprovado |
| Excel | A ação concluiu sem erro e mostrou “Excel gerado para validação do contador”. A API automatizada valida status 200, assinatura ZIP/XLSX e reabertura das três abas. | Aprovado |
| PDF | A ação concluiu sem erro e mostrou “PDF gerado para validação do contador”. A API automatizada valida status 200, assinatura `%PDF` e texto extraível. | Aprovado |
| Responsividade | Em 390 px, `clientWidth=390` e `scrollWidth=390`; cards de evidência ficam entre 12 e 378 px, sem overflow horizontal. Em 1280 px, largura rolável e viewport também coincidem. | Aprovado |
| Teclado e foco | Foco visível presente; tabs, drawer e modal operáveis; Escape restaura foco nos gatilhos. | Aprovado |

## Defeitos encontrados e resolvidos

1. `06-demo-credit-mismatch.md` — falso positivo: a primeira captura leu um frame intermediário da animação. API, dataset e estado terminal estavam corretos em R$ 1.840,00. A QA passou a aguardar estabilização.
2. `06-key-modal-escape.md` — o diálogo dependia do Escape nativo. Foi adicionado fechamento idempotente com handlers explícitos de `cancel` e `keydown Escape`.
3. `06-mobile-horizontal-overflow.md` — o mínimo intrínseco do canvas expandia o grid para 491 px. `min-width:0` e `minmax(0,1fr)` eliminaram o overflow.
4. `06-mobile-config-accessible-name.md` — o breakpoint ocultava a única fonte de nome do botão. Foi adicionado `aria-label="Configurar OpenAI"`.

## Regressão automatizada

Após as correções:

- `pytest -q`: **41 aprovados**, 0 falhas;
- `tests/test_frontend_static.py`: **7 aprovados**;
- console desktop final: **0 erros**;
- console mobile final: **0 erros**.

O warning de depreciação do adaptador `httpx` do `TestClient` já está registrado em `06-AUTOMATED-QA.md` e não afeta o runtime.

## Evidências visuais

- `software/.planning/evidence/06-desktop-results.jpg` — jornada desktop completa após a demo;
- `software/.planning/evidence/06-mobile-results.jpg` — jornada mobile completa após a correção responsiva.

## Limitação da automação do navegador

O evento de download não foi exposto pelo browser-client para links Blob criados via JavaScript. O sucesso foi confirmado pela resposta visual sem erro e, de forma independente, pelos testes de integração que verificam bytes, media type e abertura dos arquivos. Não há risco funcional pendente conhecido.
