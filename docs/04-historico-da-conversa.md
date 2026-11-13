# Histórico completo da conversa de planejamento (2026-11-09)

Registro cronológico do que foi dito e decidido, para retomar sem perder nada. As conclusões resumidas estão em `02-fase1-diagnostico.md`.

---

## 1. Início: briefing e primeira tarefa
O Felipe apresentou o briefing completo (ver `00-briefing-original.md`) e pediu **exclusivamente a Fase 1**: ler o contexto, organizar requisitos conhecidos, identificar dúvidas técnicas e financeiras e apresentar a primeira rodada de perguntas. Proibido criar planilhas, scripts ou integrações.

Antes de responder, foi lido o `OLIST_API.md` do repositório `jmsecom` (cópia em `05-referencias.md`) para não perguntar o que já se sabia: o Olist ERP é o Tiny, API v3, autenticação OAuth2, com pedidos, itens, produtos (incluindo custos), contas a receber, notas, intermediadores e depósitos.

## 2. Primeira resposta do Claude

### O que já se sabia
- Olist ERP = Tiny, API v3, OAuth2. Os endpoints de token ainda não tinham sido localizados.
- 5 marketplaces, 20 a 50 pedidos por dia, Lucro Presumido, fulfillment em Mercado Livre, Amazon e Magalu.

### Quatro pontos críticos apresentados
1. **Onde estão as tarifas reais por pedido.** O ERP provavelmente traz pedido e valor, mas não necessariamente comissão, tarifa fixa e repasse exatos de cada marketplace. É hipótese, só a Fase 2 confirma. Se for o caso, será preciso usar relatórios ou APIs financeiras de cada canal, e o projeto cresce. Sugestão: começar por 1 ou 2 canais.
2. **O Google Sheets talvez não deva ser a base de dados.** Cerca de 18 mil pedidos por ano, mais itens, mais histórico de alterações. Limite do Sheets de 10 milhões de células, cotas do Apps Script apertadas, auditoria e fotografia de custo difíceis. Inclinação: banco (a VPS da Vertex já tem Postgres) com o Sheets só como painel. Decisão na Fase 3.
3. **A fotografia do custo tem limite.** Se o Olist guarda só o custo atual do produto, o histórico não é recuperável. Pedidos importados depois de uma mudança de custo usariam o custo novo.
4. **No Lucro Presumido, PIS, COFINS, IRPJ e CSLL são apurados sobre a receita do período, não por pedido.** Por pedido só dá para ratear estimativas. O ICMS depende de operação, UF e substituição tributária. Tudo é estimativa gerencial a validar com o contador.

### Primeira rodada de perguntas (9, em 4 blocos)
- **A. Conta Olist:** (1) plano e liberação da API v3; (2) como os 5 marketplaces entram no Olist e se o fulfillment entra como pedido normal; (3) onde aparecem hoje comissão, tarifa e frete.
- **B. Escopo:** (4) quanto histórico e qual canal tem mais volume ou mais dor; (5) como o lucro é calculado hoje.
- **C. Custos:** (6) o custo no Olist é manual, médio ou último; frequência; kits; (7) embalagem e preparação são fixas por SKU ou variam por pedido.
- **D. Tributos e fulfillment:** (8) contador, vendas para fora de MT, alíquota fixa atual e o que ela cobre; (9) extratos de fulfillment mensais; envio aos centros por transportadora ou frete próprio.

## 3. Respostas do Felipe

### Aos pontos críticos
1. **Tarifas:** a ideia é fornecer relatórios diários para alimentar o sistema, ou conectar cada marketplace para entender cada pedido. Meses atrás contrataram o **Gestor Seller**, que recebia comissões por API, mas só em 1 ou 2 marketplaces. Já não o têm. Querem algo parecido, mais preciso e mais próximo da realidade deles, nos marketplaces em que já atuam.
2. **Base de dados:** pode ser Postgres, mas começa no Sheets por estar iniciando. Migração depois, com orientação do Claude.
3. **Fotografia do custo:** pediu para explicar melhor (explicação abaixo).
4. **Impostos:** propôs montar uma estrutura de estimativa por pedido para validar com o contador depois, e pediu opinião sincera e outra sugestão. O contador ajuda por WhatsApp e faz algumas apurações, mas ele **não quer deixar a precificação na mão do contador**.

### Às perguntas
1. Plano **Domine**. Não sabe se a API v3 está liberada; pediu para averiguar.
2. Pedidos entram de forma nativa (integração Olist-marketplace), inclusive os do Full.
3. Comissão, tarifa e frete que aparecem no Olist **não são confiáveis, estão sempre defasados**, parece estimativa. Quer puxar direto do marketplace, ou alimentar manualmente com o relatório do próprio marketplace.
4. Quer começar do zero, mas importar **pelo menos 7 dias** de histórico para testar. Acredita que Amazon e Mercado Livre vendem mais, sem certeza.
5. **Não existe cálculo de lucro hoje.** Nas palavras dele: a empresa cresceu sem direção, faturando e achando que ganhava dinheiro, e agora não está dando conta de pagar as contas.
6. O custo no Olist varia mensalmente, é atualizado todo mês, então equivale a custo médio. Há kits.
7. Embalagem e preparação não são consideradas hoje. Precisam ser formalizadas.
8. Existem regras cadastradas no Olist; o Claude deveria averiguar o que está sendo praticado.
9. Existem extratos dos marketplaces de fulfillment, mas são manuais. Talvez haja API; averiguar. O envio aos centros de distribuição é feito por terceirizados e **esse gasto não é contabilizado** na carga de produtos enviados.

