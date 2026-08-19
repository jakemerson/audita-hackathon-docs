# Fase 01: Core tributário e XML — Resumo

## Resultado

Fundação Python 3.12 com cálculo determinístico do Anexo I, regras NCM versionadas, estados de confiança e parser NF-e/NFC-e independente de namespace.

## Entregas e commits

- `10a64c0` — ambiente Python e proteção de segredos;
- `e98c7a0` — modelos e motor tributário;
- `ceb386a` — parser e auditoria de lote;
- `bb27923` — 16 testes do core.

## Decisões

- Precisão `Decimal` até a borda HTTP.
- Faixas 1–5 do Anexo I no MVP; acima de R$ 3,6 milhões requer revisão do perfil.
- Somente saída confirmada e receita não segregada gera estimativa.
- Catálogo MVP é explicitamente parcial e cada achado leva fonte e ressalvas.

## Desvios tratados

- **Regra 3 — bloqueio:** o sandbox não tinha rede para pip; dependências foram instaladas no `.venv` após autorização de rede.

## Verificação

`16 passed`; Python 3.12.6; `.env` e `.venv` ignorados.
