# Audita

## Visão

Audita é uma plataforma de apoio à auditoria de receitas monofásicas de PIS/Cofins para pequenos negócios optantes pelo Simples Nacional. O produto cruza documentos fiscais, regras tributárias versionadas e contexto do PGDAS-D para identificar indícios de receita não segregada, explicar cada achado e produzir memória de cálculo para validação profissional.

## Problema

Pequenos varejistas frequentemente não possuem equipe tributária nem uma trilha de evidências que conecte NCM, descrição, destinação, CST de PIS/Cofins, receita de venda e declaração no PGDAS-D. Isso pode levar a recolhimento indevido ou a maior. XML de compra, NCM ou CST isolados não comprovam um crédito.

## Proposta de valor

- analisar XMLs de NF-e/NFC-e em lote, inclusive ZIP;
- classificar itens com regras legais versionadas e estados `CONFIRMADO`, `REVISAR` e `NAO_ENQUADRADO`;
- estimar somente o componente de PIS/Cofins do DAS sobre receita monofásica não segregada;
- mostrar a trilha de evidências, as premissas e as pendências de validação;
- gerar planilha e memória de cálculo/checklist em PDF;
- oferecer um Copilot Fiscal com IA e fallback local, sempre citando fontes e limites;
- manter o contador de demonstração em exatamente R$ 1.840,00, identificado como simulação sintética.

## Usuários

- dono ou gestor de pequeno varejo;
- contador responsável pelo Simples Nacional;
- consultor tributário que prepara revisão documental;
- advogado, quando houver manifestação jurídica.

## Princípios obrigatórios

1. Não chamar o fenômeno de bitributação como conclusão jurídica; usar “potencial pagamento indevido ou a maior”.
2. Não prometer restituição, prazo, ausência de risco ou pagamento imediato via Pix.
3. Não considerar CST/CSOSN ou XML de compra como prova suficiente.
4. Separar ICMS/CSOSN de PIS/Cofins/CST.
5. Calcular o potencial com a alíquota efetiva do Simples e a fração de PIS/Cofins do Anexo I, não com 3,65% fixos.
6. Requerer contexto do PGDAS-D; se a receita já foi segregada, o potencial recuperável é zero.
7. Exigir validação do contador antes de retificação ou pedido; documentos gerados não são petição nem parecer jurídico.
8. Preservar privacidade: chave de IA apenas em memória, sem log; fallback local completo; fixtures sintéticas e identificadas.

## Base normativa de referência

- Lei Complementar nº 123/2006, art. 18, § 4º-A, I;
- CTN, arts. 165 e 168;
- Resolução CGSN nº 140/2018;
- IN RFB nº 2.055/2021;
- Leis nº 10.147/2000, 10.485/2002 e 13.097/2015;
- listas, exceções, destinação e vigência detalhadas em `../NCM_MONOFASICO_REGRAS_E_FONTES.md`.

## Arquitetura

- backend: Python 3.12, FastAPI, Pydantic, lxml;
- regras: `Decimal`, tabelas versionadas e explicações determinísticas;
- IA: OpenAI Responses API com `gpt-4o-mini` quando configurado, fallback local quando não;
- relatórios: OpenPyXL e ReportLab;
- frontend: SPA em HTML/CSS/JavaScript, Tailwind Play CDN, Chart.js, Lucide e canvas-confetti;
- testes: pytest, pytest-asyncio e httpx.

## Fora do escopo do MVP

- transmitir PGDAS-D, PER/DCOMP ou pedidos à Receita Federal;
- assinar documentos ou emitir parecer jurídico;
- afirmar uma lista universal e eterna de NCMs sem vigência e exceções;
- armazenar XML, chave OpenAI ou dados pessoais em banco;
- garantir deferimento ou disponibilidade de valores.

## Critério de sucesso da demo

Em até três minutos, o usuário carrega o lote sintético da oficina, vê o potencial estimado de R$ 1.840,00, entende de onde veio o número, identifica itens que exigem revisão e baixa Excel/PDF. Toda tela deixa explícito que a decisão depende de documentos, PGDAS-D e validação do contador.