## 4. Segunda resposta do Claude

### Priorização
Com a empresa sem conseguir pagar as contas, a prioridade é responder rápido onde o dinheiro é perdido. Proposta em duas etapas:
- **Etapa 1:** pedidos do Olist de 7 dias mais relatórios de Mercado Livre e Amazon baixados à mão. Lucro por pedido e por SKU com imposto estimado.
- **Etapa 2:** automação, APIs dos marketplaces e conciliação.

### Respostas aos pontos críticos
1. **Relatórios ou API:** os dois, com o mesmo modelo de dados. Cada registro financeiro guarda a fonte (API ou relatório). O que o Gestor Seller fazia em 1 ou 2 canais, tenta-se cobrir nos 5. A viabilidade de cada API só se confirma na Fase 2.
2. **Sheets agora, Postgres depois:** concordância. Para migrar fácil: lógica em script e não em fórmulas, dados em abas simples, ID por pedido e por item.
3. **Fotografia do custo, explicada:**
   - O SKU X custa R$ 100 no Olist em outubro. Em novembro é atualizado para R$ 120.
   - Se o lucro de um pedido de outubro for recalculado em novembro lendo o cadastro, passa a usar R$ 120 e o lucro "muda sozinho".
   - Solução: copiar o custo para a linha do pedido no momento da importação e nunca mais reler.
   - Como o custo é atualizado todo mês, a fotografia funciona para a frente. Para pedidos antigos, o Olist só tem o custo de hoje, então o retroativo é aproximado.
4. **Impostos:** a ideia do Felipe está certa, com um ajuste. O contador valida as regras **uma vez** e o sistema calcula depois, em vez de o contador opinar pedido a pedido por WhatsApp. Três camadas:
   - **ICMS:** pode vir da nota fiscal que o Olist já emite (a verificar na Fase 2), por ser imposto da operação.
   - **PIS, COFINS, IRPJ e CSLL:** percentual sobre a receita. Pela regra geral do comércio no Lucro Presumido, em torno de 6% de tributos federais; o contador precisa confirmar os valores exatos.
   - **Calibração mensal:** ao fechar o mês, o contador informa o total apurado de cada imposto. O sistema compara com a estimativa e ajusta a alíquota efetiva.
   - Assim a precificação fica com o Felipe, e o contador só confere parâmetros e fechamento.

### Respostas às perguntas
- **API v3:** não é possível ver a conta dele. Pela pesquisa, a API v3 está nos planos pagos a partir do Construa, e o Domine tem o maior limite (120 requisições por minuto, suficiente para 50 pedidos por dia). Ressalva: as fontes divergem (blogs independentes e a central de ajuda), nomes e preços de plano mudaram ao longo do tempo. **Confirmar em Configurações, em "Aplicativos API V3".** Detalhes em `05-referencias.md`.
- **Dados do Olist não confiáveis:** o Olist entra só como fonte de pedido, itens, SKU, custo e nota. Comissão, tarifa e repasse virão do marketplace.
- **Fulfillment e frete aos centros:** metodologia de rateio por lote na Fase 4. Como esse frete hoje não entra no custo, todo lucro de produto enviado ao fulfillment está superestimado.

### Pedidos para a próxima rodada
1. Prints das regras de tributação e da natureza de operação no Olist, e um pedido de kit.
2. Um relatório de cobranças do Mercado Livre e outro da Amazon, sem dados pessoais de clientes.
3. Se ele tem acesso de administrador às contas de cada marketplace, que permite criar credenciais de API.

## 5. Repositório

- O Felipe criou `felipevertex/precificacaojms` e pediu para salvar o básico e alguns markdown para recomeçar de casa.
- Foram criados `README.md`, `CLAUDE.md`, `.gitignore` e `docs/00` a `03`. O `CLAUDE.md` registra a regra de não programar antes da aprovação e as preferências de trabalho.
- O primeiro push foi negado (403): a conta `zaffalor` só tinha leitura. O Felipe liberou o acesso e o push foi feito.
- Em seguida pediu para salvar tudo com detalhes completos, o que gerou este arquivo e o `05-referencias.md`.

## 6. Observações a não esquecer
- O Felipe quer um sistema confiável e econômico, sem intervenção manual constante, e quer **aprender** o n8n se ele trouxer vantagem real (avaliar, não impor).
- Frases-chave dele: "a precisão financeira é mais importante do que a aparência"; "seja crítico, não concorde automaticamente".
- O frete de envio aos centros de distribuição e o custo de embalagem hoje não entram em lugar nenhum. Isso é parte do motivo de o lucro real estar abaixo do que ele imagina.
- A Fase 2 deve começar pelo que o Felipe trouxer de casa (relatórios, prints do Olist) e pela confirmação do acesso à API v3.

## 7. Continuação
A sessão seguinte (2026-11-13: token, leitura do Olist, planilha, importação automática, relatórios dos marketplaces) está em `08-sessao-2-etapa1.md`. Resumo e lembretes para retomar: `../RETOMAR.md`.
