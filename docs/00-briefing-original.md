# Briefing original do projeto

> Texto como o Felipe escreveu em 2026-11-09, preservado integralmente. É a fonte de verdade dos requisitos. Resumo em `01-requisitos-resumo.md`.

# PROJETO: SISTEMA DE GESTÃO DE RENTABILIDADE E CONTROLE FINANCEIRO PARA ECOMMERCE

Quero desenvolver um sistema de gestão financeira e apuração de rentabilidade por pedido, utilizando Google Sheets como interface principal, integrado ao meu ERP Olist por meio de API.

O projeto deverá ser planejado cuidadosamente antes de qualquer implementação. Quero que você atue como um arquiteto de soluções, analista de negócios, especialista em Google Sheets, Google Apps Script, APIs, n8n e gestão financeira de operações de ecommerce.

**IMPORTANTE: NÃO COMECE A PROGRAMAR, CRIAR PLANILHAS OU IMPLEMENTAR INTEGRAÇÕES NESTA PRIMEIRA ETAPA.** Primeiro, precisamos estudar a operação, definir os requisitos, projetar a arquitetura, validar os cálculos e aprovar todo o planejamento.

## 1. CONTEXTO DA MINHA OPERAÇÃO

Trabalho com ecommerce e comercializo produtos em diferentes marketplaces.

Atualmente, utilizo os seguintes canais de venda:

* Mercado Livre.
* Shopee.
* Amazon.
* Magalu.
* KaBuM!

Possuo apenas uma conta em cada marketplace.

Meu ERP centralizador é o Olist, que recebe e gerencia todos os pedidos, inclusive aqueles processados pelos serviços de fulfillment dos marketplaces.

O Olist é atualmente minha principal fonte de dados operacionais e financeiros.

Meu volume habitual é de aproximadamente 20 a 50 pedidos por dia, podendo ultrapassar essa quantidade em determinados períodos.

Tenho experiência anterior com integração de APIs, inclusive já desenvolvi integrações entre sistemas utilizando o Bling. Portanto, não tenho problema em trabalhar com APIs, autenticação, scripts, webhooks e ferramentas de automação.

Minha preferência tecnológica é:

* Google Sheets: interface principal e visualização dos dados.
* Google Apps Script: processamento e automações.
* API do Olist: extração e atualização dos dados.
* n8n: tecnologia complementar que desejo avaliar e, se fizer sentido, utilizar na arquitetura.

Não quero utilizar o n8n obrigatoriamente. Quero que você avalie tecnicamente se ele agrega vantagens reais ao projeto.

## 2. OBJETIVO PRINCIPAL

Quero saber exatamente quanto lucro ou prejuízo minha empresa obteve em cada pedido realizado nos marketplaces.

A planilha deverá apresentar todos os componentes financeiros envolvidos na venda, sem esconder despesas dentro de cálculos genéricos.

Preciso visualizar individualmente:

* Valor bruto da venda.
* Descontos concedidos.
* Comissão do marketplace.
* Tarifas fixas.
* Outras tarifas cobradas pelo marketplace.
* Frete pago pelo vendedor.
* Custos relacionados ao fulfillment.
* Impostos.
* Custo de aquisição dos produtos.
* Custos adicionais de preparação e embalagem.
* Custos indiretos.
* Outros ajustes financeiros.
* Valor líquido recebido.
* Lucro ou prejuízo efetivo.
* Margem de lucro percentual.

O objetivo é que cada venda seja registrada e processada automaticamente, sem precisar preencher manualmente as informações financeiras.

Quero abrir a planilha ao final do dia e conseguir identificar imediatamente:

1. Quanto vendi?
2. Quanto gastei?
3. Quanto paguei aos marketplaces?
4. Quanto paguei em impostos?
5. Quanto custaram os produtos vendidos?
6. Quanto gastei com fulfillment?
7. Quanto efetivamente recebi?
8. Quanto foi meu lucro líquido?
9. Quais pedidos deram prejuízo?
10. Qual marketplace apresentou a melhor rentabilidade?

A precisão financeira é mais importante do que a aparência visual.

## 3. INTEGRAÇÃO COM O OLIST

A integração deverá utilizar a API oficial do Olist.

Quero que você estude a documentação oficial da API antes de propor a arquitetura definitiva.

Investigue:

