# Plano 04 — SPA premium

## Objetivo

Criar uma experiência de auditoria de alto impacto, transparente, acessível e pronta para o pitch.

## Contexto visual

Seguir `../../../design-system/audita/MASTER.md` e `../../../design-system/audita/pages/audit-workspace.md`: dark glass profissional, IBM Plex Sans/Inter, Slate/Emerald, foco visível, sem excesso de neon, responsivo e com `prefers-reduced-motion`.

## Tarefas

### 04-01 — Shell, onboarding e upload

- criar HTML semântico, header, status do motor, contexto RBT12/PGDAS e dropzone acessível;
- usar CSS próprio resiliente, Tailwind Play CDN apenas como complemento;
- adicionar Lucide com fallback textual.

**Commit:** `feat(04-01): build accessible audit workspace shell`

### 04-02 — Resultado WOW responsável

- conectar upload/demo à API;
- animar potencial e confetti somente após resposta, respeitando redução de movimento;
- mostrar quatro KPIs, selo “simulação sintética” e avisos de estimativa/validação.

**Commit:** `feat(04-02): add transparent demo results experience`

### 04-03 — Evidências e visualização

- implementar donut Chart.js com fallback, parecer em abas e tabela pesquisável/filtrável;
- mostrar lei, regra, confiança, motivo, CST PIS/Cofins, CSOSN separado e pendências;
- implementar estados vazio, carregando e erro.

**Commit:** `feat(04-03): visualize evidence and audit findings`

### 04-04 — Copilot, configuração e downloads

- drawer acessível com foco/ESC, perguntas rápidas e respostas citadas;
- modal de chave com aviso de memória e campo password;
- conectar downloads reais Excel/PDF.

**Commit:** `feat(04-04): finish copilot and report actions`

### 04-05 — Testes estáticos e acessibilidade

- validar IDs, handlers, labels, teclado, responsive e motion;
- atualizar estado e resumo.

**Commit:** `test(04-05): validate SPA interactions and a11y`
