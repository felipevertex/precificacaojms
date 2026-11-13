# Planilha "Análise de Pedidos" (Etapa 1): construída em 2026-11-13

O Felipe aprovou explicitamente começar a construção ("pode começar e faça o que der pra fazer até agora"), antes de fechar o dicionário de dados. As colunas e regras abaixo são a primeira versão e **continuam sujeitas à validação dele**.

Planilha: https://docs.google.com/spreadsheets/d/16t5RS9R2Y9WAFiF3dtO4VkdE8cuM22EKqf5whV-pE_s (ID também em `SHEET_ID_ANALISE_PEDIDOS` no `.env`, que não vai para o Git).

## Como foi feito
1. `scripts/olist_buscar_pedidos.py` (roda local, usa o token do `.env`): lê da API 2.0 do Olist os pedidos dos últimos 7 dias (07 a 13/11/2026), os itens e o cadastro de cada produto. **Somente leitura.** Não guarda dados pessoais de clientes (nome, CPF, endereço, e-mail, telefone). Saída em `dados/olist_pedidos.json` (pasta ignorada pelo Git).
2. `scripts/montar_planilha.py` (roda na VPS, onde está a chave da conta de serviço do Google): cria as abas, fórmulas, formatos e cores, e grava os dados. O token do Olist não sai da máquina local, e a chave do Google não sai da VPS.

Lidos: **282 pedidos, 283 itens, 88 produtos** (6 são kits).

## Abas
| Aba | Função |
|---|---|
| LEIA-ME | Guia, cores das origens, status dos valores, regras |
| Dashboard | Totais e quebra por canal e por modalidade |
| Pedidos | Uma linha por pedido, colunas agrupadas por origem do dado |
| Itens | Uma linha por SKU vendido, com a fotografia do custo |
| Produtos e Custos | Cadastro por SKU: custo do Olist e custos adicionais (a preencher) |
| Lançamentos | Cobranças e ajustes dos marketplaces, uma linha por valor (a preencher com os relatórios) |
| Fulfillment (lotes) | Frete e preparação dos envios aos centros, para rateio (a preencher) |
| Custos indiretos | Despesas gerais e critério de rateio (a preencher) |
| Parâmetros | Alíquota estimada, custo indireto por pedido, fonte dos dados por canal |
| Logs | Histórico das importações |

## Origem de cada coluna de Pedidos
- **Olist** (A a M): pedido no canal (chave), nº Olist, data, canal (`ecommerce.nomeEcommerce`), modalidade (a partir do depósito e da forma de envio), situação, produtos, frete cobrado do cliente, descontos, receita (fórmula), NF emitida, datas de envio e entrega.
- **XML da nota** (N): ICMS. **Ainda pendente**, fora do cálculo do lucro por enquanto.
- **Custos próprios** (O e P): custo dos produtos (CMV) vem de Itens (fotografia do **custo médio** do Olist no dia da leitura); custos adicionais (embalagem, preparação, frete aos centros) vêm de Produtos e Custos e de Fulfillment.
- **Marketplace** (Q a T): comissão, tarifa fixa, frete pago, fulfillment e outras. Vêm de **Lançamentos** (fórmulas somam por pedido e tipo). Sem lançamento, o valor é `pendente`.
- **Calculado** (U a Z): imposto estimado (alíquota de Parâmetros, hoje 2,5% herdada da planilha manual), custos indiretos, reembolsos e estornos, lucro, margem e situação do dado.

## Regras implementadas
- **Pendente nunca é zero.** Valor que ainda não chegou aparece como `pendente` (amarelo). Lucro só é calculado quando todos os valores aplicáveis estão preenchidos.
- **n/a:** coluna que não se aplica (frete pago em fulfillment, qualquer custo em pedido cancelado).
- **Cancelado** fica fora do resultado.
- **Devolução** sem lançamento de reembolso fica `pendente`.
- **Custo congelado:** o custo é copiado para o item na leitura; mudar o cadastro depois não altera pedidos já importados.
- **Kit:** custo = soma do custo médio dos componentes. Se faltar um componente, o item fica `pendente`.
- Cores de origem no topo de Pedidos: azul (Olist), verde-água (XML), cinza (custos próprios), amarelo (marketplace), verde (calculado).

## Resultado desta primeira carga
- 282 pedidos: 262 no resultado e 20 cancelados.
- Receita dos pedidos no resultado: R$ 50.634,65 (ticket médio R$ 193,26).
- **Nenhum pedido está com dado completo**, como esperado: faltam comissão, tarifas, frete pago, fulfillment, embalagem, custos indiretos e ICMS.
- Custo dos produtos lido para 258 dos 262 pedidos. 4 itens sem custo utilizável (custo médio zerado no Olist): SKUs `23-DLXL-TSPF`, `923`, `L1-O349-LQJ6`.

## Limitações conhecidas desta versão
- `Produtos e Custos` não acrescenta SKUs novos em reimportações (só é preenchida na criação).
- A importação é por execução manual do script, ainda sem agendamento.
- A API 2.0 do Olist é a legada; a v3 (OAuth2) continua pendente de confirmação de acesso.
- ICMS da nota, tarifas reais e frete aos centros dependem de dados que o Felipe ainda vai fornecer.