* Autenticação.
* Endpoints disponíveis.
* Consulta de pedidos.
* Consulta de itens dos pedidos.
* Dados financeiros.
* Informações de comissão e tarifas.
* Informações de frete.
* Dados de produtos e SKUs.
* Custos de aquisição cadastrados.
* Dados de faturamento.
* Dados de cancelamento.
* Dados de devolução.
* Informações de fulfillment.
* Possibilidade de consultar atualizações financeiras posteriores.
* Webhooks, caso disponíveis.
* Limites de requisições.
* Paginação.
* Estratégias de sincronização.

Não presuma que todos os dados necessários estão disponíveis na API.

Se algum dado não estiver disponível diretamente, identifique alternativas para obtê-lo, seja por meio de outras integrações, relatórios oficiais dos marketplaces ou lançamentos complementares controlados.

### Funcionamento desejado

1. Um cliente realiza uma compra em qualquer marketplace.
2. O Olist recebe o pedido.
3. A integração identifica o novo pedido.
4. Os dados são enviados automaticamente ao Google Sheets.
5. A planilha identifica o marketplace, pedido, produtos e quantidades.
6. Os custos e tarifas são associados ao pedido.
7. Os cálculos financeiros são realizados automaticamente.
8. O pedido aparece no dashboard e nas bases de dados.

A importação deverá acontecer assim que o pedido entrar no Olist.

Entretanto, não quero que os valores financeiros sejam considerados definitivos antes de estarem devidamente confirmados.

Quero que o sistema continue atualizando os pedidos conforme novas informações forem disponibilizadas.

### Requisitos técnicos obrigatórios

* Não permitir pedidos duplicados.
* Utilizar identificadores únicos.
* Permitir atualização de pedidos existentes.
* Registrar alterações financeiras posteriores.
* Ter controle da última sincronização.
* Permitir sincronização retroativa.
* Possuir mecanismo de recuperação de falhas.
* Registrar erros de integração.
* Possuir logs de execução.
* Respeitar os limites da API.
* Permitir reprocessamento de pedidos específicos.
* Proteger credenciais e tokens de autenticação.

Considere que pedidos cancelados, devolvidos ou reembolsados não podem continuar sendo contabilizados como vendas normais.

## 4. MODELO DE CUSTOS E FORMAÇÃO DO LUCRO

Essa é a parte mais importante do sistema.

Quero que você desenvolva uma estrutura financeira que permita identificar todos os custos envolvidos na comercialização de cada produto.

### 4.1. Custo de aquisição

Atualmente, o custo de aquisição dos produtos já está cadastrado no Olist.

Quero aproveitar essa informação para calcular automaticamente o custo dos produtos vendidos.

A integração deverá identificar o SKU e buscar o custo correspondente.

Investigue como o Olist disponibiliza esse dado e como podemos garantir que o custo utilizado corresponda ao custo vigente na data da venda.

Importante: o custo de aquisição utilizado em um pedido deverá ser preservado como fotografia histórica. Uma alteração posterior no cadastro do produto não poderá modificar retroativamente o lucro de pedidos antigos.

### 4.2. Custos adicionais dos produtos

Quero criar uma base complementar de custos por SKU.

Essa base deverá permitir cadastrar:

* Embalagem.
* Caixa.
* Plástico bolha.
* Fitas adesivas.
* Etiquetas.
* Materiais de proteção.
* Mão de obra de separação.
* Preparação do produto.
* Outros custos específicos.

Quero que esses valores sejam associados automaticamente aos pedidos conforme os SKUs vendidos.

Também quero a possibilidade de estabelecer custos fixos ou variáveis e, quando necessário, utilizar critérios de rateio.

Não quero que esses custos sejam ignorados apenas porque não estão cadastrados no Olist.

### 4.3. Custos operacionais indiretos

Avalie a possibilidade de criar uma base para despesas operacionais que não podem ser diretamente associadas a um SKU.

Exemplos:

* Custos administrativos.
* Operação de estoque.
* Materiais gerais.
* Despesas operacionais relacionadas à expedição.
* Outros custos indiretos.

Proponha critérios de rateio coerentes, como valor por pedido, quantidade de itens, volume ou outro direcionador justificável.

Esses custos deverão aparecer separadamente dos custos diretamente associados aos produtos.

Não misture custos diretos e indiretos sem identificação.

## 5. FULFILLMENT DOS MARKETPLACES

Utilizo fulfillment nos seguintes marketplaces:

* Mercado Livre.
* Amazon.
* Magalu.

Quero que o sistema tenha capacidade de identificar pedidos enviados por fulfillment e contabilizar todos os custos específicos dessa modalidade.

