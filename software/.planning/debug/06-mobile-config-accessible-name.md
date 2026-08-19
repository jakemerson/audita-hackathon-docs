---
status: resolved
trigger: "Browser QA mobile: botão de configuração precisa manter nome acessível"
created: 2026-08-19T15:37:00-03:00
updated: 2026-08-19T15:39:00-03:00
---

## Current Focus

hypothesis: Confirmada — o nome explícito permanece acessível quando o `span` visual é ocultado.
test: Concluído por role/name em 390 px e teste estático.
expecting: Atingido — o controle resolve uma correspondência visível.
next_action: Nenhuma; regressão resolvida.

## Symptoms

expected: O botão compacto de chave deve continuar anunciado como "Configurar OpenAI".
actual: O botão permanece visível, mas não é encontrado pelo nome acessível no breakpoint móvel.
errors: Nenhum erro JavaScript.
reproduction: Aplicar viewport 390 × 844 e localizar o botão pelo role/name.
started: Detectado no reteste do modal após correção responsiva.

## Eliminated

Nenhuma hipótese eliminada.

## Evidence

- timestamp: 2026-08-19T15:36:45-03:00
  checked: HTML renderizado e seletor semântico em 390 px.
  found: O botão existe por `#openKeyModal`, mas o `span` é `display:none` e não há `aria-label`; a busca por role/name retorna zero correspondências.
  implication: O nome dependia exclusivamente do conteúdo visual ocultado pelo CSS.

- timestamp: 2026-08-19T15:39:00-03:00
  checked: Botão após reload em 390 × 844.
  found: A busca por role/button e nome "Configurar OpenAI" retorna uma correspondência visível; o foco restaurado mantém o mesmo rótulo.
  implication: O controle compacto é novamente identificável por tecnologia assistiva.

## Resolution

root_cause: O breakpoint esconde `.header-actions .button span`, removendo da árvore acessível a única fonte de nome do controle.
fix: Adicionado `aria-label="Configurar OpenAI"` ao botão.
verification: Browser mobile encontrou o controle por role/name e 7/7 testes estáticos passaram.
files_changed: ["app/static/index.html", "tests/test_frontend_static.py"]
