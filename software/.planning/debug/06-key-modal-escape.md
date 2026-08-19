---
status: resolved
trigger: "Browser QA: modal de configuração deve fechar por Escape e devolver foco"
created: 2026-08-19T15:24:00-03:00
updated: 2026-08-19T15:39:00-03:00
---

## Current Focus

hypothesis: Confirmada — a função idempotente e os handlers explícitos eliminam a dependência do fechamento nativo.
test: Concluído no navegador mobile após reload e pela suíte estática.
expecting: Atingido — modal invisível/`open=false` e foco em `#openKeyModal`.
next_action: Nenhuma; regressão resolvida.

## Symptoms

expected: Com o foco no campo da chave, pressionar Escape fecha o modal e devolve o foco a "Configurar OpenAI".
actual: Escape mantém o modal visível; Cancelar fecha e devolve o foco corretamente.
errors: Nenhum erro JavaScript associado.
reproduction: Abrir "Configurar OpenAI", focar o campo e pressionar Escape por locator e por entrada de teclado real.
started: Detectado durante a validação de teclado da Fase 06-02.

## Eliminated

- hypothesis: O defeito está na restauração de foco depois que o diálogo fecha.
  evidence: O botão Cancelar fecha o diálogo e o listener `close` devolve corretamente o foco a `#openKeyModal`.
  timestamp: 2026-08-19T15:33:00-03:00

- hypothesis: O código da aplicação chama `preventDefault()` em `cancel` ou possui um handler de Escape conflitante no modal.
  evidence: Não existe listener de `cancel` nem `keydown` no modal; o único handler de Escape encontrado pertence ao drawer do Copilot. O listener `close` não cancela eventos.
  timestamp: 2026-08-19T15:33:00-03:00

- hypothesis: O elemento não foi aberto como diálogo modal.
  evidence: A abertura usa `modal.showModal()`, o campo recebe foco e a inspeção do navegador identifica o elemento visível com role `dialog`.
  timestamp: 2026-08-19T15:33:00-03:00

## Evidence

- timestamp: 2026-08-19T15:23:10-03:00
  checked: Atributos do campo e fechamento por botão.
  found: Campo `type=password`, `autocomplete=off`; Cancelar fecha e restaura foco no botão de abertura.
  implication: O problema está isolado à via de teclado Escape.

- timestamp: 2026-08-19T15:23:45-03:00
  checked: Escape enviado com API semântica e entrada de teclado do navegador.
  found: Em ambos os casos o modal permaneceu visível, sem erro no console.
  implication: A aplicação não garante o fechamento por Escape nesse ambiente.

- timestamp: 2026-08-19T15:29:00-03:00
  checked: Código completo do modal em `index.html` e `initCopilotAndReports()`.
  found: O modal é aberto com `showModal()`. Não há listener de `keydown`, `cancel` ou chamada a `preventDefault()` no diálogo. O único listener de `close` apenas restaura foco. Cancelar submete o formulário com `value="cancel"`; o handler intercepta o submit e chama `modal.close()` explicitamente.
  implication: O caminho de Escape depende 100% do comportamento nativo do `<dialog>`, enquanto os botões têm caminho explícito controlado pela aplicação.

- timestamp: 2026-08-19T15:29:00-03:00
  checked: Disponibilidade da sessão in-app neste subagente após seguir a skill Browser.
  found: O seletor explícito `iab` retornou `Browser is not available: iab` para este subagente.
  implication: A instrumentação deve ser executada pela sessão já vinculada ao agente chamador; não é válido substituir por outro navegador para diagnosticar um comportamento específico do in-app.

- timestamp: 2026-08-19T15:33:00-03:00
  checked: Reprodução comparativa final na sessão in-app por locator, entrada CUA e botão Cancelar.
  found: Escape pelas duas vias mantém o role `dialog` visível. Cancelar fecha o diálogo e o foco retorna a "Configurar OpenAI". Nenhum erro aparece no console.
  implication: O produto não oferece uma garantia explícita e interoperável de Escape no ambiente-alvo; fechamento e foco funcionam quando a aplicação chama `close()`.

- timestamp: 2026-08-19T15:33:00-03:00
  checked: Possibilidade de instrumentar eventos temporariamente na sessão do navegador.
  found: A API Playwright disponível está restrita a inspeção read-only, impedindo observar diretamente se `keydown`/`cancel` foi interceptado antes do DOM.
  implication: Não é possível atribuir com evidência a falha a um detalhe interno do navegador. Isso não altera a causa acionável confirmada: dependência exclusiva de comportamento nativo sem fallback explícito.

- timestamp: 2026-08-19T15:35:00-03:00
  checked: Correção aplicada em `app.js` e teste estático de regressão.
  found: Fechamento centralizado e idempotente; `cancel` e `keydown Escape` chamam explicitamente `close()`; o teste exige esses bindings.
  implication: O fluxo não depende mais exclusivamente do comportamento nativo do navegador.

- timestamp: 2026-08-19T15:39:00-03:00
  checked: Reprodução original após reload em 390 × 844.
  found: Escape fechou o diálogo (`open=false`) e o foco retornou a `#openKeyModal`; nenhum erro no console. Sete testes estáticos passaram.
  implication: Correção verificada no ambiente em que a falha foi observada.

## Resolution

root_cause: O modal de chave delega Escape exclusivamente ao comportamento nativo de `<dialog>`. Não há listener `cancel` nem fallback `keydown`; no navegador in-app, Escape por locator e CUA não aciona o fechamento nativo, portanto `modal.close()` nunca é chamado. O caminho explícito do botão Cancelar funciona e comprova que o fechamento e a restauração de foco estão corretos.
fix: Centralizado o fechamento em `closeKeyModal()` e adicionados handlers explícitos de `cancel` e `keydown Escape`, preservando o listener `close` que restaura o foco.
verification: Caso original passou no navegador in-app; `dialog.open=false`, foco restaurado e 7/7 testes estáticos aprovados.
files_changed: ["app/static/app.js", "tests/test_frontend_static.py"]