Não quero considerar apenas a comissão convencional.

Investigue a possibilidade de identificar e controlar:

* Tarifas de armazenagem.
* Taxas de manuseio.
* Taxas de preparação.
* Custos de expedição.
* Custos de envio dos produtos até os centros de distribuição.
* Custos de transferência e movimentação.
* Taxas por estoque parado.
* Cobranças por devolução.
* Custos de retirada de estoque.
* Outras cobranças específicas de cada programa de fulfillment.

Também quero considerar os custos para enviar mercadorias aos centros de distribuição.

Por exemplo: quando envio um lote de produtos para o fulfillment, existem despesas de transporte e preparação que precisam ser incorporadas ao custo dos produtos enviados.

Proponha uma metodologia para distribuir esses custos entre os SKUs e unidades daquele lote, mantendo rastreabilidade.

Importante: não invente tarifas nem utilize percentuais genéricos quando for possível obter os valores reais.

Cada marketplace possui regras próprias. A arquitetura deverá permitir cadastrar regras diferentes por canal e modalidade logística.

## 6. TRIBUTAÇÃO: LUCRO PRESUMIDO

Minha empresa trabalha no regime de Lucro Presumido.

Atualmente utilizo uma alíquota fixa para estimar os impostos, mas quero tornar esse cálculo mais preciso.

Desejo trabalhar com dois modelos complementares:

**Modelo A: Apuração detalhada.** Separar os tributos aplicáveis, considerando as particularidades da operação:

* PIS.
* COFINS.
* IRPJ.
* CSLL.
* ICMS.
* Outros tributos aplicáveis, quando houver.

**Modelo B: Alíquota efetiva.** Permitir visualizar e utilizar uma alíquota efetiva configurável para estimativas e conferências.

Quero que você investigue como estruturar corretamente esse cálculo para uma empresa no Lucro Presumido.

Considere que a tributação pode depender de fatores como:

* Classificação fiscal dos produtos.
* NCM.
* Origem e destino da operação.
* ICMS e eventuais benefícios fiscais.
* Substituição tributária.
* Diferenciais tributários aplicáveis.
* Natureza da operação.
* Receita tributável.
* Particularidades da legislação vigente.

Não assuma que todos os tributos podem ser simplesmente calculados como um percentual sobre cada pedido.

Diferencie impostos diretamente atribuíveis à venda de tributos apurados sobre a receita da empresa em determinado período.

A planilha deverá permitir configurar regras tributárias e manter histórico de alterações.

Não invente regras fiscais. Identifique as informações necessárias, apresente as premissas e indique quais cálculos deverão ser validados pelo contador responsável.

Quero que o sistema consiga estimar o custo tributário por pedido sem confundir estimativa gerencial com apuração fiscal oficial.

## 7. COMISSÕES E TARIFAS DOS MARKETPLACES

Quero trabalhar prioritariamente com os valores efetivamente cobrados pelos marketplaces.

Cada canal possui suas próprias políticas de cobrança.

O sistema deverá identificar, sempre que possível:

* Comissão percentual.
* Tarifa fixa por venda.
* Tarifas por faixa de preço.
* Tarifas específicas por categoria.
* Custos de frete.
* Descontos e subsídios.
* Taxas de fulfillment.
* Outras cobranças.
* Estornos e ajustes.

Não quero que a planilha aplique uma comissão genérica de 12%, 15% ou qualquer outro percentual quando o marketplace disponibilizar o valor efetivamente cobrado.

Os valores reais devem prevalecer sobre as estimativas.

Quando a informação não estiver disponível no momento da importação, o pedido deverá receber um status indicando que existe uma informação financeira pendente.

Quero também uma área de parametrização das regras de cada marketplace para conferência e simulação.

## 8. CONCILIAÇÃO FINANCEIRA

Quero que o projeto contemple dois controles diferentes:

**A. Rentabilidade econômica da venda.** Deverá demonstrar o resultado econômico do pedido, considerando: receita, descontos, comissão, frete, impostos estimados ou apurados, custo dos produtos, custos adicionais, custos indiretos, fulfillment e demais despesas. Resultado: lucro ou prejuízo e margem de contribuição/lucro, com definições claras.

**B. Conciliação financeira.** Deverá demonstrar o que efetivamente aconteceu financeiramente com o pedido. Quero comparar: valor bruto da venda, descontos, deduções do marketplace, valores efetivamente repassados, ajustes posteriores, estornos, reembolsos, diferenças entre valores previstos e realizados.

