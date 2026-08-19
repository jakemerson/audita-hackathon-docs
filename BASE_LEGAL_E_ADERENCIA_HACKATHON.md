# AuditaPix & NotaCerta — base legal e aderência ao hackathon

**Pesquisa atualizada em:** 19 de agosto de 2026  
**Escopo:** PIS/Cofins monofásicos, Simples Nacional, restituição de DAS, limites profissionais, LGPD e regras do hackathon.

> Este documento é uma pesquisa para desenho de produto e apresentação. Não substitui parecer individual de advogado ou contador registrado.

## Conclusão executiva

A tese jurídica central é válida: a empresa optante pelo Simples Nacional deve segregar a receita de revenda de produto sujeito à tributação monofásica e o PGDAS-D desconsidera, nessa receita, os percentuais de PIS e Cofins. Se o DAS foi pago a maior, pode haver restituição dos tributos federais, observado o prazo de cinco anos contado de cada pagamento.

O projeto **pode participar da trilha Pequenos Negócios**, mas a versão descrita em `IMPACTO_E_ESTUDO_ECONOMICO.md` e `Prompt.md` precisa de correções materiais antes da demo:

1. não aplicar 3,65% sobre as notas: a redução corresponde à parcela efetiva de PIS/Cofins dentro do DAS;
2. usar documentos de **venda** (NF-e/NFC-e), histórico do RBT12 e extratos/declarações do PGDAS-D; notas de compra, sozinhas, não demonstram a receita que foi tributada a maior;
3. não prometer restituição, ausência de multa ou prazo de 15 a 60 dias;
4. não chamar um PDF gerado de “petição oficial”: o pedido ordinário é eletrônico e a geração de aconselhamento/petições sem revisão profissional traz risco jurídico;
5. usar dados sintéticos ou comprovadamente autorizados na demo;
6. reposicionar a solução para **recuperação do legado até 2026 + transição para CBS/IBS**, pois PIS e Cofins serão extintos a partir de 2027.

Há ainda um erro conceitual no detector proposto em `Prompt.md`: CST 01 ou 02 na venda feita pelo fabricante/importador pode representar justamente a etapa tributada do regime monofásico e não deve ser marcada automaticamente como erro. O CST 04 descreve a **revenda posterior a alíquota zero**. Além disso, CSOSN 102/500/900 pertence ao grupo de ICMS da NF-e; não é alternativa ao CST 04 de PIS/Cofins.

## 1. Aderência às regras do hackathon

| Critério | Avaliação | Condição prática |
|---|---|---|
| Trilha “Pequenos Negócios” | **Atende** | Simplifica uma rotina fiscal cara e manual e pode gerar liquidez. |
| Projeto proibido | **Não está na lista expressa** | Não transformar o produto em chatbot genérico, RAG básico ou analisador de imagens. |
| Dashboard como funcionalidade principal | **Risco corrigível** | A demo deve mostrar o fluxo `documentos → divergência comprovada → cálculo → memória de retificação`, e não cards e gráficos como produto. |
| Inovação/originalidade | **Fraco na formulação atual** | Existem concorrentes com upload de XML/PGDAS, classificação monofásica, cálculo e relatórios. Ver `CONCORRENTES_E_INOVACAO.md`. |
| Código aberto | **Obrigatório** | Repositório público e licença compatível para todo código/dataset usado. |
| Trabalho novo | **Obrigatório** | Identificar no README e na demo exatamente o que foi implementado durante o hackathon. Hoje o repositório contém apenas documentos de ideia, o que não conflita com essa regra. |
| Equipe | **Obrigatório** | No máximo quatro integrantes. |
| Direitos sobre dados e ativos | **Atenção alta** | Não publicar XML real de terceiro. Usar XML sintético, anonimizado de forma efetiva ou autorizado. Identificá-lo claramente como “dataset sintético de demonstração”. |
| Legalidade e ética | **Condicional** | Manter contador/advogado no circuito de aprovação; não protocolar nem prometer crédito automaticamente. |

## 2. Base legal do benefício

### 2.1 Segregação no Simples Nacional

