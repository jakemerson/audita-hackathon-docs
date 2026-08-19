# Resumo 06 — Qualidade e validação visual

## Resultado

Marco MVP aprovado. A suíte terminou com **41/41 testes verdes**, a compilação Python e a sintaxe JavaScript foram validadas, e o cenário sintético retornou novamente **R$ 1.840,00** na verificação final.

## Browser QA

O browser subagent percorreu a aplicação em 1280 × 720 e 390 × 844. Foram confirmados:

- demo, contador terminal, confetti e quatro KPIs;
- gráfico Chart.js com fallback textual;
- abas do parecer, busca e filtros;
- trilha de evidências e separação entre CST PIS/Cofins e CSOSN/ICMS;
- Copilot, perguntas rápidas, foco e Escape;
- configuração OpenAI sem persistência;
- geração de Excel e PDF;
- ausência de overflow horizontal em desktop e mobile.

As evidências estão em `06-BROWSER-QA.md` e em `.planning/evidence/`.

## Defeitos tratados

- `06-demo-credit-mismatch.md`: falso positivo causado por leitura durante a animação; estado terminal confirmado.
- `06-key-modal-escape.md`: fechamento explícito e restauração de foco.
- `06-mobile-horizontal-overflow.md`: correção do mínimo intrínseco do grid.
- `06-mobile-config-accessible-name.md`: nome acessível persistente no breakpoint móvel.

## Limites conhecidos

- Tailwind Play CDN emite aviso apropriado ao protótipo; CSS próprio mantém a interface utilizável.
- O browser-client não expôs o evento de download Blob. Bytes, tipos e abertura dos arquivos foram verificados nos testes de integração.
- O catálogo NCM é um subconjunto operacional versionado; não substitui a lista oficial vigente nem a validação profissional.

## Verificação final

```text
41 passed, 1 warning in 0.81s
compileall: aprovado
node --check: aprovado
demo=1840.00
```
