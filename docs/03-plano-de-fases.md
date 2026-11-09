# Plano de fases

**Regra:** não pular etapas. Nenhum código, planilha ou integração antes da aprovação explícita da Fase 7.

| Fase | Entrega | Status |
|---|---|---|
| 1. Diagnóstico e requisitos | Requisitos organizados, dúvidas e perguntas | **Em andamento.** Rodada 1 respondida, rodada 2 pendente (ver `02-fase1-diagnostico.md`) |
| 2. Pesquisa técnica e viabilidade | Matriz: informação desejada, fonte, endpoint, disponibilidade, limitações, alternativa | Não iniciada |
| 3. Arquitetura | Fluxo de dados, integrações, abas, armazenamento, sincronização, duplicidades, falhas. Sheets x Postgres. Apps Script x n8n | Não iniciada |
| 4. Modelagem financeira | Dicionário de dados, exemplos numéricos, regras para cada exceção | Não iniciada |
| 5. Projeto visual | Layout das abas, cores, dashboard, filtros, formatação condicional | Não iniciada |
| 6. Plano de implementação | Tarefas, ordem, dependências, testes e critérios de aceitação | Não iniciada |
| 7. Aprovação | Pacote completo para o Felipe aprovar | Não iniciada |

## Entrega em duas etapas (decidido em 2026-11-09)

**Etapa 1:** Olist (7 dias de pedidos) + relatórios de Mercado Livre e Amazon baixados manualmente, resultando em lucro por pedido e por SKU, com impostos estimados.

**Etapa 2:** APIs dos marketplaces, conciliação, demais canais, fulfillment completo, automação.

As fases 2 a 6 podem cobrir as duas etapas, mas a implementação começa pela Etapa 1.

## Próximo passo
Receber os itens da seção "Para o Felipe levar de casa" em `02-fase1-diagnostico.md` e fechar a Fase 1. Em seguida, iniciar a Fase 2 pelas verificações de API do Olist e dos marketplaces.
