# Referências e fontes

## Olist ERP (Tiny), API v3

- Notas de levantamento feitas em agosto de 2026 no repositório `jmsecom`: cópia integral em [`_olist_api_original.md`](_olist_api_original.md). Lista as 27 categorias de endpoints (produtos com custos, pedidos, notas, contas a receber, intermediadores, depósitos, etc.).
- Base URL registrada: `https://api.tiny.com.br/public-api/v3`, com `Authorization: Bearer {access_token}` (OAuth2).
- **Lacuna conhecida:** os endpoints de autorização e de token OAuth2 **não** foram localizados naquele levantamento, pois não estão no swagger. Devem estar na documentação completa. Localizar na Fase 2.
- Documentação oficial indicada nas notas: https://api-docs.erp.olist.com e o Swagger em https://erp.tiny.com.br/public-api/v3/swagger/index.html

## Pesquisa de 2026-11-09: a API v3 vale para o plano Domine?

Resultado da busca, **não confirmado na conta do Felipe**:
- A API v3 está disponível nos planos pagos a partir do **Construa**; o plano **Avance** não inclui integração por API (tabela de blog independente).
- Limites por minuto (fonte de blog independente; a central de ajuda também cita que a v3 tem limite por plano): Construa 30, Impulsione 60, **Domine 120**.
- Nomes de plano atuais citados em guia de 16/10/2026: Avance, Construa, Impulsione, Domine, e Protagonize sob consulta. Os nomes "Crescer" e "Evoluir" aparecem em fontes mais antigas.
- As fontes não concordam totalmente e os planos mudaram com o tempo. **Verificar na conta ou no suporte da Olist** o acesso e o limite exato.

Links consultados:
- Aplicativos API V3, central de ajuda da Olist: https://ajuda.olist.io/hubs-e-plataformas-via-api/aplicativos-api-v3-configuracoes-e-utilizacao
- Planos ERP da Olist, blog da Olist: https://olist.com/blog/pt/olist/tiny-news/planos-tiny-erp/

## A pesquisar na Fase 2 (nada confirmado)
- Documentação oficial das APIs financeiras de Mercado Livre, Amazon (finanças), Shopee, Magalu e KaBuM.
- API ou extrato de fulfillment de Mercado Livre, Amazon e Magalu.
- Webhooks do Olist e política de limites e paginação.
- Se o XML da nota fiscal emitida pelo Olist traz o ICMS por item.

## Ferramentas em avaliação
- Google Sheets e Google Apps Script (interface e processamento). Atenção às cotas do Apps Script e ao limite de 10 milhões de células.
- n8n (avaliar vantagens reais, sem obrigatoriedade).
- Postgres (migração futura; já existe na VPS da Vertex).
