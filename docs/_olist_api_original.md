# Olist ERP (Tiny) — API v3

> Referência rápida da API pública do Olist ERP (antigo Tiny) para consulta durante o desenvolvimento.
> Documentação completa: https://api-docs.erp.olist.com
> Swagger: https://erp.tiny.com.br/public-api/v3/swagger/index.html

## Autenticação

- **Tipo**: Bearer Token (OAuth2)
- **Base URL**: `https://api.tiny.com.br/public-api/v3`
- Todos os endpoints exigem header `Authorization: Bearer {access_token}`
- Fluxo OAuth2 provavelmente similar ao do Mercado Livre/Bling — precisa de `client_id`, `client_secret`, `redirect_uri`, e endpoint de autorização + troca de código por token.
- **Próximo passo**: localizar o endpoint exato de autorização/token OAuth2 do Olist ERP (não está no swagger.json, que documenta só os endpoints de dados — ver docs completas em api-docs.erp.olist.com).

## Categorias disponíveis (27 tags)

| Categoria | Principais operações |
|---|---|
| **Produtos** | Criar/editar/excluir produto, variações, preço, kit, tags, anexos/imagens, custos |
| **Categorias** | CRUD de categorias de produto, listar árvore de categorias |
| **Estoque** | Obter/atualizar estoque de um produto, logs de movimentação |
| **Depósitos** | Listar depósitos de estoque |
| **Pedidos** | CRUD de pedidos, situação, itens, marcadores, gerar nota fiscal, lançar/estornar contas e estoque, despacho (rastreio) |
| **Notas** | Emitir/cancelar nota fiscal, incluir por XML, lançar/estornar contas e estoque, despacho, obter XML/link |
| **Orçamentos** | CRUD de propostas comerciais, gerar venda a partir de orçamento |
| **Ordem de Compra** | CRUD, situação, lançar contas/estoque |
| **Ordem de Serviço** | CRUD, situação, gerar nota fiscal, lançar contas/estoque |
| **Contas a pagar / Contas a receber** | CRUD, marcadores, baixar conta, listar recebimentos |
| **Contatos** | CRUD de contatos e pessoas de contato, status CRM, tipos |
| **CRM** | Assuntos, ações, anotações, estágios, marcadores (funil de vendas) |
| **Expedição / Separação** | Agrupamentos de expedição, etiquetas, situação de separação |
| **Serviços** | CRUD de serviços, transformar serviço em produto |
| **Marcas** | CRUD de marcas |
| **Tags de Produtos / Grupos de Tags** | Criar/listar tags |
| **Lista de Preços** | CRUD de listas de preço, associar/remover produtos |
| **Logistica (Formas de envio)** | Listar formas de envio |
| **Formas de pagamento / recebimento** | Listar formas de pagamento e recebimento |
| **Intermediadores** | Listar intermediadores (marketplaces conectados) |
| **Vendedores / Usuários** | Listar vendedores e usuários da conta |
| **Dados da empresa** | Obter informações da conta |
| **Categorias de receita e despesa** | Listar categorias financeiras |

## Casos de uso relevantes pro JMSECOM

- **Sincronizar estoque**: `GET/POST /estoque/{idProduto}` — mesma lógica que já fazemos com Bling
- **Puxar pedidos**: `GET /pedidos` — poderia alimentar o agente Aero (rastreamento) via `despacho`
- **Cadastro de produtos**: `POST /produtos` — usar no futuro agente Cadastrador junto com Bling
- **Notas fiscais**: `GET /notas`, `POST /notas/{idNota}/emitir` — automatizar emissão/consulta de NF
- **Rastreio**: `PUT /pedidos/{idPedido}/despacho` e `PUT /notas/{idNota}/despacho` — atualizar código de rastreio direto no Olist

## Status da integração

- ✅ Placeholder da conexão Olist ERP criado na sidebar (`app.py`) — estrutura OAuth2 (client_id/secret/redirect) seguindo padrão do Bling
- ✅ Script `setup_ml_oauth.py` criado (fluxo OAuth2 PKCE do Mercado Livre — usado como teste/base, já que Olist ERP e ML têm ecossistemas relacionados)
- ⏳ Fluxo de autorização OAuth2 do Olist ERP em si ainda não implementado
- ⏳ Endpoints de token/autorização do Olist ERP ainda não localizados (não estão no swagger.json — checar api-docs.erp.olist.com)

---
**Última atualização**: 2026-08-12
