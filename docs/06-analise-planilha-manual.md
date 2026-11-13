# Análise da planilha manual do Felipe (2026-11-13)

Base: print da planilha "Relação de Pedidos JMS" (pedidos Amazon de jan a mar/2024, preenchida com copiar e colar). Versão visual com a prévia da nova aba: https://claude.ai/artifact/9nyX9HKHucswj69RfHwzFi (privada).

## Colunas visíveis
Pedido, Data Pedido, Valor, Custo, Tarifa Amazon, Tipo Envio, V. Frete Pg, V. Frete NFe, Dif. Frete, Situação, Data Atualização, Lucro bruto, P. de Entrega, Pagamento, Imposto, Lucro. Há colunas ocultas (C, D, E e J) que ainda não sabemos o que são.

## Lógica deduzida dos números (conferida em várias linhas)
- `Dif. Frete = V. Frete NFe − V. Frete Pg`
- `Lucro bruto = Valor − Custo − Tarifa + Dif. Frete`
- `Imposto = 2,5% do Valor`
- `Lucro = Lucro bruto − Imposto`

## Problemas encontrados
1. **Devolução não reduz o lucro.** Linhas com situação "Devolução" seguem com lucro positivo (linhas 260, 321 e 505, por exemplo). O resultado está superestimado.
2. **Frete pago vazio vira ganho.** Pedido 701-0574230-5337063: frete pago em branco, frete da nota R$ 46,37, e a planilha soma esse valor como lucro (R$ 80,19 no total). Viola a regra de que dado ausente não vale zero.
3. **Embalagem, preparação, indiretos e frete aos centros não entram em lugar nenhum.** O "Lucro" ainda não é lucro.
4. **Tarifa num único campo.** Comissão, tarifa fixa, fulfillment e outras cobranças ficam misturadas. Os valores aparecem em percentuais quase redondos (10%, 12%, 13%, 14%): é preciso saber se vieram do relatório da Amazon ou de um percentual por categoria.
5. **Um custo por pedido.** Pedido com vários SKUs não se abre; não dá para medir a rentabilidade por produto.
6. **Imposto fixo de 2,5%.** Estimativa única, sem separar o ICMS real da nota.
7. **Nomes.** "Lucro bruto" aqui é margem de contribuição antes do imposto.

## O que manter
Pedido e data (chave única), tipo de envio (vira modalidade logística), data de atualização (controle de sincronização), prazo de entrega e **data de pagamento** (base do fluxo de caixa), a comparação frete pago x frete da nota.

## O que acrescentar
Embalagem e preparação por SKU; frete de envio aos centros, rateado por lote; taxas de fulfillment; devolução (valor reembolsado, custo logístico, produto voltou ao estoque); descontos, cupons e subsídios (quem pagou); custos indiretos rateados; ICMS e tributos reais da nota; custo do prazo de recebimento (antecipação, capital de giro); quantidade e SKU por item; **situação do dado** em cada valor (real, estimado, pendente); datas prevista e real de pagamento.

## Para precificar
O pedido sozinho não basta. Uma aba por SKU, canal e modalidade com custo total unitário, tarifa e imposto, e o **preço mínimo para a margem desejada**. Fórmula-base a validar na Fase 4: `preço mínimo = (custo total unitário + frete esperado) ÷ (1 − tarifa% − imposto% − margem alvo%)`.

## Achados na leitura do Olist
- O pedido 3559 veio de **Casas Bahia Marketplace**, canal que não estava na lista de cinco.
- A Amazon aparece em duas integrações: "Amazon" (DBA, estoque próprio) e "Amazon FBA Classic" (fulfillment).

## Perguntas ao Felipe
1. O que são as colunas ocultas C, D, E e J?
2. A "Tarifa Amazon" veio do relatório da Amazon ou foi calculada por percentual?
3. A coluna "Pagamento" é a data prevista ou a data em que o dinheiro caiu?
4. Casas Bahia Marketplace é um canal que vocês usam?
5. Os 2,5% de imposto vieram do contador? Sobre qual base?
6. "Total Express" e "Correios" nessa planilha são envios com contrato próprio?
