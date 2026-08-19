/goal 
Você é um Engenheiro de Software Sênior e Especialista em IA e Direito Tributário Brasileiro. Sua missão é desenvolver DO ZERO e de forma 100% autônoma a plataforma completa:

================================================================================
🚀 PROJETO: AuditaPix & NotaCerta — Caçador Autônomo de Bitributação Fiscal
Trilha: Pequenos Negócios | OpenAI Hackathon 2026 | Fator WOW: 🔥🔥🔥🔥
================================================================================

A DOR REAL:
Pequenas empresas optantes pelo Simples Nacional no Brasil (oficinas mecânicas, autopeças, bares, restaurantes, farmácias e perfumarias) pagam PIS/COFINS em duplicidade todo mês. A indústria e importadores já recolhem o tributo de toda a cadeia na origem (Regime Monofásico). Quando o fornecedor emite a NF-e com CST tributável comum (01, 49, 99) ou o pequeno comerciante não segrega a receita no PGDAS-D, ele paga imposto duas vezes pelo mesmo produto!

A SOLUÇÃO:
Uma plataforma com IA (OpenAI GPT-4o-mini + Motor de Regras Tributárias Autônomo) que permite o upload em lote de arquivos XML de NF-e (ou arquivo .zip), cruza os NCMs/CFOPs/CSTs contra a legislação federal em menos de 5 segundos, apura o crédito a restituir, gera a Planilha Excel (.xlsx) de retificação do PGDAS-D, a Petição Administrativa Oficial em PDF para a Receita Federal e disponibiliza um Copilot Fiscal com IA para tirar dúvidas ao vivo.

A DEMO AO VIVO DE 3 MINUTOS (PITCH DO HACKATHON):
Um botão de 1-clique "Demo 3 Min (Oficina)" carrega 5 notas fiscais reais de autopeças (pastilhas de freio, amortecedores, filtros, velas e pneus). Em 2 segundos a ferramenta exibe um banner vibrante com chuva de confetti e contador animado: "Você tem R$ 1.840,00 de crédito imediato a receber via Pix da Receita Federal", com downloads instantâneos de Excel e PDF prontos!

--------------------------------------------------------------------------------
⚙️ REGRAS DE EXECUÇÃO OBRIGATÓRIAS (SIGA À RISCA):
--------------------------------------------------------------------------------
1. GSD OBRIGATÓRIO:
   - Leia a skill do GSD (`.agents/skills/gsd/SKILL.md`) e execute via agente executor (`.agents/skills/gsd/agents/executor/SKILL.md`).
   - Crie a pasta `.planning/` completa (`PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`) dividindo o projeto em fases estruturadas:
     * Fase 01: Setup do Ambiente (.venv Python 3.12), Motor Tributário e Parser XML NF-e v4.00.
     * Fase 02: Motor de Auditoria OpenAI, Copilot Fiscal, Gerador Excel (.xlsx) e Petição PDF.
     * Fase 03: API REST FastAPI (upload lote/zip, demo oficina, copilot, rotas de exportação).
     * Fase 04: Frontend SPA Premium com Dark Glassmorphism, Tailwind CDN, Chart.js, Confetti e Copilot Drawer.
     * Fase 05: Dataset de Teste com 5 XMLs físicos (R$ 1.840,00), scripts `run.sh` / `start.py`, README e Roteiro de Pitch.
     * Fase 06: Validação Visual no Navegador via Browser Subagent.
   - Cada fase/tarefa deve gerar commits atômicos no Git (`feat(...)`, `test(...)`, `docs(...)`).
   - Se encontrar qualquer erro ou bug, registre em `.planning/debug/` usando a skill de debug.

2. AMBIENTE PYTHON (.venv):
   - SEMPRE crie e utilize o ambiente virtual `.venv` usando Python 3.12 (`python3.12 -m venv .venv`).
   - Instale todas as dependências no `.venv`: `fastapi`, `uvicorn[standard]`, `pydantic`, `python-dotenv`, `openai`, `openpyxl`, `pandas`, `lxml`, `reportlab`, `jinja2`, `pytest`, `pytest-asyncio`, `httpx`, `python-multipart`.
   - Crie `.env` com o placeholder `OPENAI_API_KEY=sua_chave_openai_aqui` e `.env.example`.

3. NÃO ME PEÇA PERMISSÃO NEM FAÇA PERGUNTAS:
   - Execute tudo até o final de forma 100% autônoma. Só pare quando estiver tudo pronto, testado e validado visualmente.

--------------------------------------------------------------------------------
🏛️ ESPECIFICAÇÕES TÉCNICAS E MÓDULOS A DESENVOLVER:
--------------------------------------------------------------------------------

1. MOTOR TRIBUTÁRIO & NCMs MONOFÁSICOS (`app/core/tax_rules.py`):
   - Mapeamento completo dos NCMs monofásicos conforme as leis federais:
     * Autopeças (Lei 10.485/2002): Pastilhas/discos de freio (8708.30.90), amortecedores/suspensão (8708.80.00), filtros de óleo/ar (8421.23.00, 8421.31.00), velas de ignição (8511.10.00), pneus novos (4011.10.00, 4011.20.90), baterias (8507.10.10, 8507.10.90).
     * Bebidas Frias (Lei 13.097/2015): Cervejas (2203.00.00), refrigerantes/águas saborizadas (2202.10.00), águas minerais (2201.10.00), energéticos (2202.99.00).
     * Medicamentos e Cosméticos (Lei 10.147/2000): Shampoos (3305.10.00), perfumes (3303.00.10), maquiagens/cremes (3304.99.90), medicamentos (3004.90.99).
     * Simples Nacional: Art. 18, § 4º-A, inciso I da Lei Complementar nº 123/2006.
   - Detectar anomalias fiscais: Se o item é monofásico e o fornecedor emitiu com CST 01, 02, 49, 99 ou CSOSN 102/500/900 (ao invés do CST 04 Monofásico Alíquota Zero), calcular o valor pago a maior com base na alíquota efetiva do Simples Nacional (~3.65%).