O sistema deverá identificar divergências entre o resultado esperado e os valores efetivamente cobrados ou repassados.

Quero uma classificação visual para: Conciliado, Pendente, Divergente, Parcialmente conciliado, Cancelado, Reembolsado.

Investigue quais dados o Olist fornece e quais relatórios ou integrações adicionais dos marketplaces serão necessários.

Não confunda valor líquido de repasse com lucro líquido. São informações diferentes.

## 9. ESTRUTURA DE ABAS DO GOOGLE SHEETS

Proponha uma estrutura organizada, intuitiva e escalável. Como ponto de partida, considere as seguintes abas:

* **01 DASHBOARD:** painel gerencial (faturamento bruto, descontos, comissões, fretes, impostos, CMV, custos adicionais, fulfillment, indiretos, lucro líquido, margem líquida, quantidade de pedidos, ticket médio, pedidos com prejuízo). Filtros por período, marketplace, SKU, produto, modalidade logística e status do pedido. Gráficos e indicadores visuais.
* **02 PEDIDOS:** uma linha consolidada por pedido (identificação, receita, despesas totais, repasse e resultado).
* **03 ITENS DOS PEDIDOS:** uma linha por SKU vendido, vinculada ao pedido. Permite rentabilidade por produto.
* **04 PRODUTOS E CUSTOS:** cadastro complementar de custos por SKU (aquisição, embalagem, preparação, demais).
* **05 TAXAS E MARKETPLACES:** regras e tarifas de cada canal, com histórico e validade.
* **06 IMPOSTOS:** parametrização de tributos, alíquotas, regras e critérios.
* **07 FULFILLMENT:** armazenagem, movimentação, preparação, envio aos centros de distribuição e demais despesas.
* **08 CONCILIAÇÃO:** comparação entre valores calculados e valores cobrados e recebidos.
* **09 CUSTOS INDIRETOS:** cadastro e rateio das despesas operacionais.
* **10 LOGS E SINCRONIZAÇÃO:** importações, atualizações, erros, reprocessamentos, última execução.
* **11 CONFIGURAÇÕES:** parâmetros gerais, conexões, períodos, regras de sincronização.

Essa estrutura é uma sugestão inicial. Avaliar se todas são necessárias, se alguma pode ser consolidada ou se outras precisam ser adicionadas. Não criar abas apenas por criar. Priorizar organização, desempenho e facilidade de utilização.

## 10. DASHBOARD GERENCIAL

Painel limpo, profissional e de leitura rápida. Desempenho diário, semanal e mensal.

Indicadores: faturamento bruto, lucro líquido, margem líquida, total de impostos, comissões, fretes, custo de aquisição, custos operacionais, gastos com fulfillment, ticket médio, número de pedidos, pedidos com prejuízo.

Comparações entre marketplaces: quem vende mais, quem tem maior margem, quem cobra mais comissões, quem tem maior custo logístico, maior lucro absoluto, mais pedidos deficitários. Gráficos de evolução diária e mensal.

Cores com significados consistentes: verde = resultado positivo; vermelho = prejuízo ou divergência; amarelo = pendência ou atenção; azul = informação operacional; cinza = neutro.

Formatação condicional para margem baixa, prejuízo, tarifas inesperadas ou informações incompletas. O dashboard deve permitir filtrar sem comprometer as bases de dados.

## 11. AUTOMAÇÃO: GOOGLE APPS SCRIPT E N8N

Comparar três arquiteturas:

1. API Olist + Google Apps Script + Google Sheets.
2. API Olist + n8n + Google Sheets.
3. API Olist + n8n + Google Apps Script + Google Sheets.

Para cada uma, avaliar: facilidade de implementação, custo de operação, limites técnicos, desempenho, escalabilidade, facilidade de manutenção, segurança, tratamento de falhas, frequência de sincronização, complexidade para adicionar novos marketplaces.

Considerar o volume de 20 a 50 pedidos diários, com possibilidade de crescimento. Preferência: solução confiável, econômica e sem intervenções manuais constantes. Se o n8n oferecer vantagens concretas, o Felipe quer aprender a usá-lo no projeto. Apresentar a arquitetura recomendada e justificar tecnicamente.

## 12. REGRAS DE INTEGRIDADE E CONFIABILIDADE (obrigatórias)

