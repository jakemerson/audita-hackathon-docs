# NCMs e regras de enquadramento no regime monofásico de PIS/Cofins

**Pesquisa atualizada em:** 19 de agosto de 2026  
**Escopo:** produtos sujeitos à tributação concentrada/monofásica de PIS e Cofins relevantes para a segregação de receitas no Simples Nacional.

## Resposta curta

Não existe uma única lista legal, plana e eterna de NCMs monofásicos. O conjunto está distribuído entre várias leis e é representado operacionalmente nas **Tabelas 4.3.10 e 4.3.11 da EFD-Contribuições**, publicadas pelo SPED/Receita Federal.

A lista oficial usa quatro tipos de regra:

1. código NCM exato;
2. posição ou subposição NCM, abrangendo seus desdobramentos;
3. código acompanhado de exceção `Ex`, abrangendo somente a descrição daquele `Ex`;
4. descrição ou destinação legal adicional, que impede decidir apenas pelo número do NCM.

Portanto, o motor do produto deve implementar **regras**, não apenas um conjunto de strings de oito dígitos.

## Fontes oficiais para download e consulta

- [Tabela 4.3.10 do SPED — incidência monofásica com alíquotas percentuais, versão 1.25](https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/efd-contribuicoes/tabelas-de-codigos/tabelas-utilizadas-na-apuracao-das-contribuicoes-para-o-pis-pasep-e-da-cofins/tabela-4-3-10)
- [Download direto da Tabela 4.3.10](https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/efd-contribuicoes/tabelas-de-codigos/tabelas-utilizadas-na-apuracao-das-contribuicoes-para-o-pis-pasep-e-da-cofins/tabela-4-3-10/@@download/file)
- [Tabela 4.3.11 do SPED — incidência monofásica por unidade de medida, versão 1.33](https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/efd-contribuicoes/tabelas-de-codigos/tabelas-utilizadas-na-apuracao-das-contribuicoes-para-o-pis-pasep-e-da-cofins/tabela-4-3-11)
- [Download direto da Tabela 4.3.11](https://www.gov.br/sped/pt-br/assuntos/escrituracoes-digitais/efd-contribuicoes/tabelas-de-codigos/tabelas-utilizadas-na-apuracao-das-contribuicoes-para-o-pis-pasep-e-da-cofins/tabela-4-3-11/@@download/file)
- [Sistema Classif — consulta oficial da NCM vigente e do histórico](https://www.gov.br/receitafederal/pt-br/assuntos/aduana-e-comercio-exterior/classificacao-fiscal-de-mercadorias/classif)
- [Download oficial da NCM vigente em JSON/XLSX](https://www.gov.br/receitafederal/pt-br/assuntos/aduana-e-comercio-exterior/classificacao-fiscal-de-mercadorias/download-ncm-nomenclatura-comum-do-mercosul)
- [Histórico oficial da NCM desde 1996](https://www.gov.br/receitafederal/pt-br/assuntos/aduana-e-comercio-exterior/classificacao-fiscal-de-mercadorias/historico-ncm-nomenclatura-comum-do-mercosul)

As tabelas SPED são a melhor fonte operacional. A fonte jurídica primária continua sendo a lei indicada em cada grupo.

## Como interpretar os níveis da NCM

| Forma encontrada na lei | Como testar | Os desdobramentos entram? |
|---|---|---|
| `4011.10.00` | igualdade com os 8 dígitos | somente esse subitem |
| `8409.91` | prefixo de 6 dígitos | sim, todos os itens/subitens abaixo, salvo exceção |
| `40.11` | prefixo de 4 dígitos | sim, todos os códigos classificados na posição, salvo restrição textual |
| `87.01 a 87.06` | faixa de posições | sim, todos os desdobramentos das posições da faixa |
| `4016.99.90 Ex 03 e 05` | código + descrição do `Ex` | não; apenas os produtos descritos nos Ex 03 e 05 |
| `8412.21.10, próprios para...` | código + uso/destinação | não basta o NCM; a destinação também deve ser comprovada |

Hierarquia simplificada: capítulo (2 dígitos) → posição (4) → subposição (6) → item (7) → subitem (8).

## Regra completa por setor

### 1. Combustíveis e álcool

Principais códigos ou prefixos encontrados nas Tabelas 4.3.10/4.3.11:

- `2710.12.59` — gasolina, exceto gasolina de aviação;
- `2710.19.21` — óleo diesel;
- `2711.19.10` — GLP, observadas as condições de destinação/embalagem vigentes;
- `2710.19.11` — querosene de aviação;
- `3826.00.00` e `3826.00.00 Ex 01` — biodiesel na nomenclatura atual da tabela;
- `2207.10`, `2207.20.1` e `2208.90.00 Ex 01` — álcool/etanol, conforme a operação e o período.

Há também correntes destinadas à formulação de gasolina ou diesel e produtos petroquímicos descritos sem NCM específico. Logo, **NCM vazio não significa regra inexistente**.

Fontes legais indicadas pela própria Tabela 4.3.10:

- Lei nº 9.718/1998, arts. 4º e 5º;
- Lei nº 10.560/2002, art. 2º;
- Lei nº 10.336/2001, art. 14;
- Lei nº 11.116/2005, art. 3º;
- Lei nº 11.196/2005, art. 56.

Esse grupo exige forte versionamento por data: as tabelas registram várias mudanças de código, alíquota, coeficiente e período.

### 2. Produtos farmacêuticos

Regra do art. 1º, I, `a`, da Lei nº 10.147/2000:

- posição `30.01`;
- posição `30.03`, **exceto** `3003.90.56`;
- posição `30.04`, **exceto** `3004.90.46`;
- itens `3002.10.1`, `3002.10.2`, `3002.10.3`;
- itens `3002.20.1`, `3002.20.2`;
- itens `3006.30.1`, `3006.30.2`;
- códigos `3002.90.20`, `3002.90.92`, `3002.90.99`;
- código `3005.10.10`;
- código `3006.60.00`.

Quando a lei cita `30.01`, todos os códigos subordinados à posição entram. Quando cita `3002.10.1`, entram os subitens de oito dígitos que começam com esses sete dígitos. As exceções `3003.90.56` e `3004.90.46` ficam fora mesmo pertencendo às posições mais amplas.

Fonte: [Lei nº 10.147/2000, arts. 1º e 2º](https://www.planalto.gov.br/ccivil_03/leis/l10147.htm).

### 3. Perfumaria, toucador e higiene pessoal

Regra atual do art. 1º, I, `b`, da Lei nº 10.147/2000:

- posições `33.03`, `33.04`, `33.05` e `33.07`;
- a posição `33.06` está expressamente **excluída**;
- `3401.11.90`, **exceto** `3401.11.90 Ex 01`;
- `3401.20.10`;
- `9603.21.00`.

Todos os desdobramentos das posições 33.03, 33.04, 33.05 e 33.07 entram, desde que a mercadoria esteja corretamente classificada nelas. A posição 33.06 e o Ex 01 de 3401.11.90 não entram nessa regra monofásica.

Fonte: [Lei nº 10.147/2000, arts. 1º e 2º](https://www.planalto.gov.br/ccivil_03/leis/l10147.htm).

### 4. Veículos e máquinas

Regra vigente indicada no código 301 da Tabela 4.3.10:

- `73.09`;
- `7310.29`;
- `7612.90.12`;
- `8424.81`;
- `84.29`;
- `8430.69.90`;
- `84.32`;
- `84.33`;
- `84.34`;
- `84.35`;
- `84.36`;
- `84.37`;
- `87.01`, `87.02`, `87.03`, `87.04`, `87.05`, `87.06`;
- `8716.20.00`.

Se a lei usa uma posição de quatro dígitos, seus desdobramentos são alcançados. Para o Capítulo 84, a redação vigente abrange produtos autopropulsados ou não.

Fonte: [Lei nº 10.485/2002, art. 1º](https://www.planalto.gov.br/ccivil_03/leis/2002/l10485compilado.htm).

### 5. Autopeças — Anexo I da Lei nº 10.485/2002

Lista completa do Anexo I:

```text
4016.10.10
4016.99.90 Ex 03 e 05
68.13
7007.11.00
7007.21.00
7009.10.00
7320.10.00 Ex 01
8301.20.00
8302.30.00
8407.33.90
8407.34.90
8408.20
8409.91
8409.99
8413.30
8413.91.00 Ex 01
8414.80.21
8414.80.22
8415.20
8421.23.00
8421.31.00
8431.41.00
8431.42.00
8433.90.90
8481.80.99 Ex 01 e 02
8483.10
8483.20.00
8483.30
8483.40
8483.50
8505.20
8507.10.00
85.11
8512.20
8512.30.00
8512.40
8512.90.00
8527.2
8536.50.90 Ex 01
8539.10
8544.30.00
8706.00
87.07
87.08
9029.20.10
9029.90.10
9030.39.21
9031.80.40
9032.89.2
9104.00.00
9401.20.00
```

Os códigos de 4 ou 6 dígitos abrangem seus desdobramentos. As linhas com `Ex` abrangem somente as descrições específicas dos Ex indicados.

### 6. Autopeças — Anexo II da Lei nº 10.485/2002

O Anexo II comprova por que NCM sozinho não basta. A lista completa contém:

1. tubos da posição `40.09`, com acessórios, próprios para máquinas e veículos das posições/códigos `84.29`, `8433.20`, `8433.30.00`, `8433.40.00`, `8433.5`, `87.01`, `87.02`, `87.03`, `87.04`, `87.05` e `87.06`;
2. partes da posição `84.31`, reconhecíveis como exclusiva ou principalmente destinadas às máquinas da posição `84.29`;
3. motores `8408.90.90`, próprios para máquinas `84.29`, `8433.20`, `8433.30.00`, `8433.40.00` e `8433.5`;
4. cilindros hidráulicos `8412.21.10`, próprios para máquinas `84.29`, `8433.20`, `8433.30.00`, `8433.40.00` e `8433.5`;
5. outros cilindros hidráulicos de movimento retilíneo `8412.21.90`, próprios para máquinas `84.29`, `8433.20`, `8433.30.00`, `8433.40.00` e `8433.5`;
6. cilindros pneumáticos `8412.31.10`, próprios para produtos `8701.20.00`, `87.02` e `87.04`;
7. bombas volumétricas rotativas `8413.60.19`, próprias para produtos `84.29`, `8433.20`, `8433.30.00`, `8433.40.00`, `8433.5`, `8701.20.00`, `87.02` e `87.04`;
8. compressores de ar `8414.80.19`, próprios para produtos `8701.20.00`, `87.02` e `87.04`;
9. caixas de ventilação para veículos autopropulsados `8414.90.39`;
10. partes `8432.90.00` de máquinas `8432.40.00` e `8432.80.00`;
11. válvulas redutoras de pressão `8481.10.00`, próprias para máquinas e veículos `84.29`, `8433.20`, `8433.30.00`, `8433.40.00`, `8433.5`, `87.01`, `87.02`, `87.03`, `87.04`, `87.05` e `87.06`;
12. válvulas para transmissões óleo-hidráulicas ou pneumáticas `8481.20.90`, próprias para máquinas `84.29`, `8433.20`, `8433.30.00`, `8433.40.00` e `8433.5`;
13. válvulas solenoides `8481.80.92`, próprias para máquinas e veículos `84.29`, `8433.20`, `8433.30.00`, `8433.40.00`, `8433.5`, `87.01`, `87.02`, `87.03`, `87.04`, `87.05` e `87.06`;
14. embreagens de fricção `8483.60.1`, próprias para máquinas `84.29`, `8433.20`, `8433.30.00`, `8433.40.00` e `8433.5`;
15. motores de corrente contínua `8501.10.19`, próprios para acionamento elétrico de vidros de veículos autopropulsados.

O resultado deve ser `REVISAR` quando o XML não trouxer evidência da destinação exigida. Confira sempre a redação no [Anexo II oficial da Lei nº 10.485/2002](https://www.planalto.gov.br/ccivil_03/leis/2002/l10485compilado.htm).

### 7. Pneus e câmaras de ar

- posição `40.11` — pneus novos de borracha;
- posição `40.13` — câmaras de ar de borracha.

Todos os desdobramentos dessas posições entram, mas a Lei nº 10.485/2002 determina expressamente que seu regime **não se aplica a produtos usados**. A exclusão do art. 6º vale para todos os produtos regulados pela lei — veículos, máquinas, autopeças, pneus e câmaras — e não apenas para este grupo. Assim, NCM compatível + descrição indicando produto usado deve ser rejeitado ou enviado para revisão.

Fonte: [Lei nº 10.485/2002, arts. 5º e 6º](https://www.planalto.gov.br/ccivil_03/leis/2002/l10485compilado.htm).

### 8. Bebidas frias

Regra dos arts. 14 e 28 da Lei nº 13.097/2015:

- `2106.90.10 Ex 02`;
- posição `22.01`, exceto os Ex 01 e 02 do código `2201.10.00`;
- posição `22.02`, com as exceções e reinclusões previstas no art. 14;
- `22.02.90.00 Ex 03` na nomenclatura indicada pela lei para determinadas cervejas/chopes especiais;
- posição `22.03` — cervejas de malte.

Para as posições 22.01 e 22.02, o parágrafo único do art. 14 limita a regra a:

- água;
- refrigerantes;
- chás;
- refrescos;
- cerveja sem álcool;
- repositores hidroeletrolíticos;
- bebidas energéticas;
- compostos líquidos prontos para consumo cujo ingrediente principal seja inositol, glucuronolactona, taurina ou cafeína.

Portanto, **nem todo produto classificado em 22.01/22.02 pode ser aceito apenas pelo prefixo**. É necessário validar também a descrição legal. A redução a zero prevista no art. 28 depende ainda de a receita ser auferida por varejista e de ele não ser industrial, importador ou equiparado nas hipóteses excluídas pela lei.

Fonte: [Lei nº 13.097/2015, arts. 14, 17 e 28](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13097.htm).

## Produtos filhos e subcategorias: regra objetiva

**Sim**, os códigos filhos se enquadram quando a lei cita uma posição/subposição mais ampla, desde que:

1. o código filho estivesse vigente na data da operação;
2. ele realmente pertença à árvore daquele prefixo no Sistema Classif;
3. não haja `exceto`, `Ex` restritivo ou descrição que o exclua;
4. sejam atendidas as condições de produto, uso, destinação e papel do vendedor;
5. a mercadoria não esteja fora do regime por outra disposição, como a exclusão de produtos usados na Lei nº 10.485/2002.

Exemplos:

- `4011.10.00` é filho de `40.11`: em princípio entra como pneu novo; usado não entra;
- `8708.29.99` é filho de `87.08`: entra no alcance do Anexo I, desde que a classificação esteja correta;
- qualquer filho de `33.06` fica fora da regra atual da Lei nº 10.147/2000;
- `3401.11.90 Ex 01` fica fora, apesar de compartilhar o código-base `3401.11.90`;
- uma válvula `8481.10.00` não entra automaticamente pelo Anexo II: precisa ser própria para as máquinas/veículos ali enumerados.

## Algoritmo recomendado

```text
normalizar NCM da mercadoria
        ↓
selecionar somente regras vigentes na data da venda
        ↓
testar código exato, prefixo ou faixa
        ↓
aplicar exclusões e descrições Ex
        ↓
validar descrição, uso/destinação e condição do vendedor
        ↓
CONFIRMADO | REVISAR | NÃO ENQUADRADO
```

Não use apenas `ncm.startsWith(prefixo)`. A estrutura mínima de cada regra deve conter:

```json
{
  "legal_basis": "Lei 10.485/2002, Anexo II, item 11",
  "ncm_pattern": "8481.10.00",
  "match_type": "exact_plus_condition",
  "required_use": "própria para as máquinas e veículos enumerados",
  "valid_from": "YYYY-MM-DD",
  "valid_until": null,
  "seller_roles_allowed": ["atacadista", "varejista"],
  "manual_review_if_missing_evidence": true
}
```

## Limite importante para recuperação de cinco anos

A NCM vigente hoje não pode ser aplicada retroativamente a todas as vendas. Para cada documento é necessário usar:

- o código e a descrição vigentes na data da operação;
- a versão histórica da regra monofásica;
- os `Ex` e condições vigentes naquele período;
- eventual tabela de correlação quando um código foi criado, extinto ou desdobrado.

O próprio download oficial da NCM alerta que seu arquivo contém apenas a tabela vigente; para operações antigas deve-se consultar o **Histórico NCM do Sistema Classif**. As Tabelas 4.3.10 e 4.3.11 também trazem início e término de escrituração para suas regras.

## Conclusão para o MVP

Para uma demo juridicamente defensável, não tente expandir todas as posições para milhares de códigos de oito dígitos. Implemente as regras hierárquicas acima e mostre três casos:

1. filho de uma posição ampla confirmado;
2. código com `Ex` excluído;
3. código compatível, mas sem prova de destinação, enviado para revisão.

Isso é mais correto e tecnicamente mais inovador do que apresentar uma lista estática de NCMs.
