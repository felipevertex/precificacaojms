# precificacaojms: contexto para sessões do Claude Code

> Carregado automaticamente em qualquer sessão neste repositório. Serve para retomar o projeto sem depender do histórico de conversas.

**👉 Comece por `RETOMAR.md`** (estado atual, lembretes, próximos passos) e depois `ROADMAP.md` (lembrete rápido no topo).

## O que é

Sistema de rentabilidade por pedido para o ecommerce da **JMS** (informática, Cuiabá-MT). Interface: Google Sheets. Fonte dos pedidos: ERP **Olist** (Tiny, API v3). Marketplaces: Mercado Livre, Shopee, Amazon, Magalu, KaBuM. Fulfillment em Mercado Livre, Amazon e Magalu. Volume: 20 a 50 pedidos por dia. Regime tributário: Lucro Presumido.

Repositório separado do `jmsecom` (portal de agentes da Vertex). Quem trabalha aqui é o **Felipe**.

## Regra nº 1: planejamento antes de código

**Não programar, criar planilhas ou implementar integrações sem aprovação explícita do Felipe.** Em 2026-11-13 ele aprovou iniciar a Etapa 1 (planilha com os pedidos do Olist, ver `docs/07-planilha-etapa1.md`). Fora desse escopo, volta a valer a regra: planejar e aprovar antes. O projeto avança por fases (ver `docs/03-plano-de-fases.md`) e não se pula etapa. Antes de qualquer implementação, apresentar: requisitos, arquitetura, estrutura da planilha, modelo financeiro, estratégia de integração, plano e riscos.

## Como o Felipe quer que eu trabalhe

- Ser crítico e técnico; não concordar automaticamente. Se houver solução melhor, dizer e justificar.
- Precisão financeira vale mais que aparência.
- Não inventar endpoints, tarifas, alíquotas ou regras fiscais. Quando faltar informação, dizer e propor alternativa.
- Não tratar dado ausente como zero sem marcar como pendente.
- Decisão técnica importante: apresentar alternativas, prós, contras e recomendação.
- Perguntas em pequenos blocos; não repetir o que já foi respondido.
- Estimativa gerencial de imposto nunca se confunde com apuração fiscal oficial. Regras tributárias precisam ser validadas pelo contador.
- Valor líquido de repasse não é lucro líquido.

## Decisões já tomadas

Ver `docs/02-fase1-diagnostico.md`. Em resumo: Sheets como interface agora, Postgres depois (a VPS da Vertex já tem), com a lógica em script e não em fórmulas para facilitar a migração. Entrega em duas etapas: primeiro lucro por pedido a partir do Olist mais relatórios dos marketplaces, depois automação por API.

## Estado atual (2026-11-13)

Etapa 1 em andamento. A planilha "Análise de Pedidos" tem 282 pedidos e é **atualizada sozinha a cada 30 minutos** por um cron na VPS (`scripts/importar_pedidos.py`). Não calcula lucro ainda: faltam os relatórios dos marketplaces (Mercado Livre e Magalu primeiro, depois Amazon, Shopee, KaBuM), o ICMS do XML, embalagem/preparação por SKU, frete aos centros e custos indiretos. O token do Olist precisa ser trocado. Lista completa em `RETOMAR.md`.

## Como o código está organizado

- `scripts/regras.py` é a **fonte única** das colunas e fórmulas de Pedidos, Itens e Produtos e Custos. Mudança de coluna ou fórmula: só ali.
- `scripts/olist.py`: cliente somente leitura da API 2.0 do Olist. `scripts/sheets_util.py`: conexão com o Google Sheets (converte `,` em `;` nas fórmulas por causa do locale pt_BR).
- `scripts/montar_planilha.py` constrói a planilha (`--reset` apaga o que foi lançado à mão: cuidado). `scripts/importar_pedidos.py` é a rotina incremental do cron.
- Onde roda: token do Olist local e na VPS; chave do Google só na VPS. Detalhes em `docs/10-operacao-vps.md`.
- Pendências de cada lado (Felipe e Claude): `RETOMAR.md`.

## Permissões e cuidados
- Instalar ou alterar agendamento (cron) e mexer na VPS exigem a autorização **explícita e atual** do Felipe no chat. O cron atual foi autorizado em 2026-11-13. Quando a política de segurança bloqueia uma ação, não contornar: pedir a autorização.

## Segurança

Nunca commitar tokens, client secrets, chaves de API, planilhas reais ou relatórios com dados pessoais de clientes. Credenciais ficam fora do repositório.
