# Requisitos: resumo em uma página

Versão enxuta do briefing (`00-briefing-original.md`). Em caso de dúvida, vale o briefing.

## Contexto
- Empresa: JMS, ecommerce de informática, Cuiabá-MT. Regime: **Lucro Presumido**.
- Canais: Mercado Livre, Shopee, Amazon, Magalu, KaBuM (uma conta em cada).
- Fulfillment: Mercado Livre, Amazon, Magalu.
- ERP: **Olist ERP (Tiny), API v3**, plano Domine. Pedidos dos marketplaces entram de forma nativa, inclusive os do fulfillment.
- Volume: 20 a 50 pedidos por dia.
- Stack preferida: Google Sheets (interface), Apps Script (processamento), API do Olist, n8n a avaliar sem obrigatoriedade.

## O que o sistema precisa responder ao fim do dia
Quanto vendi, gastei, paguei aos marketplaces, paguei de imposto, custaram os produtos, gastei com fulfillment, recebi de fato, lucrei, quais pedidos deram prejuízo e qual marketplace rende mais.

## Componentes do resultado de cada pedido (todos separados, nada escondido)
Receita bruta, descontos, comissão, tarifa fixa, outras tarifas, frete pago pelo vendedor, fulfillment, impostos, custo de aquisição, embalagem e preparação, custos indiretos, ajustes, valor líquido recebido, lucro ou prejuízo e margem %.

## Regras de ouro
1. Valores reais do marketplace prevalecem sobre estimativa; nunca aplicar comissão genérica quando houver o valor cobrado.
2. Dado ausente = status "pendente", nunca zero silencioso.
3. Custo de aquisição congelado no pedido (fotografia histórica). Mudança posterior no cadastro não altera pedidos antigos.
4. Sem pedido duplicado (ID único), com atualização, rastreabilidade, reprocessamento, logs e recuperação de falhas.
5. Cancelado, devolvido e reembolsado não contam como venda normal.
6. Imposto estimado por pedido é estimativa gerencial, nunca apuração fiscal. Regras validadas pelo contador.
7. Valor líquido de repasse não é lucro líquido.
8. Custos diretos e indiretos aparecem separados.
9. Credenciais nunca em célula da planilha nem no repositório.

## Dois controles distintos
- **Rentabilidade econômica** do pedido (lucro e margem).
- **Conciliação financeira** (previsto x realizado), com status: Conciliado, Pendente, Divergente, Parcialmente conciliado, Cancelado, Reembolsado.

## Custos a modelar
- Aquisição (vem do Olist), adicionais por SKU (embalagem, caixa, bolha, fita, etiqueta, mão de obra), indiretos com rateio justificado.
- Fulfillment: armazenagem, manuseio, preparação, expedição, estoque parado, devolução, retirada. **Frete e preparação do envio de lotes aos centros de distribuição** entram no custo das unidades enviadas, com rateio rastreável.

## Estrutura de abas proposta (a revisar na Fase 3 e 5)
Dashboard, Pedidos, Itens dos pedidos, Produtos e custos, Taxas e marketplaces, Impostos, Fulfillment, Conciliação, Custos indiretos, Logs e sincronização, Configurações.

## Exceções que precisam de regra documentada (Fase 4)
Pedido multi-SKU, cancelamento antes e depois da expedição, devolução total e parcial, reembolso parcial, mudança de comissão, ajuste de frete, subsídio, cupom, desconto do vendedor x do marketplace, fulfillment, custo ausente, SKU sem custo adicional, divergência Olist x marketplace, falha de importação, reprocessamento.

## Fases
Ver `03-plano-de-fases.md`.