- A [Lei Complementar nº 123/2006, art. 18, § 4º-A, I](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm) determina a segregação das receitas sujeitas à tributação concentrada em uma única etapa.
- O [Manual do PGDAS-D, item 6.6.4](https://www8.receita.fazenda.gov.br/SimplesNacional/Arquivos/manual/MANUAL_PGDAS-D_2018_V4.pdf) orienta a informar a receita decorrente da venda do produto como sujeita à tributação monofásica. PIS e Cofins são desconsiderados dessa parcela; os demais tributos continuam incidindo.
- A [Solução de Consulta Cosit nº 19/2016](https://normas.receita.fazenda.gov.br/sijut2consulta/anexoOutros.action?idArquivoBinario=39319) confirma, para produtos da Lei nº 10.147/2000, que a redução independe de o fornecedor ser industrial, importador, atacadista ou varejista.
- A [Solução de Consulta Cosit nº 202/2014](https://normas.receita.fazenda.gov.br/sijut2consulta/anexoOutros.action?idArquivoBinario=31562) confirma a desconsideração dos percentuais de PIS/Cofins no Anexo I para revenda de produtos farmacêuticos, de perfumaria e higiene pessoal sujeitos ao regime.

### 2.2 Leis por grupo de produtos

- [Lei nº 10.485/2002](https://www.planalto.gov.br/ccivil_03/leis/2002/l10485.htm): veículos, autopeças dos Anexos I e II, pneus e câmaras de ar. Os arts. 3º, § 2º, e 5º, parágrafo único, reduzem a zero as alíquotas na etapa atacadista/varejista aplicável.
- [Lei nº 10.147/2000](https://www.planalto.gov.br/ccivil_03/leis/l10147.htm): produtos farmacêuticos, de perfumaria, toucador e higiene pessoal expressamente abrangidos; o art. 2º trata da alíquota zero nas etapas posteriores.
- [Lei nº 13.097/2015, arts. 14 a 39](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13097.htm): bebidas frias; o art. 28 reduz a zero as alíquotas na receita da pessoa jurídica varejista e o § 2º inclui optantes do Simples Nacional.

**Limitação técnica importante:** NCM isolado nem sempre basta. As leis contêm posições, subposições, códigos “Ex”, descrições, destinações e exceções. Uma auditoria de cinco anos também precisa versionar NCM/TIPI e a regra vigente na data de cada operação. A IA pode sugerir classificação, mas a decisão que gera valor recuperável deve vir de regra determinística versionada e deixar evidência da fonte.

### 2.3 CST e CSOSN: como não gerar falsos positivos

O [Guia Prático da EFD-Contribuições](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/manuais/sped/manuais-efd-contribuicoes/versao-atual/guia_pratico_efd_contribuicoes_versao_1_35-18_06_2021.pdf) define, separadamente para PIS e Cofins:

- CST 01: operação tributável com alíquota básica;
- CST 02: operação tributável com alíquota diferenciada;
- CST 03: operação tributável por unidade de produto;
- CST 04: operação tributável monofásica — **revenda a alíquota zero**.

Logo, CST 01/02/03 pode ser coerente na saída do fabricante/importador, enquanto CST 04 é coerente na saída do revendedor alcançado pela alíquota zero. Para decidir, o motor precisa conhecer o papel do emitente, a operação, o produto e a regra vigente — não apenas procurar um código.

O [Manual de Orientação do Contribuinte da NF-e](https://www.nfe.fazenda.gov.br/portal/exibirArquivo.aspx?conteudo=HO2V+vzhFBk%3D) coloca CST/CSOSN no grupo de **ICMS** conforme o regime do emissor, enquanto PIS e Cofins possuem grupos e CST próprios. Portanto, CSOSN não pode ser tratado como se fosse um CST de PIS/Cofins.

## 3. Como o cálculo correto funciona

Para comércio no Anexo I:

```text
Alíquota efetiva do Simples =
  (RBT12 × alíquota nominal da faixa − parcela a deduzir) ÷ RBT12

Parcela efetiva de PIS/Cofins =
  alíquota efetiva do Simples × percentual de repartição de PIS/Cofins da faixa

Pagamento potencialmente a maior no mês =
  receita de revenda monofásica que não foi segregada × parcela efetiva de PIS/Cofins
```

Nas cinco primeiras faixas do Anexo I, PIS (2,76%) + Cofins (12,74%) representam **15,5% da alíquota efetiva do DAS**, não 3,65% da receita. O [Anexo I da LC nº 123/2006](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm) e o [exemplo oficial do Manual do PGDAS-D](https://www8.receita.fazenda.gov.br/simplesnacional/arquivos/manual/manual_pgdas-d_2018_v4.pdf) demonstram essa partilha.

Consequência: o percentual fixo de 3,65% usado no estudo econômico superestima os exemplos apresentados. O recálculo está em `ESTATISTICAS_E_ECONOMIA.md`.

## 4. Quais documentos sustentam o crédito

O fato gerador relevante é a **receita da revenda**. Portanto, uma apuração defensável deve reconciliar, por período:

1. NF-e/NFC-e de saída e outros documentos que representem as vendas;
2. cadastro de produtos e enquadramento legal vigente por data;
3. extrato/declaração PGDAS-D original e, se existente, retificadora;
4. RBT12 e faixa efetivamente usados no mês;
5. DAS efetivamente pago;
6. memória que compare o declarado com o que deveria ter sido segregado.

XMLs de entrada podem ajudar a enriquecer o cadastro, mas **não provam quanto daquele estoque foi vendido em cada mês**. Além disso, a Cosit nº 19/2016 deixa claro que o regime tributário do fornecedor não define o direito do varejista. Logo, “CST errado do fornecedor” não deve ser apresentado como condição jurídica necessária para a recuperação.

Para bares, restaurantes, oficinas e pet shops, também é necessário separar venda de mercadoria de prestação de serviço e evitar inferir que toda compra virou receita monofásica no mesmo período.

## 5. Restituição e prazo de cinco anos

- O [CTN, arts. 165 e 168](https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm) prevê restituição de pagamento indevido/a maior e prazo de cinco anos contado da extinção do crédito tributário. É uma janela móvel por pagamento, não um direito automático a “60 vezes o faturamento atual”.
- A [Resolução CGSN nº 140/2018, arts. 128 a 130](https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=92278) disciplina restituição no Simples e atribui o pedido ao ente responsável pelo tributo.
- A [IN RFB nº 2.055/2021, art. 13](https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=122002&visao=anotado) determina que pagamento a maior em DAS seja solicitado pelo Pedido Eletrônico de Restituição no Portal do Simples/e-CAC.
- O [serviço oficial de restituição do Simples/MEI](https://www.gov.br/pt-br/servicos/obter-restituicao-de-tributos-do-simples-nacional-e-mei) informa que análise e pagamento são automatizados, mas apresenta o tempo como **“não estimado ainda”**.
- O [Manual da Restituição](https://www8.receita.fazenda.gov.br/SimplesNacional/Arquivos/manual/MANUAL_RESTITUICAO_MEI.pdf) informa que os tributos federais podem ser restituídos e que deve existir um pedido para cada DAS. Ele também alerta que pedir restituição sem pagamento indevido pode provocar cobrança do débito original.
- Desde 2023, o sistema aceita [Pix, conta corrente, conta de pagamento ou poupança](https://www8.receita.fazenda.gov.br/SIMPLESNACIONAL/Noticias/NoticiaCompleta.aspx?id=0aee78f5-c0da-433f-9b01-63f8f5d285be).
- A atualização ocorre pela Selic desde o mês subsequente ao pagamento até o mês anterior à restituição, mais 1% no mês do pagamento, conforme a [Receita Federal](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/restituicao-ressarcimento-reembolso-e-compensacao/restituicao/atualizacao-das-restituicoes-compensacoes).

### Correções de afirmações do estudo original

| Afirmação original | Situação após pesquisa |
|---|---|
| “Direito inalienável aos últimos 60 meses” | O direito existe, mas está sujeito à comprovação e ao prazo móvel de cinco anos por pagamento. “Inalienável” é linguagem inadequada. |
| “Processo 100% administrativo” | Em regra, sim, para o pedido federal após a correção das apurações; divergências podem gerar exigências ou litígio. |
| “Petição administrativa oficial necessária” | Não é o fluxo ordinário do pedido eletrônico em DAS. Um dossiê/memória de cálculo é mais útil para a demo. |
| “15 a 60 dias úteis” | **Não comprovado.** O serviço oficial não estima duração. |
| “Sem risco de multa” | **Remover.** Retificar é permitido, mas erro, falsidade ou restituição indevida pode gerar cobrança e outras consequências. |
| “Via Pix” | Confirmado como uma das formas aceitas, sem garantia de data ou deferimento. |
| “Cosit nº 225/2014 e nº 394/2017 apoiam a tese” | **Citações incorretas.** A nº 225/2014 trata de remessas/afretamento e a nº 394/2017 de cessão de mão de obra. Usar Cosit nº 19/2016, nº 202/2014 e, para situações específicas de autopeças industrializadas por encomenda, nº 461/2017. |
| “CST 01/02/49/99 ou CSOSN genérico no XML prova pagamento em dobro” | **Incorreto.** CST tributável pode ser correto na etapa concentrada; CSOSN é de ICMS; e o pagamento a maior no Simples é comprovado pela receita de revenda não segregada no PGDAS e pelo DAS pago. |
| “Bitributação” | Como slogan é impreciso. Juridicamente, o caso é melhor descrito como **pagamento indevido ou a maior por falta de segregação de receita monofásica**, não a clássica bitributação por entes distintos sobre o mesmo fato. |

## 6. Reforma tributária: prazo de validade da proposta atual

A [Receita Federal](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/entenda) informa que PIS e Cofins serão extintos a partir de 2027 e substituídos pela CBS. Empresas do Simples poderão recolher IBS/CBS dentro do regime ou optar pelo regime regular. O [CGSN já definiu os prazos de opção para 2027](https://www8.receita.fazenda.gov.br/SimplesNacional/Noticias/NoticiaCompleta.aspx?id=c739e03c-8482-473f-8e82-f38ec3b13637).

Isso não extingue o valor do produto: pagamentos pretéritos ainda podem ser revistos dentro do prazo. Mas transforma a tese em um produto de **recuperação de legado com vida útil decrescente**. Para ser sustentável e inovador, o motor deve também explicar a migração para CBS/IBS e preservar o rastreamento das regras históricas.

## 7. Limites profissionais e LGPD

### Jurídico e contábil

- A [Lei nº 8.906/1994, art. 1º, II](https://www.planalto.gov.br/ccivil_03/leis/l8906.htm) reserva consultoria, assessoria e direção jurídicas à advocacia.
- O [Decreto-Lei nº 9.295/1946, art. 25](https://www.planalto.gov.br/ccivil_03/decreto-lei/del9295.htm) e a [Resolução CFC nº 1.640/2021](https://cfc.org.br/noticias/resolucao-sobre-prerrogativas-profissionais-de-contadores-e-de-tecnicos-em-contabilidade-e-atualizada/) disciplinam trabalhos técnicos de contabilidade e atribuições dos profissionais registrados.

Para reduzir risco, o produto deve:

- declarar “diagnóstico preliminar” e não “parecer pericial definitivo”;
- exigir aprovação identificada de contador antes de produzir a memória final de retificação;
- oferecer apenas modelo editável de manifestação jurídica, quando necessário, sujeito à revisão de advogado;
- não transmitir retificação ou pedido em nome do cliente durante a demo;
- mostrar confiança, ambiguidade e fonte por item, permitindo rejeição humana.

### Dados pessoais e sigilo empresarial

XMLs podem conter nome, CPF, endereço e outros dados de pessoas naturais, além de informação comercial confidencial. A [LGPD, arts. 6º, 7º e 46](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm) exige finalidade, necessidade, base legal e medidas técnicas/administrativas de segurança. A [ANPD](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-2-de-27-de-janeiro-de-2022) mantém deveres mínimos de segurança mesmo para agentes de pequeno porte.

Requisitos mínimos para a demo/produto:

- processamento local ou retenção curta e explícita;
- criptografia em trânsito e em repouso;
- exclusão automática dos arquivos após o processamento;
- mascaramento de CPF/CNPJ, nomes, chaves de acesso e endereços em logs;
- não enviar o XML integral ao modelo quando somente os campos tributários forem necessários;
- informar finalidade, base legal, operadores/suboperadores e canal do titular;
- proibir datasets reais no repositório público.

## 8. Fluxo recomendado para uma demo legalmente defensável

```text
Dataset sintético de vendas + PGDAS original
        ↓
Parser reconstrói a receita por item e período
        ↓
Motor determinístico versionado cita lei/NCM/regra por data
        ↓
Comparação: declarado × segregação correta × DAS efetivamente pago
        ↓
Fila de ambiguidades para revisão do contador
        ↓
Memória de cálculo + checklist de retificação + trilha de evidências
```

O “fator wow” deve ser a explicabilidade verificável: o jurado clica em um item e vê documento, período, regra vigente, cálculo e impacto, além da transição correspondente para 2027. Pix e confete podem existir na interface, mas não devem ser tratados como resultado garantido.

## Fontes consultadas

### Regras do evento

- [`regras_hackathon.md`](regras_hackathon.md), fornecido pelo participante.

### Legislação e orientação tributária oficial

- [Lei Complementar nº 123/2006 — Planalto](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm)
- [Código Tributário Nacional — Lei nº 5.172/1966 — Planalto](https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm)
- [Lei nº 10.485/2002 — autopeças e pneus — Planalto](https://www.planalto.gov.br/ccivil_03/leis/2002/l10485.htm)
- [Lei nº 10.147/2000 — farmacêuticos, perfumaria e higiene — Planalto](https://www.planalto.gov.br/ccivil_03/leis/l10147.htm)
- [Lei nº 13.097/2015 — bebidas frias — Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13097.htm)
- [Resolução CGSN nº 140/2018 — Receita Federal](https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=92278)
- [IN RFB nº 2.055/2021 — Receita Federal](https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=122002&visao=anotado)
- [Manual do PGDAS-D — Portal do Simples Nacional](https://www8.receita.fazenda.gov.br/SimplesNacional/Arquivos/manual/MANUAL_PGDAS-D_2018_V4.pdf)
- [Guia Prático da EFD-Contribuições — CST de PIS/Cofins](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/manuais/sped/manuais-efd-contribuicoes/versao-atual/guia_pratico_efd_contribuicoes_versao_1_35-18_06_2021.pdf)
- [Manual de Orientação do Contribuinte da NF-e — grupos CST/CSOSN e PIS/Cofins](https://www.nfe.fazenda.gov.br/portal/exibirArquivo.aspx?conteudo=HO2V+vzhFBk%3D)
- [Perguntas e Respostas do Simples Nacional](https://www8.receita.fazenda.gov.br/SimplesNacional/Arquivos/manual/PerguntaoSN.pdf)
- [Manual da Restituição do Simples Nacional e Simei](https://www8.receita.fazenda.gov.br/SimplesNacional/Arquivos/manual/MANUAL_RESTITUICAO_MEI.pdf)
- [Serviço oficial: obter restituição do Simples Nacional e MEI](https://www.gov.br/pt-br/servicos/obter-restituicao-de-tributos-do-simples-nacional-e-mei)
- [Atualização das restituições e compensações — Receita Federal](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/restituicao-ressarcimento-reembolso-e-compensacao/restituicao/atualizacao-das-restituicoes-compensacoes)
- [Pedido eletrônico passou a aceitar Pix — Portal do Simples Nacional](https://www8.receita.fazenda.gov.br/SIMPLESNACIONAL/Noticias/NoticiaCompleta.aspx?id=0aee78f5-c0da-433f-9b01-63f8f5d285be)
- [Solução de Consulta Cosit nº 19/2016](https://normas.receita.fazenda.gov.br/sijut2consulta/anexoOutros.action?idArquivoBinario=39319)
- [Solução de Consulta Cosit nº 202/2014](https://normas.receita.fazenda.gov.br/sijut2consulta/anexoOutros.action?idArquivoBinario=31562)
- [Solução de Consulta Cosit nº 461/2017](https://normas.receita.fazenda.gov.br/sijut2consulta/anexoOutros.action?idArquivoBinario=45605)
- [Reforma Tributária do Consumo — Receita Federal](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/entenda)
- [Opção do Simples e IBS/CBS para 2027 — Portal do Simples Nacional](https://www8.receita.fazenda.gov.br/SimplesNacional/Noticias/NoticiaCompleta.aspx?id=c739e03c-8482-473f-8e82-f38ec3b13637)

### Limites profissionais e proteção de dados

- [Estatuto da Advocacia — Lei nº 8.906/1994 — Planalto](https://www.planalto.gov.br/ccivil_03/leis/l8906.htm)
- [Decreto-Lei nº 9.295/1946 — profissão contábil — Planalto](https://www.planalto.gov.br/ccivil_03/decreto-lei/del9295.htm)
- [Resolução CFC nº 1.640/2021 — notícia e link oficial do CFC](https://cfc.org.br/noticias/resolucao-sobre-prerrogativas-profissionais-de-contadores-e-de-tecnicos-em-contabilidade-e-atualizada/)
- [Lei Geral de Proteção de Dados — Lei nº 13.709/2018 — Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm)
- [Resolução CD/ANPD nº 2/2022 — agentes de pequeno porte](https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-2-de-27-de-janeiro-de-2022)
