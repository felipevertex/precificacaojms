# precificacaojms: contexto para sessões do Claude Code

> Carregado automaticamente em qualquer sessão neste repositório. Serve para retomar o projeto sem depender do histórico de conversas.

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

## Estado atual

Etapa 1 iniciada: planilha criada e carregada com 282 pedidos. Faltam os relatórios dos marketplaces, o cadastro de custos adicionais e a validação das colunas. Pendências do Felipe estão na seção "Perguntas em aberto" de `docs/02-fase1-diagnostico.md`.

## Segurança

Nunca commitar tokens, client secrets, chaves de API, planilhas reais ou relatórios com dados pessoais de clientes. Credenciais ficam fora do repositório.
