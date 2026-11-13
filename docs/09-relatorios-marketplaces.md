# O que pedir a cada marketplace para completar a planilha

Registro de 2026-11-13. Os nomes exatos de relatórios e menus variam e mudam com o tempo: **nada abaixo foi verificado nas contas do Felipe**. Quando o relatório certo não for encontrado, mandar o que achar que o formato é lido a partir das colunas.

## O princípio
A aba **Lançamentos** guarda **uma linha por valor cobrado em cada pedido**: nº do pedido no canal, tipo do valor e valor. As colunas de Pedidos são fórmulas que somam esses lançamentos.

| Tipo do lançamento | Alimenta a coluna | Observação |
|---|---|---|
| Comissão | Comissão | |
| Tarifa fixa | Tarifa | |
| Frete pago | Frete pago | Só estoque próprio. Em fulfillment é `n/a` |
| Fulfillment | Fulfillment | Só pedidos Full/FBA/fulfillment Magalu |
| Reembolso / Estorno | Reembolsos | Sem lançamento em pedido devolvido fica `pendente` |

Sem lançamento, a coluna fica `pendente`, **nunca zero**. O lucro só é calculado com todos os valores aplicáveis preenchidos.

## Por canal

### Mercado Livre
- Relatório de vendas/faturamento, **uma linha por venda**, Excel ou CSV.
- Colunas desejadas: nº da venda, tarifa de venda (comissão e tarifa fixa), custo de envio pago pelo vendedor, valor do envio pago pelo comprador, reembolsos e cancelamentos.
- Pedidos no **Full**: tarifa de envio e armazenagem do Full, que costuma vir na fatura mensal e não por venda.
- Risco de cruzamento: o ML usa número de venda e de pacote diferentes. Confirmar qual deles o Olist grava em `numero_ecommerce` (a chave da coluna A de Pedidos).

### Magalu
- Extrato ou relatório financeiro do Portal do Seller, uma linha por pedido: nº do pedido, comissão, tarifa (se houver), frete a cargo do vendedor, descontos, valor repassado, reembolsos e cancelamentos.
- Pedidos em fulfillment Magalu: armazenagem e preparação costumam vir separadas, e vão para a aba Fulfillment (lotes).
- **Prioridade alta:** menor margem antes das tarifas na primeira carga (19,0%). Um pedido vendido por R$ 202,95 com custo R$ 350,70.

### Amazon
- Relatório de **transações/pagamentos** do Seller Central, por período, com o nº do pedido (formato `xxx-xxxxxxx-xxxxxxx`) em cada linha.
- Colunas desejadas: comissão por referência, tarifa de FBA por pedido (FBA), frete cobrado do vendedor (DBA) e reembolsos.
- A Amazon aparece em **duas integrações** no Olist: "Amazon" (DBA, estoque próprio) e "Amazon FBA Classic" (fulfillment). O tratamento é diferente.

### Shopee e KaBuM
- Mesmo princípio: relatório de repasse ou financeiro por pedido. Ficam para depois dos três acima.
- "Fulfillment Shopee" apareceu como depósito nos pedidos. **Confirmar com o Felipe** se é um canal real.

### Casas Bahia Marketplace
- Apareceu em pelo menos um pedido (o 3559), mas não estava na lista de canais. **Confirmar com o Felipe.**

## Como entregar
1. Baixar os relatórios **dos mesmos dias da planilha** (07 a 13/11/2026, e depois os dias novos).
2. Colocar na pasta `dados/relatorios/` do projeto (ignorada pelo Git, para não subir dados de clientes).
3. Dizer o caminho na sessão. O Claude lê, converte linhas em lançamentos, **cruza o nº do pedido com a coluna A de Pedidos antes de gravar** e mostra o que não casar, em vez de chutar.

## O que vai continuar pendente mesmo com os relatórios
- **Pedidos muito recentes**: as tarifas podem não estar liquidadas ainda. Ficam `pendente` e completam em relatório mais novo.
- **Frete aos centros e armazenagem**: não vêm por pedido. Vão para a aba Fulfillment (lotes) e entram por rateio (Fase 4).
- **ICMS**: vem do XML da nota, não dos relatórios.
- **Embalagem, preparação e custos indiretos**: cadastros do Felipe.

## Alternativa: API
Na fase seguinte, pesquisar as APIs financeiras de cada marketplace para carregar sem relatório manual. Exige o Felipe autorizar a conta de vendedor no portal de desenvolvedor de cada um. Nada está confirmado.
