# Sessão 2 (2026-11-13): da leitura do Olist à planilha com importação automática

Diário cronológico. A sessão 1 (planejamento, 2026-11-09) está em `04-historico-da-conversa.md`. Resumo operacional em `../RETOMAR.md`.

## 1. Repositório e roadmap
- O Felipe criou `felipevertex/precificacaojms`; o primeiro push foi negado (403) até ele dar escrita à conta `zaffalor`. Depois disso o push funcionou.
- Pediu o ROADMAP em formato visual. Há versão em Markdown (`../ROADMAP.md`) e uma versão visual privada, na conta dele: https://claude.ai/artifact/LVifwWVvkMQBGVT1PYDDTE. **O Markdown é a fonte de verdade**; o visual pode estar desatualizado.

## 2. Token do Olist e leitura dos pedidos
- O Felipe mandou um print e o token da API do Olist. Decisões: o token fica **só local** (`.env`, ignorado pelo Git) e, depois, também na VPS. Ficou registrado que o token apareceu no chat e **deve ser trocado**.
- Aprovou usar a API para ler os últimos 7 dias. Foi usada a **API 2.0 do Olist (Tiny)**, que o token libera; a v3 (OAuth2) continua sem confirmação de acesso.
- Endpoints usados (POST com `token` e `formato=json`): `pedidos.pesquisa.php`, `pedido.obter.php`, `produto.obter.php`. A listagem já traz a situação do pedido.
- Somente leitura. Não se guarda nome, CPF, endereço, e-mail ou telefone de clientes.
- Constatações sobre os dados do Olist:
  - o pedido **não traz comissão nem tarifas** (o `valor_frete` é o que o cliente pagou, `outras_despesas` vem zerado);
  - **fulfillment** identifica-se pelo campo `deposito`;
  - o custo vem de `produto.obter.php` (`preco_custo_medio`, `preco_custo`); kits (`classe_produto = K`) trazem componentes;
  - NCM e origem vêm do produto. O **ICMS** ainda não foi verificado (exige o XML da nota).
- Limite de chamadas: pausa de ~2,3 s por chamada e espera de 70 s ao receber "Excedido/Bloqueada".

## 3. Primeiros números (07 a 13/11/2026)
- 282 pedidos: 262 no resultado e 20 cancelados. 283 itens, 88 produtos (6 kits).
- Receita dos pedidos no resultado: R$ 50.634,65. Ticket médio R$ 193,26.
- Custo do produto lido para 258 dos 262 pedidos.
- Receita menos custo do produto, antes das tarifas: média 28,8%. Por canal, de **19,0% (Magalu)** a **34,6% (Amazon FBA)**.
- Um pedido do Magalu foi vendido por R$ 202,95 com custo de R$ 350,70.
- **3 SKUs com custo médio zerado no Olist:** `23-DLXL-TSPF`, `923`, `L1-O349-LQJ6`.
- Canais fora da lista original: **Casas Bahia Marketplace** e **Fulfillment Shopee** (este aparece como depósito). A Amazon tem duas integrações: DBA (estoque próprio) e FBA Classic (fulfillment).

## 4. Análise da planilha manual
Ver `06-analise-planilha-manual.md`. Em resumo: devoluções ainda contam como lucro, frete pago vazio vira ganho, embalagem e indiretos não entram em lugar nenhum, tarifa em campo único, um custo por pedido e imposto fixo de 2,5%.

## 5. Estrutura da planilha (pedido do Felipe)
Pedido dele: estruturar a planilha mostrando de onde vem cada informação (Olist, marketplaces, XML etc.), com visual dos pedidos já importados, e foco em **precificação assertiva**. Aprovou explicitamente construir ("pode começar e faça o que der pra fazer até agora"). Resultado em `07-planilha-etapa1.md`:
- 10 abas: LEIA-ME, Dashboard, Pedidos, Itens, Produtos e Custos, Lançamentos, Fulfillment (lotes), Custos indiretos, Parâmetros, Logs.
- Colunas agrupadas por origem com cor: Olist (azul), XML (verde-água), custos próprios (cinza), marketplace (amarelo), calculado (verde).
- Valores: `pendente` (amarelo, nunca zero), `n/a`, e situação do dado Completo/Incompleto/Fora do resultado.
- Lucro = Receita − soma dos custos (O a V) − reembolsos, só quando Dado = Completo.
- Custo congelado: custo médio do Olist copiado para a aba Itens na leitura. Kit = soma dos componentes.

