# RETOMAR: leia isto primeiro

Atualizado em **2026-11-13** (fim da sessão 2). Resumo de uma página para continuar de outra sessão, outra máquina ou outra conta. O detalhe está nos links.

## Em uma frase
A planilha **"Análise de Pedidos"** já existe, tem os pedidos dos últimos 7 dias lidos do Olist e se **atualiza sozinha a cada 30 minutos**. Ela ainda **não calcula nenhum lucro** porque faltam os dados dos marketplaces (comissão, tarifa, frete pago, fulfillment). Esses dados dependem do Felipe trazer os relatórios.

## O que está no ar (feito e funcionando)
| Item | Situação |
|---|---|
| Planilha Google "Análise de Pedidos" | Criada, 10 abas. ID em `SHEET_ID_ANALISE_PEDIDOS` no `.env` local (não versionado). Estrutura em `docs/07-planilha-etapa1.md` |
| Carga inicial | 282 pedidos, 283 itens, 88 produtos (07 a 13/11/2026) |
| Importação automática | **Cron instalado na VPS** (a cada 30 min, 07h às 22h de Cuiabá). Autorizado pelo Felipe em 2026-11-13. Detalhes e comandos em `docs/10-operacao-vps.md` |
| Token do Olist | Em `.env` local e em `/opt/precificacao/olist.env` na VPS. **Precisa ser trocado** (ver abaixo) |
| Documentação | Este arquivo, `ROADMAP.md`, `docs/00` a `docs/10` |

## 🔔 Lembretes (o que ainda precisa acontecer)

### Do Felipe (bloqueia o lucro por pedido)
1. **Trocar o token do Olist.** Ele apareceu no chat e foi para o servidor. Gerar novo no Olist e atualizar `.env` local e `/opt/precificacao/olist.env`. Nada precisa mudar no código.
2. **Baixar os relatórios por pedido, dos dias 07 a 13/11**, de Mercado Livre, Magalu e Amazon (e Shopee e KaBuM depois). O que pedir de cada um: `docs/09-relatorios-marketplaces.md`. Colocar em `dados/relatorios/` (pasta ignorada pelo Git) e dizer o caminho.
3. **Resolver 3 SKUs com custo médio zerado no Olist:** `23-DLXL-TSPF`, `923`, `L1-O349-LQJ6`.
4. **Confirmar canais:** "Casas Bahia Marketplace" e "Fulfillment Shopee" são canais reais?
5. **Prints do Olist:** regras de tributação e natureza de operação. Um pedido de kit.
6. **Confirmar** se é administrador de cada conta de marketplace e se "Aplicativos API V3" aparece nas configurações do Olist.
7. **Perguntas da planilha manual:** colunas ocultas C/D/E/J, origem da tarifa Amazon, significado de "Pagamento", origem dos 2,5% de imposto, contratos de Total Express e Correios (`docs/06-analise-planilha-manual.md`).
8. **Contador (uma vez):** confirmar a alíquota estimada usada em `Parâmetros!B2` (hoje 2,5% herdada da planilha manual, **não validada**) e a regra de ICMS/ST.

### Do Claude, na próxima sessão (nesta ordem)
1. Conferir que o cron está rodando: aba **Logs** deve ter uma linha nova a cada 30 minutos, e `ssh` na VPS: `tail /var/log/precificacao.log`.
2. Quando o Felipe trouxer o relatório do **Mercado Livre**: ler as colunas, montar o importador de lançamentos, **cruzar o nº do pedido com a coluna A de Pedidos antes de gravar** (no ML venda e pacote têm números diferentes) e mostrar o que não casar.
3. Repetir para Magalu e Amazon.
4. Ler o ICMS no XML da nota (coluna N de Pedidos, hoje `pendente`, fora do cálculo).
5. Cadastro de embalagem e preparação por SKU (colunas cinzas de Produtos e Custos), rateio do frete aos centros (aba Fulfillment (lotes)), custos indiretos (aba Custos indiretos).
6. Aba de **preço mínimo** por SKU/canal/modalidade.
7. Pequeno ajuste: `scripts/olist_buscar_pedidos.py` ainda tem cópias próprias das funções de `scripts/olist.py`. Refatorar.

### Por que o Magalu e o ML primeiro
Na primeira carga, **Magalu teve a menor margem antes das tarifas (19,0%)** e um pedido vendido por R$ 202,95 com custo R$ 350,70. O ML tem o maior volume. Os dois juntos dão a visão mais útil.

## Regras que não podem ser quebradas
- **Dado ausente nunca vira zero.** Fica `pendente`. Lucro só aparece com `Dado = Completo`.
- **Custo congelado:** copiado para o item na importação, não relido.
- **Imposto é estimativa gerencial**, não apuração fiscal. Contador valida parâmetros.
- **Somente leitura** no Olist. Nunca escrever nada lá.
- **Segredos fora do Git:** `.env`, tokens, chave do Google, relatórios com dados de clientes. A pasta `dados/` é ignorada.
- Regra de implementação em `CLAUDE.md`: fora da Etapa 1 aprovada, planejar e aprovar antes de construir.

## Primeira mensagem sugerida para a próxima sessão
> Leia `RETOMAR.md` e `ROADMAP.md`. Confira se o cron da importação está rodando (aba Logs e `/var/log/precificacao.log`). Depois vamos pelos relatórios dos marketplaces: segue a pasta `dados/relatorios/`.

## Mapa rápido dos documentos
| Para quê | Arquivo |
|---|---|
| Visão e fases | `ROADMAP.md`, `docs/03-plano-de-fases.md` |
| O que decidimos e o que está em aberto | `docs/02-fase1-diagnostico.md` |
| A planilha: abas, colunas, regras | `docs/07-planilha-etapa1.md` |
| O que pedir de cada marketplace | `docs/09-relatorios-marketplaces.md` |
| Onde as coisas rodam, como conferir, como desligar | `docs/10-operacao-vps.md` |
| Diário detalhado das sessões | `docs/04-historico-da-conversa.md` (sessão 1) e `docs/08-sessao-2-etapa1.md` (sessão 2) |
| Análise da planilha manual dele | `docs/06-analise-planilha-manual.md` |
