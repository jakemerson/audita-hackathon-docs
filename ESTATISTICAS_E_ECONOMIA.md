# AuditaPix & NotaCerta — estatísticas e economia potencial

**Pesquisa atualizada em:** 19 de agosto de 2026  
**Regra metodológica:** dados observados são separados de hipóteses e simulações. Valores de marketing de fornecedores não são tratados como estatística independente.

## Conclusão em uma frase

Existe mercado relevante e o cálculo jurídico pode gerar economia material, mas **não foi encontrada estatística pública confiável que demonstre quantas empresas deixam de segregar receitas monofásicas, qual o percentual médio pago a maior ou o crédito médio por empresa**. Os números de 80%, quatro milhões e 3%–4,5% do estudo original não têm sustentação encontrada e devem ser removidos do pitch.

## 1. Dados reais encontrados

| Indicador observado | Valor | Data/base | Como pode ser usado |
|---|---:|---|---|
| Pessoas jurídicas ativas classificadas no programa Receita Sintonia | **10.892.593** | junho de 2026 | Dimensão do universo empresarial formal classificado, não do público elegível. |
| Optantes do Simples nas cinco faixas divulgadas pelo Receita Sintonia | **6.143.860** | junho de 2026 | Soma de 1.274.960 A+, 1.691.818 A, 1.267.097 B, 983.862 C e 926.123 D. Não equivale a empresas com PIS/Cofins monofásicos pagos a maior. |
| Emissores de NF-e exibidos pelo Portal Nacional da NF-e | **2,941 milhões** | consulta em 19/08/2026 | Demonstra escala da infraestrutura documental, não o número de clientes elegíveis. |
| NF-e autorizadas exibidas pelo Portal Nacional | **59,941 bilhões** | consulta em 19/08/2026 | Demonstra volume de documentos; o portal apresenta contador acumulado. |
| Série oficial da Selic acumulada no mês | **SGS 4390** | mensal; disponível até julho de 2026 na consulta | Permite estimar a atualização de pagamentos pretéritos, com as ressalvas abaixo. |

