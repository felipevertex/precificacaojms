# Fase 1: diagnóstico (2026-11-09)

Registro da primeira conversa de levantamento: o que sabemos, o que decidimos e o que falta.

## Situação de negócio
A empresa **não tem cálculo de lucro hoje**. Cresceu faturando sem medir, e agora não está conseguindo pagar as contas. Por isso a prioridade é **descobrir rápido onde o dinheiro é perdido** (SKUs e canais com prejuízo), e não montar primeiro o sistema perfeito.

Observação: lucro por pedido não explica sozinho o problema de caixa. Prazo de repasse dos marketplaces, dinheiro parado em estoque e em fulfillment pesam no caixa. Vale olhar isso depois.

## Pontos críticos levantados e respostas do Felipe

### 1. Onde estão as tarifas reais por pedido
- Os valores de comissão, tarifa e frete que o Olist mostra são **estimativas defasadas, não confiáveis**.
- Decisão: o Olist será fonte de **pedido, itens, SKU, custo e nota**. Comissão, tarifa, frete e repasse virão do **marketplace**, por API ou por relatório importado.
- Contexto: há meses o Felipe usava o **Gestor Seller**, que pegava comissões por API, mas só em 1 ou 2 marketplaces. Meta: fazer algo parecido, mais preciso e cobrindo os 5 canais.
- Modelo de dados: cada lançamento financeiro guarda a **fonte** (API ou relatório importado). Onde houver API, automatiza. Onde não houver, o Felipe sobe o relatório diário.
- A conferir na Fase 2: quais APIs financeiras cada marketplace realmente oferece (nada confirmado ainda).

### 2. Base de dados
- Começar no **Google Sheets**, por estar iniciando. Migrar depois para **Postgres** (a VPS da Vertex já tem), com orientação do Claude.
- Para a migração ser simples: lógica em script (não em fórmulas), dados em abas tabulares, **ID único por pedido e por item**, registro de eventos financeiros apenas acrescentado (nunca sobrescrito).
- Riscos do Sheets a lembrar: limite de 10 milhões de células, cotas do Apps Script, auditoria e histórico de alterações mais difíceis.

### 3. Fotografia histórica do custo
- Ao importar um pedido, o custo do SKU é **copiado para a linha do pedido** e nunca relido do cadastro.
- O Felipe atualiza o custo no Olist **todo mês, como custo médio**. Funciona bem para a frente. Para pedidos antigos, o Olist só informa o custo de hoje, então o retroativo é **aproximado** e deve vir marcado.
- Kits: o Felipe vende kits. A composição e o custo do kit precisam ser entendidos (ver perguntas).

### 4. Impostos (Lucro Presumido)
Estrutura combinada, a validar com o contador:
- **ICMS:** possivelmente lido da nota fiscal que o Olist já emite (a verificar na Fase 2).
- **PIS, COFINS, IRPJ e CSLL:** percentual sobre a receita. É regra geral do comércio no Lucro Presumido, e o contador precisa confirmar os valores.
- **Calibração mensal:** ao fechar o mês, comparar a estimativa do sistema com o total apurado pelo contador e ajustar a alíquota efetiva.
- Princípio: o contador valida os parâmetros uma vez, o sistema calcula. A precificação fica com o Felipe. Hoje o contador ajuda por WhatsApp e faz algumas apurações.
- Estimativa gerencial nunca se apresenta como apuração fiscal.

## Respostas da primeira rodada

| Tema | Resposta |
|---|---|
| Plano Olist | **Domine**. Não se sabe se a API v3 está liberada. Pesquisa indica API v3 nos planos pagos a partir do Construa, com Domine em 120 requisições por minuto (fonte: blog independente e central de ajuda). **Confirmar na conta** |
| Entrada dos pedidos | Integração nativa Olist-marketplace, inclusive os do fulfillment |
| Dados financeiros no Olist | Não confiáveis (estimativas defasadas). Querem puxar direto do marketplace ou por relatório manual |
| Histórico | Começar do zero, mas importar **pelo menos 7 dias** para teste |
| Canais de maior venda | Acredita que sejam Amazon e Mercado Livre (a confirmar com dados) |
| Cálculo de lucro atual | Não existe |
| Custo no Olist | Atualizado mensalmente, equivale a custo médio. Há kits |
| Embalagem e preparação | Hoje não são consideradas, precisam ser formalizadas |
| Regras fiscais no Olist | Existem regras cadastradas. Precisam ser levantadas |
| Extratos de fulfillment | Existem, mas o acesso é manual. Verificar se há API |
| Frete aos centros de distribuição | Feito por terceirizados. **Hoje não entra no custo dos produtos enviados** |

## Decisão de abordagem: duas etapas
- **Etapa 1 (rápida):** pedidos do Olist de 7 dias mais relatórios do Mercado Livre e da Amazon baixados à mão. Entrega lucro por pedido e por SKU com imposto estimado. Responde onde há prejuízo.
- **Etapa 2:** automação por API dos marketplaces, conciliação, demais canais.

## Perguntas em aberto

### Para o Felipe levar de casa
1. **Olist:** prints das regras de tributação e da natureza de operação. Um pedido de **kit** para ver como o custo é composto.
2. **Relatórios:** um relatório de cobranças do **Mercado Livre** e outro da **Amazon**, sem dados pessoais de clientes.
3. **Acessos:** ele é administrador de cada conta de marketplace? Isso permite criar as credenciais de API.
4. **Olist API:** confirmar se "Aplicativos API V3" aparece em Configurações da conta.
5. **Contador:** quais parâmetros ele consegue confirmar (presunção de IRPJ e CSLL, PIS e COFINS cumulativos, regra de ICMS e substituição tributária)?

### Ainda não perguntadas
- Quais custos fixos mensais compõem os custos indiretos (aluguel, folha, ferramentas) e qual o faturamento mensal aproximado?
- Quem mais vai usar a planilha (controle de acesso)?
- Prazo de repasse de cada marketplace.
- Quantos SKUs ativos?

## Verificações técnicas para a Fase 2
Nada abaixo está confirmado.
- Olist API v3: autenticação OAuth2 (endpoints de token ainda não localizados no levantamento anterior do repo `jmsecom`), pedidos e itens, custos de produto, notas, contas a receber, webhooks, limites e paginação.
- APIs financeiras: Mercado Livre, Amazon (finanças), Shopee, Magalu, KaBuM.
- API ou extrato para fulfillment de Mercado Livre, Amazon e Magalu.
- Se o XML da nota emitida pelo Olist traz o ICMS por item.
- Comparação das arquiteturas: Apps Script, n8n, ou os dois.

## Atualização 2026-11-13
- A Etapa 1 foi iniciada (ver `07-planilha-etapa1.md` e `08-sessao-2-etapa1.md`). O Olist está sendo lido pela **API 2.0 (token)**; a v3 continua sem confirmação.
- Respondido de fato: o Olist **não traz comissão nem tarifas** no pedido; fulfillment se identifica pelo depósito; o custo vem do cadastro do produto.
- Novas pendências do Felipe (lista viva em `../RETOMAR.md`): relatórios de Mercado Livre, Magalu e Amazon (`09-relatorios-marketplaces.md`), 3 SKUs sem custo, confirmar canais Casas Bahia e Fulfillment Shopee, trocar o token do Olist.
- Perguntas da planilha manual ainda sem resposta: ver `06-analise-planilha-manual.md`.
