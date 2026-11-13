# Roadmap

Atualizado em 2026-11-13. **Fonte de verdade: este arquivo.** A versão visual privada (https://claude.ai/artifact/LVifwWVvkMQBGVT1PYDDTE) pode estar desatualizada.

> 👉 **Retomando de outra sessão? Leia primeiro [`RETOMAR.md`](RETOMAR.md).**

## 🔔 LEMBRETE RÁPIDO (2026-11-13)

**Onde estamos:** a Etapa 1 está em construção. A planilha "Análise de Pedidos" existe, tem 282 pedidos dos últimos 7 dias e **se atualiza sozinha a cada 30 minutos** (cron na VPS). Ainda **não calcula lucro**: faltam os dados dos marketplaces.

**Próximo passo:** o Felipe traz os **relatórios por pedido do Mercado Livre e do Magalu** (depois Amazon) em `dados/relatorios/`. Guia do que pedir: [`docs/09-relatorios-marketplaces.md`](docs/09-relatorios-marketplaces.md).

**Pendências rápidas**
- [ ] 🔐 Trocar o token do Olist (apareceu no chat)
- [ ] Relatórios de Mercado Livre e Magalu (07 a 13/11); depois Amazon, Shopee, KaBuM
- [ ] 3 SKUs com custo médio zerado: `23-DLXL-TSPF`, `923`, `L1-O349-LQJ6`
- [ ] Confirmar canais "Casas Bahia Marketplace" e "Fulfillment Shopee"
- [ ] Conferir que o cron roda (aba Logs + `/var/log/precificacao.log`)
- [ ] Contador valida a alíquota estimada (hoje 2,5%, herdada da planilha manual)

## Estado por frente

| Frente | Estado |
|---|---|
| Planilha "Análise de Pedidos" | ✅ Criada (10 abas), carregada |
| Importação do Olist | ✅ Automática, a cada 30 min (07h às 22h Cuiabá) |
| Custo do produto por item | ✅ Congelado na importação; 3 SKUs sem custo |
| Comissão, tarifa, frete pago, fulfillment | ⏳ Aguardam relatórios dos marketplaces |
| ICMS da nota | ⏳ Pendente (XML) |
| Embalagem, preparação, frete aos centros, indiretos | ⏳ Cadastros e rateio a fazer |
| Preço mínimo por SKU/canal | ⏳ A fazer |
| APIs financeiras dos marketplaces | ⏳ Etapa 2, pesquisa não iniciada |
| Postgres | ⏳ Depois |

**Regra original:** nenhum código antes da aprovação da Fase 7. **Exceção:** em 2026-11-13 o Felipe aprovou explicitamente iniciar a Etapa 1 (ver `docs/07-planilha-etapa1.md`). O que vai além dela volta a exigir aprovação.

```mermaid
flowchart LR
    F1["1 Diagnóstico<br/>e requisitos<br/><b>EM ANDAMENTO</b>"] --> F2["2 Pesquisa técnica<br/>e viabilidade"]
    F2 --> F3["3 Arquitetura"]
    F3 --> F4["4 Modelagem<br/>financeira"]
    F4 --> F5["5 Projeto visual"]
    F5 --> F6["6 Plano de<br/>implementação"]
    F6 --> F7{"7 Aprovação<br/>do Felipe"}
    F7 --> E1["Etapa 1<br/>Lucro por pedido<br/>(Olist + relatórios)"]
    E1 --> E2["Etapa 2<br/>APIs, conciliação,<br/>demais canais"]
    style F1 fill:#f8ecd2,stroke:#b0700f
    style E1 fill:#f8ecd2,stroke:#b0700f
```

## Agora: fechar a Fase 1

Itens que o Felipe precisa trazer:

- [ ] Prints das regras de tributação e da natureza de operação no Olist
- [ ] Um pedido de kit do Olist (composição e custo)
- [ ] Relatório de cobranças do Mercado Livre e da Amazon, sem dados pessoais de clientes
- [ ] Confirmar que é administrador de cada conta de marketplace (credenciais de API)
- [ ] Conferir se "Aplicativos API V3" aparece em Configurações da conta Olist (plano Domine)

Depois, segunda rodada de perguntas: custos fixos mensais, faturamento aproximado, prazo de repasse de cada canal, quantidade de SKUs ativos e quem mais usará a planilha.

## As 7 fases

| # | Fase | O que entrega | Status |
|---|---|---|---|
| 1 | Diagnóstico e requisitos | Requisitos organizados, dúvidas e perguntas | Em andamento |
| 2 | Pesquisa técnica e viabilidade | Matriz: informação, fonte, endpoint, disponibilidade, limitações, alternativa. Olist API v3, APIs financeiras dos 5 canais, extratos de fulfillment, ICMS no XML da nota | A fazer |
| 3 | Arquitetura | Fluxo de dados, abas, armazenamento, sincronização, duplicidades, falhas. Sheets x Postgres. Apps Script x n8n | A fazer |
| 4 | Modelagem financeira | Dicionário de dados, fotografia do custo, impostos em 3 camadas, rateio do frete aos centros, regras para 19 exceções, exemplos numéricos | A fazer |
| 5 | Projeto visual | Abas, cabeçalhos, cores, dashboard, filtros, formatação condicional | A fazer |
| 6 | Plano de implementação | Tarefas, dependências, testes, critérios de aceitação, backup e controle de acesso | A fazer |
| 7 | Aprovação | Pacote completo (requisitos, arquitetura, planilha, modelo financeiro, integração, plano, riscos) | A fazer |

## Entrega em duas etapas

**Etapa 1, onde está o prejuízo:** pedidos do Olist de pelo menos 7 dias, relatórios de Mercado Livre e Amazon baixados à mão, lucro por pedido e por SKU, imposto estimado (marcado como estimativa), embalagem, preparação e frete aos centros entrando no custo.

**Etapa 2, automação:** APIs financeiras dos marketplaces, conciliação, demais canais (Shopee, Magalu, KaBuM), fulfillment completo, possível migração para Postgres.

## Decisões tomadas

| Tema | Decisão |
|---|---|
| Base de dados | Google Sheets agora, Postgres depois. Lógica em script, ID único por pedido e item |
| Fonte do pedido | Olist: pedido, itens, SKU, custo e nota |
| Comissão, tarifa e repasse | Do marketplace, por API ou relatório importado. O Olist mostra valores defasados |
| Custo do produto | Copiado para o pedido na importação, nunca relido. Retroativo aproximado e marcado |
| Impostos | 3 camadas: ICMS da nota, federais sobre a receita, calibração mensal. Contador valida os parâmetros |
| Entrega | Duas etapas, do zero, com pelo menos 7 dias de histórico para teste |

## Pendentes

| Tema | Situação |
|---|---|
| API v3 no plano Domine | Pesquisa indica que sim (120 requisições por minuto). Confirmar na conta |
| n8n | Avaliar na Fase 3. Não obrigatório |
| Critério de rateio dos custos indiretos | Fase 4, depende dos custos fixos |
| Regras de ICMS e substituição tributária | Prints do Olist e confirmação do contador |

## Riscos

- Tarifas reais fora do Olist: relatório diário agora, API por canal onde existir.
- Frete aos centros não contabilizado: lucro dos produtos em fulfillment superestimado hoje. Rateio por lote na Fase 4.
- Limites do Google Sheets (10 milhões de células, cotas do Apps Script): dados tabulares e IDs estáveis para migrar.
- Custo antigo desconhecido: fotografia daqui para frente, retroativo aproximado.
- Imposto por pedido é estimativa gerencial: conferir todo mês com o contador.
