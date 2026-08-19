# QA automatizado — 19/08/2026

## Resultado

- Python: 3.12.6
- Testes coletados: 41
- Aprovados: 41
- Falhas: 0
- Compilação Python: aprovada
- Sintaxe JavaScript (`node --check`): aprovada

## Cobertura comportamental

- fórmula e faixas do Anexo I, arredondamento e segregação PGDAS-D;
- regras NCM, exceções, produto usado e separação CST/CSOSN;
- NF-e/NFC-e com namespaces, XML malformado, DTD e lote;
- fallback OpenAI/Copilot, workbook e PDF;
- healthcheck, segredo em memória, upload, ZIP traversal e downloads;
- semântica/a11y estática, responsive e reduced motion;
- cinco fixtures sintéticas, ZIP físico e resultado exato de R$ 1.840,00.

## Warning conhecido

Starlette 1.6 emite aviso de depreciação do adaptador `httpx` em `TestClient`. Não afeta execução, produção ou resultado; será acompanhado na atualização coordenada FastAPI/Starlette.
