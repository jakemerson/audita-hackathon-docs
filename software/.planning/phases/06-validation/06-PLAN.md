# Plano 06 — Qualidade e validação visual

## Objetivo

Executar testes completos e validar a jornada real no navegador antes da apresentação.

## Tarefas

### 06-01 — Suíte completa

- garantir ao menos 17 testes coletados e 100% aprovados;
- rodar testes com warnings visíveis e checar importação/compilação;
- registrar/corrigir qualquer bug em `.planning/debug/`.

**Commit:** `test(06-01): complete automated verification suite`

### 06-02 — Browser subagent

- iniciar aplicação em `http://localhost:8000`;
- validar botão Demo, confetti ou seu modo reduzido, contador R$ 1.840,00, abas, Chart.js/fallback, busca, filtro, drawer, perguntas rápidas, modal e downloads;
- testar viewport desktop e mobile, console e erros de rede;
- registrar evidências em `06-BROWSER-QA.md`.

**Commit:** `test(06-02): document browser acceptance results`

### 06-03 — Fechamento

- corrigir defeitos remanescentes com commits separados;
- atualizar `STATE.md`, matriz de requisitos e criar `06-SUMMARY.md`;
- confirmar árvore Git sem incorporar alterações externas ao software.

**Commit:** `docs(06-03): close Audita MVP milestone`

## Critério final

- 17+ testes verdes;
- demo exibe `R$ 1.840,00` como potencial estimado de uma simulação sintética;
- Excel e PDF baixam e abrem;
- nenhum segredo está versionado;
- todos os requisitos estão satisfeitos ou explicitamente documentados.