O Portal do Simples também oferece [estatísticas de optantes por CNAE, UF e município](https://www8.receita.fazenda.gov.br/simplesnacional/aplicacoes/atbhe/estatisticassinac.app/default.aspx). Esse é o caminho correto para dimensionar segmentos específicos, mas o painel interativo não publica uma medida de “pagamento monofásico indevido”.

### O que esses números não provam

- Os 6,14 milhões não são o TAM do produto: muitos não revendem produtos monofásicos; outros segregam corretamente; MEI e empresas sem vendas elegíveis não devem ser incluídos.
- Quantidade de NF-e não mede pagamento indevido.
- Nota classificada com CST incomum não prova erro no PGDAS-D.
- Uma classificação de conformidade tributária baixa no Receita Sintonia não pode ser atribuída a PIS/Cofins monofásicos.

## 2. Dados reais que não foram encontrados

Após busca em Receita Federal, Portal do Simples, Banco Central, IBGE/Sidra e páginas setoriais, não foi localizada base pública que informe:

| Afirmação desejada | Resultado da pesquisa |
|---|---|
| Percentual de empresas do Simples que não segregam PIS/Cofins monofásicos | **Não encontrado.** |
| “Mais de 80% pagam em dobro” | **Não comprovado.** |
| “Mais de quatro milhões de empresas atingidas” | **Não comprovado.** |
| Valor médio pago a maior por empresa/segmento | **Não encontrado.** |
| Mix médio de produtos monofásicos de oficina, bar, drogaria, conveniência ou pet shop | **Não encontrado em fonte pública comparável.** |
| Consultoria tradicional custa R$ 5 mil–R$ 20 mil ou R$ 15 mil em média | **Não comprovado por levantamento representativo.** Há software concorrente anunciado por R$ 37/30 dias, o que contradiz usar R$ 15 mil como preço universal da alternativa. |
| Restituição ocorre em 15–60 dias úteis | **Não comprovado.** O serviço oficial informa duração “não estimada ainda”. |
| Valor total anual restituído especificamente por falta de segregação monofásica no Simples | **Não encontrado.** Os dados abertos gerais de PER/DCOMP não isolam adequadamente esse fluxo eletrônico e essa causa. |

Essas ausências devem ser ditas explicitamente aos jurados. A maneira correta de obter uma estatística própria seria um piloto com empresas reais, consentimento, critérios de elegibilidade publicados e amostra descrita — algo que não deve ser inventado durante o hackathon.

## 3. Fórmula econômica correta

Para empresa comercial enquadrada no Anexo I:

```text
alíquota efetiva = (RBT12 × alíquota nominal − parcela a deduzir) ÷ RBT12

percentual efetivo de PIS/Cofins =
  alíquota efetiva × participação de PIS/Cofins na faixa

principal pago a maior =
  receita de revenda monofásica não segregada × percentual efetivo de PIS/Cofins
```

Nas faixas 1 a 5 do Anexo I, a participação combinada é 12,74% de Cofins + 2,76% de PIS = **15,5% da alíquota efetiva do DAS**.

### Sensibilidade por R$ 100 mil de receita monofásica no mês

| RBT12 de referência | Alíquota efetiva do DAS | PIS/Cofins efetivos sobre a receita monofásica | Economia por R$ 100 mil/mês não segregados |
|---:|---:|---:|---:|
| R$ 180.000 | 4,0000% | 0,6200% | R$ 620,00 |
| R$ 600.000 | 7,1900% | 1,1145% | R$ 1.114,45 |
| R$ 1.800.000 | 9,4500% | 1,4648% | R$ 1.464,75 |
| R$ 3.600.000 | 11,8750% | 1,8406% | R$ 1.840,63 |

Isso mostra que, nos portes usados no estudo original, aplicar 3,65% diretamente sobre a receita monofásica superestima o principal em aproximadamente duas a seis vezes.

## 4. Recálculo dos exemplos do estudo original

As linhas abaixo **não são estatísticas setoriais**. Elas apenas mantêm o faturamento e o mix hipotéticos do documento original para mostrar o cálculo legal corrigido.

Premissas:

- comércio no Anexo I;
- faturamento mensal constante, portanto RBT12 = 12 × faturamento mensal;
- todo o mix indicado foi efetivamente revendido, era legalmente monofásico e deixou de ser segregado;
- 60 pagamentos mensais de mesmo valor;
- sem multas, honorários, compensações de ofício, meses não pagos, mudança de faixa ou mudança de mix;
- coluna com Selic é somente uma ilustração descrita na seção seguinte.

| Cenário hipotético | Faturamento/mês | Mix monofásico assumido | PIS/Cofins efetivos | Economia mensal futura | Principal em 60 meses | Ilustração com Selic* |
|---|---:|---:|---:|---:|---:|---:|
| Oficina pequena | R$ 50.000 | 70% | 1,1145% | **R$ 390,06** | **R$ 23.403,45** | **R$ 30.805,81** |
| Auto center médio | R$ 150.000 | 75% | 1,4648% | **R$ 1.647,84** | **R$ 98.870,63** | **R$ 130.142,74** |
| Bar/restaurante | R$ 80.000 | 45% | 1,2952% | **R$ 466,28** | **R$ 27.976,73** | **R$ 36.825,58** |
| Distribuidora/conveniência | R$ 200.000 | 85% | 1,6527% | **R$ 2.809,57** | **R$ 168.574,13** | **R$ 221.893,00** |
| Drogaria/perfumaria | R$ 120.000 | 60% | 1,4163% | **R$ 1.019,75** | **R$ 61.184,70** | **R$ 80.537,01** |
| Pet shop/clínica | R$ 60.000 | 40% | 1,1741% | **R$ 281,79** | **R$ 16.907,40** | **R$ 22.255,10** |

\* Não é previsão de pagamento. É a aplicação de uma hipótese uniforme às taxas oficiais disponíveis.

### Comparação com os valores do documento original

| Cenário | Original: principal em 60 meses | Corrigido: principal em 60 meses | Diferença |
|---|---:|---:|---:|
| Oficina pequena | R$ 76.650,00 | R$ 23.403,45 | −69,5% |
| Auto center médio | R$ 246.375,00 | R$ 98.870,63 | −59,9% |
| Bar/restaurante | R$ 78.840,00 | R$ 27.976,73 | −64,5% |
| Distribuidora/conveniência | R$ 372.300,00 | R$ 168.574,13 | −54,7% |
| Drogaria/perfumaria | R$ 157.680,00 | R$ 61.184,70 | −61,2% |
| Pet shop/clínica | R$ 52.560,00 | R$ 16.907,40 | −67,8% |

## 5. Ilustração da Selic retroativa

A Receita informa que pagamentos indevidos são atualizados pela Selic desde o mês subsequente ao pagamento até o mês anterior à restituição, mais 1% no mês em que a restituição for efetuada. O sistema apresenta o valor original no pedido; a atualização ocorre na efetivação do pagamento.

Para quantificar a ordem de grandeza sem fingir conhecer a data de pagamento:

- foram usadas as taxas mensais reais da série **BCB/SGS 4390** de agosto de 2021 a julho de 2026;
- supuseram-se 60 pagamentos iguais, um por mês, de agosto de 2021 a julho de 2026;
- supôs-se, apenas para cálculo, restituição em agosto de 2026, com 1% nesse mês;
- para cada pagamento, somaram-se as taxas a partir do mês seguinte, conforme o método descrito pela Receita;
- o pagamento mais antigo teria acréscimo ilustrativo de 59,05% e o mais recente de 1%;
- sobre os 60 pagamentos iguais, o multiplicador médio resultou em **1,316293**, ou acréscimo de **31,63%** sobre o principal agregado.

O valor real muda com datas, valores de cada mês, deferimento e data efetiva de pagamento. Portanto, não deve aparecer no produto como “crédito garantido”.

## 6. Qual economia retroativa podemos afirmar

Não existe um valor universal. O que pode ser afirmado com rigor é:

```text
economia retroativa comprovável =
  soma, mês a mês, de:
  receita monofásica efetivamente vendida e não segregada
  × parcela efetiva de PIS/Cofins do DAS daquele período
  limitada aos pagamentos ainda dentro do prazo
  + atualização aplicada pela Receita quando houver pagamento
```

Nos seis cenários hipotéticos do estudo, o principal recalculado varia de **R$ 16,9 mil a R$ 168,6 mil** e a ilustração com Selic varia de **R$ 22,3 mil a R$ 221,9 mil**. Esses valores só são alcançados se todas as premissas forem verdadeiras e comprovadas.

Não é metodologicamente válido multiplicar esses valores pelos 6,14 milhões de optantes classificados no Receita Sintonia. Faltam taxas observadas de elegibilidade, erro, mix, faturamento, sobrevivência por cinco anos e deferimento.

## 7. Como produzir dados reais próprios após o hackathon

Um piloto publicável deveria registrar, por empresa e sem dados identificáveis:

- CNAE e faixa de RBT12;
- número de meses/documentos analisados;
- receita total e receita monofásica confirmada;
- valor originalmente declarado no PGDAS e valor retificado;
- principal potencial, valor pedido, valor deferido e prazo real;
- quantidade de itens confirmados, rejeitados e enviados à revisão humana;
- motivo de cada falso positivo;
- seleção da amostra e taxa de abandono.

Até existir esse piloto, use no pitch a expressão **“simulação legal reproduzível”**, nunca “média de mercado” ou “caso real”.

## Fontes consultadas

- [Receita Sintonia — classificação trimestral de junho de 2026](https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2026/julho/receita-federal-divulga-nova-classificacao-trimestral-do-programa-receita-sintonia)
- [Estatísticas do Simples Nacional por CNAE, UF e município](https://www8.receita.fazenda.gov.br/simplesnacional/aplicacoes/atbhe/estatisticassinac.app/default.aspx)
- [Portal Nacional da NF-e — estatísticas de documentos e emissores](https://www.nfe.fazenda.gov.br/Portal/listaConteudo.aspx?AspxAutoDetectCookieSupport=1&tipoConteudo=%2FNJarYc9nus%3D)
- [IBGE — Cadastro Central de Empresas 2023](https://www.ibge.gov.br/estatisticas/economicas/industria/9016-estatisticas-do-cadastro-central-de-empresas.html?edicao=45103)
- [Receita Federal — dados setoriais das pessoas jurídicas 2023](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/estudos/pessoas-juridicas-por-setor/estudos-setoriais-das-pessoas-juridicas/dados-setoriais-2023/)
- [Lei Complementar nº 123/2006 e Anexo I — Planalto](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm)
- [Manual do PGDAS-D — fórmula e partilha do Anexo I](https://www8.receita.fazenda.gov.br/simplesnacional/arquivos/manual/manual_pgdas-d_2018_v4.pdf)
- [Código Tributário Nacional, arts. 165 e 168 — Planalto](https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm)
- [Serviço oficial de restituição do Simples/MEI — duração não estimada](https://www.gov.br/pt-br/servicos/obter-restituicao-de-tributos-do-simples-nacional-e-mei)
- [Receita Federal — atualização das restituições pela Selic](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/restituicao-ressarcimento-reembolso-e-compensacao/restituicao/atualizacao-das-restituicoes-compensacoes)
- [Receita Federal — método de soma mensal da Selic](https://www.gov.br/receitafederal./pt-br/assuntos/orientacao-tributaria/pagamentos-e-parcelamentos/pagamento-em-atraso/como-calcular-juros-de-mora-acrescimos-legais)
- [Banco Central — série SGS 4390, Selic acumulada no mês](https://dadosabertos.bcb.gov.br/dataset/4390-taxa-de-juros---selic-acumulada-no-mes)
- [API oficial BCB/SGS 4390 — período usado na simulação](https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial=01/07/2021&dataFinal=31/07/2026)
- [Receita Federal — dados abertos de restituição e ressarcimento](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos/restituicao-e-ressarcimento)
- [Auditor Simples — preço público e limites do plano](https://app.auditorsimples.com.br/conheca-nossos-planos)