## 6. Acesso ao Google Sheets
- O Felipe pediu um e-mail para compartilhar a planilha. Foi usada a **conta de serviço do Google que já existe no jmsecom** (a chave fica só na VPS).
- A planilha foi criada por ele limpa, compartilhada com a conta de serviço, e o ID foi gravado em `SHEET_ID_ANALISE_PEDIDOS` no `.env`.
- Por isso a montagem roda **na VPS**: o token do Olist fica na máquina local, a chave do Google fica na VPS. A leitura do Olist (local) gerou `dados/olist_pedidos.json`, que foi enviado à VPS para a montagem.

## 7. Problemas encontrados e como foram resolvidos
| Problema | Solução |
|---|---|
| Cola de várias linhas falhou no console do Windows | Comandos em uma linha só, botão direito para colar |
| Heredoc quebrado no bash | Arquivos criados pela ferramenta de escrita |
| Cota de leitura do Sheets estourada (429) | Ler metadados uma vez; evitar leituras repetidas; esperar entre execuções |
| Erro 400 ao congelar colunas | Havia células mescladas atravessando a divisão; mesclagens removidas |
| `#ERROR!` em todas as fórmulas | Locale pt_BR exige `;`; `sheets_util.py` converte `,` em `;` |
| Quantidade aparecia como "1," | Formato de número "0" |
| Risco de estourar a grade | Todas as abas com 3000 linhas × 30 colunas |
| ICMS pendente travaria todos os lucros | Coluna ICMS fora da contagem de situação do dado (por enquanto) |
| `sleep` encadeado bloqueado | Espera em segundo plano |

## 8. Importação incremental
Pergunta do Felipe: de quanto em quanto tempo a importação roda? Foram oferecidas duas rotas (Apps Script ou script na VPS). Decisão dele: **"vamos sem o app scripts por enquanto, vamos usar o token"**, ou seja, script na VPS.
- `scripts/importar_pedidos.py` + módulos compartilhados `olist.py`, `regras.py`, `sheets_util.py`.
- A cada execução: lista os pedidos dos últimos 30 dias, acrescenta os novos dos últimos 7, atualiza situação, nota e datas dos que mudaram e escreve em Logs. Nunca apaga nem sobrescreve lançamentos, custos ou parâmetros.
- Testes na VPS: 1147 pedidos na janela de 30 dias, 0 novos, 0 alterados; depois um pedido (3538) foi apagado de propósito e reapareceu corretamente, com item, custo e fórmulas, 0 erros.
- Limitações: pedidos com mais de 30 dias não têm a situação atualizada; carga histórica maior precisa ser feita de propósito.

## 9. O cron
- A primeira tentativa de instalar o cron foi **bloqueada pela política de segurança da sessão** e não foi contornada. O Felipe respondeu "quero te autorizar". Depois dessa autorização, o cron foi instalado, com backup do crontab anterior. Detalhes e comandos: `10-operacao-vps.md`.
- O Felipe perguntou o que faltava de Mercado Livre e Amazon, e depois onde fica o Magalu. As respostas estão em `09-relatorios-marketplaces.md`. A sugestão final foi trazer **ML e Magalu juntos**.

## 10. Decisões da sessão
| Tema | Decisão |
|---|---|
| Ordem de trabalho | Construir a Etapa 1 agora, com autorização explícita |
| Fonte do pedido | API 2.0 do Olist (token), somente leitura |
| Onde roda | Script na VPS por cron, sem Apps Script |
| Interface | Google Sheets, planilha "Análise de Pedidos" |
| Dado ausente | `pendente`, nunca zero |
| Primeiros relatórios | Mercado Livre e Magalu (Amazon logo depois) |

## 11. Em aberto
Ver a lista completa em `../RETOMAR.md`. Resumo: relatórios dos marketplaces, token do Olist a trocar, 3 SKUs sem custo, confirmação de canais, ICMS pelo XML, cadastros de embalagem/preparação, rateio do frete aos centros, custos indiretos, aba de preço mínimo.
