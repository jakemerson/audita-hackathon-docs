# Fase 02: IA, Copilot e relatórios — Resumo

## Resultado

Auditor e Copilot com OpenAI Responses API opcional e fallback local integral, além de XLSX auditável e PDF de memória/checklist.

## Entregas e commits

- `2a392af` — auditor estruturado e fallback;
- `c3075da` — Copilot com fontes e limites;
- `f4aeb9d` — workbook executivo;
- `d8e1e62` — memória de cálculo PDF;
- `273d230` — testes de serviços.

## Decisões

- A IA não recebe autoridade para alterar cálculos ou status.
- Chave inválida/ausente e qualquer falha de rede resultam em fallback local.
- PDF é apoio técnico e checklist, não petição.

## Verificação

6 testes de serviços aprovados; XLSX reaberto e PDF extraído por parser.