2. PARSER DE XML NF-e RESILIENTE (`app/core/nfe_parser.py` e `app/models/nfe_models.py`):
   - Extrair dados do cabeçalho (`ide`: nNF, série, dhEmi), emitente (`emit`: CNPJ, xNome, CRT), destinatário (`dest`: CNPJ, xNome) e itens detalhados (`det`: cProd, xProd, NCM, CFOP, vProd, imposto/ICMS, imposto/PIS, imposto/COFINS).
   - Ignorar namespaces XML para suportar qualquer emissor estadual da SEFAZ (nfeProc ou NFe avulsa).
   - Função `audit_xml_batch` para consolidar métricas de faturamento, faturamento monofásico, itens bitributados e total a restituir.

3. IA OPENAI & MODO CONTINGÊNCIA AUTÔNOMO (`app/services/openai_auditor.py` e `app/services/copilot_service.py`):
   - Estrutura híbrida inteligente:
     * Com `OPENAI_API_KEY`: Chamada ao GPT-4o-mini para gerar Parecer Executivo, Fundamentação Jurídica e Plano de Ação estruturados em JSON, além do chat do Copilot.
     * Sem `OPENAI_API_KEY` (placeholder): Fallback instantâneo local com laudo pericial fundamentado nos artigos de lei e FAQ tributário inteligente. Zero quebra e velocidade máxima no pitch!

4. GERADORES DE RELATÓRIOS OFICIAIS:
   - Planilha Excel .XLSX (`app/services/excel_generator.py`): OpenPyXL com design C-Level, paleta Slate/Emerald, abas 'Resumo Executivo', 'Itens com Bitributação' e 'Memória PGDAS-D Retificador' com fórmulas automáticas de soma (`SUM`).
   - Petição PDF (`app/services/pdf_generator.py`): ReportLab gerando documento formal de Requerimento Administrativo perante a Receita Federal / Comitê Gestor do Simples Nacional com qualificação, quadro de créditos apurados, amparo legal e espaço para assinatura.

5. API REST FASTAPI (`app/api/audit_routes.py` e `app/main.py`):
   - `POST /api/audit/upload`: Upload em lote de múltiplos `.xml` ou arquivos compactados `.zip`.
   - `POST /api/audit/demo-oficina`: Retorno instantâneo do lote de 5 notas de oficina (R$ 1.840,00).
   - `POST /api/audit/copilot`: Chatbot com IA para tirar dúvidas tributárias.
   - `POST /api/export/excel` e `POST /api/export/pdf`: Streaming dos relatórios para download.
   - `GET /api/health` e `POST /api/config/set-key`: Healthcheck e configuração dinâmica da chave OpenAI na sessão.

6. FRONTEND SINGLE PAGE APPLICATION DE ALTO IMPACTO (`app/static/`):
   - Layout Dark Glassmorphism elegante (`#030712`, `#0f172a`, acentos `#10b981` e `#6366f1`).
   - Inclusão do Tailwind CSS Play CDN configurado + Google Fonts (`Outfit`, `Inter`, `JetBrains Mono`) + Ícones `Lucide`.
   - Dropzone interativo para arrastar e soltar XMLs/ZIPs com animação de progresso.
   - Botão de 1-Clique "Demo 3 Min (Oficina)".
   - Banner com Efeito WOW: Chuva de Confetti (`canvas-confetti`) e Contador Animado de Dinheiro (`countUp` até R$ 1.840,00).
   - 4 Cards de KPI: Total de Notas, Faturamento Auditado, Faturamento Monofásico e Taxa de Retorno.
   - Gráfico Donut com `Chart.js` mostrando a distribuição de créditos por segmento.
   - Card do Parecer da IA com alternância de abas: Resumo, Fundamentação Jurídica e Plano de Ação.
   - Tabela detalhada de itens com busca em tempo real por NCM/descrição e filtro de itens com glosa.
   - Gaveta lateral (Drawer) do AuditaPix Copilot com botões de perguntas rápidas ("Pastilhas de freio", "Prazo de restituição", "Como retificar PGDAS").
   - Modal para configurar dinamicamente a chave da OpenAI.

7. DATASET FÍSICO DE TESTE & PITCH:
   - Criar pasta `sample_invoices/` com 5 XMLs reais de oficina mecânica gerando exatamente **R$ 1.840,00** de restituição + arquivo `lote_oficina_mecanica_5_notas.zip` + XMLs extras de cervejaria e farmácia.
   - Criar `run.sh` (executável via `chmod +x run.sh`) e `start.py` para subir o servidor em 1 comando na porta 8000.
   - Criar `README.md` com diagrama de arquitetura em Mermaid e `PITCH_HACKATHON.md` com roteiro de fala minuto a minuto para os jurados.

8. TESTES AUTOMATIZADOS & VALIDAÇÃO NO BROWSER:
   - Criar e rodar suíte de testes com `pytest` (17+ testes unitários e de integração com 100% de aprovação).
   - OBRIGATÓRIO: Chamar o `browser_subagent` para abrir `http://localhost:8000`, testar o botão Demo de 3 Minutos, verificar a chuva de confetti, o contador financeiro de R$ 1.840,00, a alternância de abas, o gráfico Chart.js, a busca na tabela, a gaveta do Copilot e os downloads.

Comece agora, execute todas as fases, teste no navegador e só pare quando a aplicação estiver 100% impecável e pronta para apresentação!