1. Nenhum pedido poderá ser importado duas vezes.
2. Atualizações posteriores deverão modificar os registros existentes.
3. Pedidos antigos não poderão ter seu histórico de custos alterado indevidamente.
4. Custos históricos deverão ser preservados.
5. Alterações financeiras deverão possuir rastreabilidade.
6. Pedidos cancelados e devolvidos deverão receber tratamento específico.
7. Reembolsos parciais deverão ser tratados corretamente.
8. Pedidos com múltiplos SKUs deverão ter seus custos discriminados.
9. Informações financeiras ausentes não poderão ser tratadas como zero sem identificação.
10. Falhas de integração deverão ser registradas.
11. Deverá existir possibilidade de reprocessamento.
12. A sincronização não poderá comprometer os registros já consolidados.
13. Credenciais e tokens nunca deverão ficar expostos em células públicas da planilha.
14. O sistema deverá permitir auditoria dos cálculos.

Propor mecanismos de backup, proteção das abas, controle de acesso e recuperação de dados.

## 13. TRATAMENTO DE EXCEÇÕES

Definir regra documentada para cada situação: pedido com vários produtos; quantidades diferentes do mesmo SKU; cancelamento antes da expedição; cancelamento após a expedição; devolução total; devolução parcial; reembolso parcial; alteração de comissão; ajuste posterior de frete; subsídio do marketplace; cupom de desconto; desconto financiado pelo vendedor; desconto financiado pelo marketplace; pedido por fulfillment; custo de aquisição ausente; SKU sem cadastro complementar de despesas; divergência entre Olist e marketplace; falha na importação; reprocessamento de pedidos antigos.

## 14. ETAPAS OBRIGATÓRIAS DO PROJETO (não pular etapas)

* **FASE 1: Diagnóstico e levantamento de requisitos.** Investigar a conta Olist, disponibilidade dos dados financeiros, particularidades dos marketplaces, fulfillment, estrutura tributária, critérios de rateio e necessidades de conciliação. Perguntas objetivas, em pequenos blocos, sem repetir as já respondidas.
* **FASE 2: Pesquisa técnica e viabilidade.** Consultar a documentação oficial; matriz com informação desejada, fonte, endpoint ou método, disponibilidade confirmada, limitações e alternativa. Não inventar endpoints, parâmetros ou funcionalidades. Avaliar também as APIs dos marketplaces.
* **FASE 3: Arquitetura do sistema.** Fluxo de dados, integrações, estrutura das abas, responsabilidades, armazenamento, sincronização, duplicidades, atualizações, recuperação de falhas. Avaliar se o Sheets basta como base principal ou se convém um banco complementar (com motivo e custos).
* **FASE 4: Modelagem financeira.** Dicionário de dados completo (nome, origem, tipo, fórmula, regra de preenchimento, possibilidade de atualização, critério de validação) e exemplos numéricos de pedidos demonstrando cada custo. Validar cálculos antes da implementação.
* **FASE 5: Projeto visual.** Nomes e ordem das abas, cabeçalhos, colunas, cores, indicadores, dashboard, filtros, formatação condicional.
* **FASE 6: Plano de implementação.** Tarefas menores, ordem, dependências, testes e critérios de aceitação.
* **FASE 7: Aprovação.** Apresentar: documento de requisitos, arquitetura recomendada, estrutura da planilha, modelo financeiro, estratégia de integração, plano de implementação, riscos e limitações. **Somente iniciar a implementação após aprovação explícita.**

## 15. DIRETRIZES DE TRABALHO

* Ser crítico e técnico; não concordar automaticamente.
* Não simplificar cálculos financeiros importantes só para facilitar a implementação.
* Não usar dados estimados quando for possível obter os reais.
* Quando uma informação não estiver disponível, deixar explícito e propor alternativa.
* Priorizar precisão financeira, integridade histórica e confiabilidade das integrações.
* Evitar fórmulas excessivamente complexas no Sheets quando for mais eficiente processar por Apps Script ou n8n.
* Considerar falhas, alterações, cancelamentos, devoluções, reembolsos e crescimento, não só o cenário ideal.
* Documentar regras de negócio e cálculos de modo que o Felipe consiga entender e manter o sistema.
* Em decisão técnica importante: alternativas, vantagens, desvantagens e recomendação.

## Objetivo final

Um sistema confiável no qual cada pedido realizado nos marketplaces seja automaticamente registrado, tenha todos os seus custos discriminados e apresente, com clareza, o lucro ou prejuízo real daquela operação.
