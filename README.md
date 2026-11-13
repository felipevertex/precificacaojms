# precificacaojms

Sistema de gestão de rentabilidade e controle financeiro por pedido para o ecommerce da JMS (nicho de informática), com Google Sheets como interface, integrado ao ERP Olist e aos marketplaces.

**Objetivo final:** cada pedido dos marketplaces registrado automaticamente, com todos os custos discriminados e o lucro ou prejuízo real daquela operação.

## Status

> 👉 **Retomando? Leia [`RETOMAR.md`](RETOMAR.md):** o que está no ar, o que falta e a primeira mensagem sugerida para a próxima sessão.

**Etapa 1 em andamento (iniciada em 2026-11-13 por autorização explícita do Felipe):** planilha "Análise de Pedidos" criada com 282 pedidos lidos do Olist (somente leitura) e **atualizada automaticamente a cada 30 minutos** por um cron na VPS. Ainda sem lucro calculado: faltam os relatórios dos marketplaces. Os documentos de planejamento continuam valendo e as colunas ainda precisam da validação dele. Ver `docs/07-planilha-etapa1.md`.

Veja o andamento em [`docs/03-plano-de-fases.md`](docs/03-plano-de-fases.md).

## Roadmap

Veja [`ROADMAP.md`](ROADMAP.md): lembrete rápido no topo, estado por frente, fases, decisões e riscos, com diagrama.

## Documentos

| Arquivo | Conteúdo |
|---|---|
| [`docs/00-briefing-original.md`](docs/00-briefing-original.md) | O briefing completo do projeto, como foi escrito. Fonte de verdade dos requisitos |
| [`docs/01-requisitos-resumo.md`](docs/01-requisitos-resumo.md) | Requisitos organizados em uma página |
| [`docs/02-fase1-diagnostico.md`](docs/02-fase1-diagnostico.md) | Pontos críticos, respostas do Felipe, decisões tomadas e perguntas em aberto |
| [`docs/03-plano-de-fases.md`](docs/03-plano-de-fases.md) | As 7 fases, o que cada uma entrega e onde estamos |
| [`docs/04-historico-da-conversa.md`](docs/04-historico-da-conversa.md) | Registro cronológico completo da conversa de planejamento (perguntas, respostas, explicações) |
| [`docs/06-analise-planilha-manual.md`](docs/06-analise-planilha-manual.md) | Análise da planilha manual do Felipe: o que manter, os problemas e o que acrescentar |
| [`docs/07-planilha-etapa1.md`](docs/07-planilha-etapa1.md) | A planilha "Análise de Pedidos" construída: abas, origem de cada coluna, regras e resultado da primeira carga |
| [`docs/08-sessao-2-etapa1.md`](docs/08-sessao-2-etapa1.md) | Diário da sessão 2: leitura do Olist, construção da planilha, importação automática, problemas e decisões |
| [`docs/09-relatorios-marketplaces.md`](docs/09-relatorios-marketplaces.md) | O que pedir de cada marketplace (ML, Magalu, Amazon, Shopee, KaBuM) para completar a planilha |
| [`docs/10-operacao-vps.md`](docs/10-operacao-vps.md) | Onde cada peça roda, o cron, como conferir, rodar na mão, desligar, armadilhas |
| [`docs/05-referencias.md`](docs/05-referencias.md) | Fontes, links e o que ainda falta pesquisar. Inclui `docs/_olist_api_original.md` (notas de API já levantadas) |

## Como retomar uma sessão

1. `git pull`
2. Ler `RETOMAR.md` (lembretes e próximos passos) e `CLAUDE.md`
3. Conferir `ROADMAP.md` (lembrete rápido no topo)

## Segurança

Nunca versionar tokens, client secrets, chaves de API ou planilhas com dados reais de clientes. Ver `.gitignore`.
