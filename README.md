# precificacaojms

Sistema de gestão de rentabilidade e controle financeiro por pedido para o ecommerce da JMS (nicho de informática), com Google Sheets como interface, integrado ao ERP Olist e aos marketplaces.

**Objetivo final:** cada pedido dos marketplaces registrado automaticamente, com todos os custos discriminados e o lucro ou prejuízo real daquela operação.

## Status

**Fase 1 (diagnóstico e requisitos) em andamento. Nada foi implementado ainda: sem planilha, sem script, sem integração.** O projeto segue um planejamento em fases e só começa a programar após aprovação explícita do Felipe.

Veja o andamento em [`docs/03-plano-de-fases.md`](docs/03-plano-de-fases.md).

## Documentos

| Arquivo | Conteúdo |
|---|---|
| [`docs/00-briefing-original.md`](docs/00-briefing-original.md) | O briefing completo do projeto, como foi escrito. Fonte de verdade dos requisitos |
| [`docs/01-requisitos-resumo.md`](docs/01-requisitos-resumo.md) | Requisitos organizados em uma página |
| [`docs/02-fase1-diagnostico.md`](docs/02-fase1-diagnostico.md) | Pontos críticos, respostas do Felipe, decisões tomadas e perguntas em aberto |
| [`docs/03-plano-de-fases.md`](docs/03-plano-de-fases.md) | As 7 fases, o que cada uma entrega e onde estamos |
| [`docs/04-historico-da-conversa.md`](docs/04-historico-da-conversa.md) | Registro cronológico completo da conversa de planejamento (perguntas, respostas, explicações) |
| [`docs/05-referencias.md`](docs/05-referencias.md) | Fontes, links e o que ainda falta pesquisar. Inclui `docs/_olist_api_original.md` (notas de API já levantadas) |

## Como retomar uma sessão

1. `git pull`
2. Ler `CLAUDE.md` e `docs/02-fase1-diagnostico.md` (seção "Perguntas em aberto")
3. Continuar da fase indicada em `docs/03-plano-de-fases.md`

## Segurança

Nunca versionar tokens, client secrets, chaves de API ou planilhas com dados reais de clientes. Ver `.gitignore`.
