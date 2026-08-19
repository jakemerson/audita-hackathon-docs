# AuditaPix & NotaCerta — concorrentes e avaliação de inovação

**Pesquisa atualizada em:** 19 de agosto de 2026  
**Método:** comparação baseada nas funcionalidades declaradas nos sites dos próprios fornecedores. As alegações comerciais não foram auditadas independentemente.

## Veredito

Na forma atual, a ideia **não é suficientemente original para se apoiar apenas em “upload de XML + identificação de monofásicos + cálculo + relatório”**. Há várias soluções brasileiras que já anunciam esse fluxo, algumas incluindo extrato do PGDAS, recuperação ponta a ponta, segregação mensal e preparação para a reforma tributária.

Isso não impede uma boa nota de inovação: o critério do hackathon também aceita melhora significativa. Mas a demo precisa evidenciar uma contribuição técnica distinta e verificável. “Usar IA”, “gerar PDF”, “receber via Pix”, “processar em cinco segundos” e apresentar um dashboard não bastam como diferenciação.

## 1. Concorrentes diretos

| Concorrente | Sobreposição comprovada com a ideia | Público/posicionamento | Preço público encontrado | Observação para o pitch |
|---|---|---|---:|---|
| [Auditor Simples](https://auditorsimples.com.br/) | Upload de XMLs e extratos PGDAS; identifica PIS/Cofins monofásicos e ICMS-ST; calcula valores e gera relatórios para declaração/retificação | Contadores e profissionais de recuperação | [R$ 37 por 30 dias](https://app.auditorsimples.com.br/conheca-nossos-planos), até 10 empresas, com teste grátis limitado | É o concorrente mais próximo e torna indefensável a afirmação de que toda alternativa custa R$ 5 mil–R$ 20 mil. |
| [Recupera Simples / AItax](https://recuperasimples.com.br/) | Calculadora monofásica, segregação mensal, classificação por código de barras/descrição/NCM e recuperação de PIS/Cofins | Contadores e advogados | Não encontrado no site consultado | A matriz funcional coincide quase integralmente com o núcleo atual. |
| [Sittax Recupera](https://sittax.com.br/) | Diagnóstico automático e recuperação de ICMS/PIS/Cofins “ponta a ponta”; segregação e apuração do Simples; simulação da reforma | Escritórios contábeis | Não encontrado no site consultado | Já conecta recuperação de legado e reforma, diferenciação que o AuditaPix ainda precisa incorporar. |
| [e-Auditoria / e-Recuperador](https://www.e-auditoria.com.br/ofertas/lm-recuperacao-de-creditos-tributarios/) | Analisa XML, EFD e PGDAS; recuperação de PIS/Cofins no Simples; cálculo e relatórios; segregação de receitas | Contadores e consultorias | Não encontrado no site consultado | Concorrente estabelecido, com escopo documental e tributário mais amplo. |
| [Contta e-Simples](https://www.contta.com.br/produtos/simples) | Lê XML, classifica item, aplica anexo/sublimite/Fator R, segrega ST e monofásico e entrega DAS para conferência | Escritórios contábeis | Não confirmado na página consultada | Vai além da recuperação e cobre a apuração mensal; também oferece módulo de reforma tributária. |
| [Jettax](https://www.jettax.com.br/) | Captura, audita e apura documentos; aplica ST e monofásicos automaticamente; cobertura de NFS-e em mais de 2.200 municípios, segundo a empresa | Escritórios contábeis | Não encontrado no site consultado | Diferencial operacional forte: captura sem depender do envio manual do cliente. |
| [REVEX](https://revexia.com.br/) | Análise de XML com IA, recuperação de PIS/Cofins monofásicos, compliance, estimativas setoriais, trilha verificável por hash e referência à CBS/IBS | Empresas e consultores | Planos exibidos pelo fornecedor, mas preço comparável não foi validado na consulta | Já usa “IA + trilha de auditoria + reforma” como narrativa; o AuditaPix precisa ser mais específico. |

## 2. Concorrentes adjacentes

| Concorrente | Adjacência relevante | Por que importa |
|---|---|---|
| [Taxcel Studio/TaxSheets](https://www.taxcel.com.br/taxcelstudio) | Importa XML/SPED, constrói fluxos de revisão de PIS/Cofins de cinco anos e exporta obrigações; possui conteúdo/ferramentas de IBS/CBS | Compete na camada de transformação, conciliação e revisão fiscal para usuários profissionais. |
| [Wefix SPED](https://wefix.com.br/) | Simulação da reforma com XML/SPED/Simples e apoio a obrigações/retificações | Mostra que “transição para IBS/CBS” isoladamente também não é inédita. |
| [e-Simples Auditor](https://www.esimplesauditoria.com/) | Auditoria eletrônica e módulos por quantidade de CNPJ | Reforça que o mercado B2B para escritórios já é povoado e costuma vender por carteira de clientes. |

## 3. Comparação por funcionalidade

| Funcionalidade da proposta atual | Já encontrada no mercado? | Exemplos |
|---|---|---|
| Upload/processamento de XML em lote | **Sim** | Auditor Simples, e-Auditoria, Contta, Taxcel |
| Classificação por NCM/CST | **Sim** | Recupera Simples, Auditor Simples, Contta |
| Detecção de PIS/Cofins monofásicos | **Sim** | Praticamente todos os concorrentes diretos |
| Leitura/comparação de PGDAS | **Sim** | Auditor Simples, e-Auditoria, Contta |
| Cálculo retroativo de cinco anos | **Sim** | Recupera Simples, e-Auditoria, Taxcel, REVEX |
| Relatórios/planilhas para recuperação | **Sim** | Auditor Simples, e-Auditoria, Sittax |
| Segregação mensal preventiva | **Sim** | Recupera Simples, Sittax, Contta |
| IA explicativa | **Sim, ao menos como alegação comercial** | REVEX e outros fornecedores que se apresentam como “inteligentes” |
| Reforma IBS/CBS | **Sim** | Sittax, Contta, Wefix, Taxcel |
| Recebimento via Pix | Não é recurso do concorrente nem do produto | É uma opção do sistema oficial da Receita; não é diferencial proprietário. |
| Petição PDF | Não foi confirmada como recurso comum | Diferencial fraco: o pedido ordinário do DAS é eletrônico e uma petição automática aumenta risco profissional. |

## 4. Onde há espaço real de inovação

O espaço mais promissor não é “mais um recuperador”. É um **agente de evidência fiscal local-first, explicável e versionado**, voltado ao pequeno empresário e ao contador que o valida.

### Proposta diferenciada recomendada

**“AuditaPix Legado 2027 — do documento ao crédito auditável, com transição para CBS/IBS.”**

1. **Reconstrução do fato econômico, não só classificação de NCM**  
   Importar saídas NF-e/NFC-e, PGDAS original, RBT12 e DAS; provar a diferença entre declarado e correto mês a mês. Notas de entrada entram apenas como evidência auxiliar.

2. **Grafo de regras versionado por data**  
   Cada item mostra lei, artigo, NCM/TIPI/“Ex”, período de vigência, exceções e versão da regra. Isso é mais defensável do que uma lista estática de NCM.

3. **IA limitada à ambiguidade e explicação**  
   O modelo interpreta descrição e levanta hipótese; o motor determinístico calcula. Itens ambíguos entram em fila de revisão, com confiança e motivo. O jurado consegue inspecionar o raciocínio.

4. **Humano no circuito com responsabilidade clara**  
   Contador aprova a memória de retificação; advogado revisa eventual manifestação jurídica. O software registra quem aprovou e não transmite sozinho.

5. **Privacidade como arquitetura demonstrável**  
   Processamento local, campos minimizados antes da chamada ao modelo, exclusão automática e relatório de quais dados saíram do dispositivo. Isso é valioso para XML fiscal e fácil de demonstrar tecnicamente.

6. **Ponte 2026 → 2027**  
   Além do legado de PIS/Cofins, traduz o mesmo catálogo para cClassTrib/CST de IBS/CBS, aponta campos faltantes e compara Simples “por dentro” com opção regular, sem prometer decisão definitiva.

7. **Projeto aberto e reproduzível**  
   Regras, fixtures sintéticas, testes por artigo/período e cálculo são públicos. Um “teste de regressão legal” mostra que alteração de regra não muda períodos pretéritos.

## 5. Demo de três minutos recomendada

### 0:00–0:30 — problema comprovável

Carregar um conjunto **sintético e identificado como sintético** com vendas, PGDAS original e DAS. Mostrar que o sistema não presume crédito a partir de compras.

### 0:30–1:20 — profundidade técnica

Reconstruir as vendas monofásicas, calcular o RBT12/faixa de cada mês e comparar com o PGDAS. Abrir um item e exibir lei, vigência, regra determinística e eventual hipótese da IA.

### 1:20–2:00 — controle de risco

Mostrar dois itens: um confirmado automaticamente e outro com NCM/descrição ambígua bloqueado para revisão do contador. Isso demonstra confiabilidade, não fragilidade.

### 2:00–2:35 — resultado acionável

Gerar memória de retificação por DAS, trilha de evidências e checklist do Pedido Eletrônico de Restituição. Exibir principal e Selic como campos separados; rotular tudo como estimativa até o deferimento.

### 2:35–3:00 — inovação e futuro

Alternar para a visão 2027 e mostrar como os mesmos produtos/documentos serão validados para CBS/IBS. Encerrar com o ganho: recuperar o legado sem criar um novo passivo e preparar a pequena empresa para a reforma.

## 6. O que retirar ou reformular no pitch

- Retirar “80% das empresas”, “quatro milhões atingidas” e “3%–4,5% a mais” sem dados.
- Retirar “R$ 1.840 garantidos via Pix” e usar “R$ X de principal potencial, sujeito a revisão e deferimento”.
- Retirar “notas fiscais reais” do repositório/demo; usar fixtures sintéticas realistas.
- Trocar “parecer pericial” por “relatório explicável para validação profissional”.
- Trocar “petição oficial” por “memória de cálculo e checklist de retificação/pedido”.
- Não afirmar que CST errado do fornecedor é a causa necessária do pagamento a maior.
- Não marcar CST 01/02 do fabricante como erro automático nem comparar CSOSN de ICMS com CST 04 de PIS/Cofins.
- Preferir “pagamento indevido/a maior por falta de segregação” a “bitributação”, tecnicamente impreciso.
- Não destacar o dashboard como produto; destacar reconciliação, motor de regras, controle de versões, revisão humana e trilha de evidência.
- Atualizar “GPT-4o-mini” para o modelo efetivamente disponibilizado/permitido no evento e demonstrar qual etapa precisa de IA.

## Fontes consultadas

### Concorrentes diretos

- [Auditor Simples — produto](https://auditorsimples.com.br/)
- [Auditor Simples — planos e preço público](https://app.auditorsimples.com.br/conheca-nossos-planos)
- [Recupera Simples / AItax](https://recuperasimples.com.br/)
- [Sittax](https://sittax.com.br/)
- [e-Auditoria — recuperação de créditos](https://www.e-auditoria.com.br/ofertas/lm-recuperacao-de-creditos-tributarios/)
- [e-Auditoria — créditos e monofásicos no Simples](https://www.e-auditoria.com.br/blog/creditos-nao-aproveitados-de-fornecedores-do-simples-nacional/)
- [Contta e-Simples Nacional](https://www.contta.com.br/produtos/simples)
- [Jettax](https://www.jettax.com.br/)
- [REVEX](https://revexia.com.br/)
- [e-Simples Auditor — preços sob consulta](https://www.esimplesauditoria.com/precos)

### Concorrentes adjacentes e reforma

- [Taxcel Studio](https://www.taxcel.com.br/taxcelstudio)
- [Taxcel — tabela cClassTrib/CST IBS/CBS](https://taxcel.com.br/cclass-cst-ibs-cbs)
- [Wefix SPED](https://wefix.com.br/)
- [Receita Federal — Reforma Tributária do Consumo](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/entenda)
