# Pitch Audita — roteiro de 3 minutos

## Antes de entrar

- execute `./run.sh` e deixe `http://localhost:8000` aberto;
- confirme o selo **Motor local ativo** — a demo não depende da internet;
- use zoom de 100% e feche painéis do navegador;
- deixe `sample_invoices/lote_oficina_mecanica_5_notas.zip` à mão como plano B;
- não configure chave OpenAI durante o pitch, a menos que o jurado pergunte.

## 0:00–0:30 — a dor real

**Fala**

> “Uma pequena oficina sabe vender peças, mas não deveria precisar interpretar NCM, exceção legal, CST e PGDAS-D para pagar o imposto certo. Quando a receita monofásica de PIS/Cofins não é segregada, pode haver pagamento indevido ou a maior. Hoje, encontrar isso exige cruzar documentos e regras espalhadas — e um XML de compra ou NCM isolado não prova nada.”

**Tela**

Mostre o título, os três princípios — processamento local, regra antes da IA, fontes por achado — e o formulário de premissas.

## 0:30–1:10 — a demonstração

**Fala**

> “Vou executar um cenário didático com cinco notas sintéticas de venda de uma oficina. O RBT12 é R$ 1,8 milhão e informamos que a receita ainda não foi segregada. O motor calcula a alíquota efetiva do Simples — não usa 3,65% fixos.”

Pressione **Demo 3 min — Oficina**.

> “Em segundos, o Audita encontra R$ 1.840,00 de potencial estimado. Repare nos termos: potencial, simulação sintética e validação. Não prometemos crédito nem Pix. Mostramos a fórmula: 9,45% de DAS efetivo vezes a fração de 15,5% de PIS/Cofins, aplicada à receita confirmada.”

## 1:10–1:55 — o diferencial

**Fala**

> “O número é a parte fácil. O diferencial é a trilha de evidências. Cada item traz NCM, CFOP, CST de PIS e Cofins, CSOSN separado como ICMS, regra, fonte, vigência e pendências. O motor trabalha com três estados: confirmado, revisar e não enquadrado. NCM amplo, exceção Ex, descrição e produto usado não viram um simples ‘sim ou não’.”

**Tela**

- aponte o donut por segmento;
- alterne **Resumo**, **Base legal** e **Plano de ação**;
- busque `4011` e mostre a fonte do pneu;
- diga que Chart.js tem fallback e que o motor funciona offline.

**Fala de inovação**

> “Concorrentes costumam parar numa lista de NCM ou numa consultoria de recuperação. O Audita vira uma camada de compliance explicável: regra versionada, evidência por item, contexto do PGDAS-D, IA impedida de alterar números e revisão humana explícita. É um caminho para o contador decidir, não uma promessa para o empresário clicar.”

## 1:55–2:30 — Copilot e artefatos

Abra **Copilot Fiscal** e clique **Pastilhas de freio**.

> “Mesmo sem chave ou rede, o Copilot responde com fontes e limites. Com OpenAI, usamos `gpt-4o-mini` na Responses API só para explicar; classificação e cálculo continuam determinísticos.”

Feche o drawer e pressione **Baixar Excel**.

> “A planilha tem resumo executivo, itens auditados e memória PGDAS-D com fórmulas. O PDF é uma memória e checklist com espaço para validação do contador — deliberadamente não é petição ou parecer.”

## 2:30–3:00 — impacto e fechamento

**Fala**

> “Nosso MVP transforma horas de triagem em uma análise de segundos, preservando a parte que não pode ser automatizada: a decisão profissional. Começamos por autopeças, bebidas e farmácia/perfumaria, com regras por vigência. O próximo passo é importar o extrato do PGDAS-D, ampliar as tabelas oficiais do SPED e preparar a transição de PIS/Cofins para CBS a partir de 2027.”

> “Audita: o pequeno negócio enxerga o possível problema; o contador recebe a evidência para decidir.”

## Perguntas prováveis dos jurados

### “Esse dinheiro é garantido?”

Não. É uma estimativa de possível pagamento indevido ou a maior. Depende de classificação, documentos, declaração original, prazo e análise da Receita. O produto insiste nessa distinção em tela e nos relatórios.

### “Por que a IA é necessária?”

Ela reduz a barreira de compreensão e transforma evidências em próximos passos. Não decide a regra nem o valor. Sem chave ou rede, o fallback local preserva a jornada completa.

### “O que há de inovador se já existem recuperadoras?”

O diferencial demonstrável é o grafo de evidências por item, o catálogo temporal com incerteza explícita, a conciliação com o PGDAS-D, o limite estrutural da IA e a geração local de artefatos auditáveis. A plataforma também funciona como prevenção recorrente, não apenas recuperação histórica.

### “Essas notas são reais?”

Não. São fixtures sintéticas, com CNPJs fictícios e marcação `SEM VALOR FISCAL`, calibradas para permitir uma demo reproduzível sem expor dados pessoais.

### “Qual é a base legal?”

LC 123/2006, art. 18, § 4º-A, I; leis setoriais 10.147/2000, 10.485/2002 e 13.097/2015; CTN, arts. 165 e 168; Resolução CGSN 140/2018; IN RFB 2.055/2021; e tabelas 4.3.10/4.3.11 da EFD-Contribuições.

## Frases proibidas no pitch

- “crédito garantido”;
- “dinheiro imediato” ou “Pix da Receita”;
- “sem risco”;
- “notas reais”;
- “todos os NCMs estão cobertos”;
- “a IA confirmou seu direito”.
