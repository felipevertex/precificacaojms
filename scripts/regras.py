"""Regras de negocio compartilhadas entre a montagem da planilha e a importacao incremental.

Qualquer mudanca de coluna ou formula de Pedidos/Itens deve ser feita AQUI, nunca duplicada.
"""


def modalidade(p):
    dep = (p.get("deposito") or "").upper()
    if "FULL" in dep:
        if "AMAZON" in dep:
            return "Fulfillment Amazon"
        if "MERCADO" in dep:
            return "Fulfillment Mercado Livre"
        if "MAGAZINE" in dep or "MAGALU" in dep:
            return "Fulfillment Magalu"
        return "Fulfillment (" + (p.get("deposito") or "").strip() + ")"
    if (p.get("forma_envio") or "") == "AMAZON_DBA":
        return "Estoque próprio · DBA"
    return "Estoque próprio"


def custo_do_produto(prod, produtos):
    """(custo medio unitario | None, observacao). None = pendente."""
    if prod is None:
        return None, "produto não encontrado no Olist"
    if prod["classe"] == "K":
        if not prod["kit"]:
            return None, "kit sem composição lida"
        total = 0.0
        for comp in prod["kit"]:
            c = produtos.get(comp["id_produto"])
            if not c or c["preco_custo_medio"] <= 0:
                return None, "componente do kit sem custo médio"
            total += c["preco_custo_medio"] * comp["quantidade"]
        return round(total, 2), "kit: soma dos componentes"
    if prod["preco_custo_medio"] > 0:
        return prod["preco_custo_medio"], ""
    return None, "custo médio zerado no Olist"


def chave_pedido(p):
    return p.get("numero_ecommerce") or f"OLIST-{p['numero']}"


def linha_item(p, it, produtos, n):
    """Linha da aba Itens (n = numero da linha na planilha)."""
    full = modalidade(p).startswith("Fulfillment")
    prod = produtos.get(it["id_produto"])
    custo, obs = custo_do_produto(prod, produtos)
    ult = prod["preco_custo"] if prod and prod["preco_custo"] > 0 else None
    return [
        p["chave"], p["numero"], it["sku"], it["descricao"], it["quantidade"], it["valor_unitario"], f"=E{n}*F{n}",
        custo if custo is not None else "pendente", ult if ult is not None else "",
        (prod or {}).get("consultado_em", ""), f'=IF(ISNUMBER(H{n}),H{n}*E{n},"pendente")',
        (f"=IF(ISNUMBER(VLOOKUP(C{n},'Produtos e Custos'!$A:$L,12,FALSE)),"
         f"VLOOKUP(C{n},'Produtos e Custos'!$A:$L,12,FALSE)*E{n},\"pendente\")"),
        "pendente" if full else "n/a", obs,
        "Kit" if prod and prod["classe"] == "K" else "Simples", (prod or {}).get("ncm", ""), (prod or {}).get("origem", ""),
    ]


def linha_produto(sku, prod, produtos, n):
    """Linha da aba Produtos e Custos."""
    custo, obs = custo_do_produto(prod, produtos)
    return [sku, (prod or {}).get("nome", ""), "Kit" if prod and prod["classe"] == "K" else "Simples",
            custo if custo is not None else "pendente", (prod or {}).get("preco_custo") or "", (prod or {}).get("consultado_em", ""),
            "", "", "", "", "", f'=IF(COUNT(G{n}:K{n})=0,"",SUM(G{n}:K{n}))',
            f'=IF(ISNUMBER(D{n}),D{n}+N(L{n}),"pendente")', (prod or {}).get("ncm", ""), (prod or {}).get("origem", ""),
            (prod or {}).get("categoria", ""), (prod or {}).get("peso_bruto", ""), obs]


def nf_emitida(p):
    return "Sim" if str(p.get("id_nota_fiscal") or "0") not in ("0", "") else "Não"


def linha_pedido(p, n, agora):
    """Linha da aba Pedidos (n = numero da linha na planilha)."""
    mod = modalidade(p)
    full = mod.startswith("Fulfillment")
    k = f"$A{n}"

    def busca(tipo):
        return (f'IF(COUNTIFS(Lançamentos!$A:$A,{k},Lançamentos!$B:$B,"{tipo}")=0,"pendente",'
                f'SUMIFS(Lançamentos!$C:$C,Lançamentos!$A:$A,{k},Lançamentos!$B:$B,"{tipo}"))')
    canc = f'$F{n}="Cancelado"'
    comissao = f'=IF({canc},"n/a",{busca("Comissão")})'
    tarifa = f'=IF({canc},"n/a",{busca("Tarifa fixa")})'
    frete = '="n/a"' if full else f'=IF({canc},"n/a",{busca("Frete pago")})'
    ful = f'=IF({canc},"n/a",{busca("Fulfillment")})' if full else '="n/a"'
    cmv = (f'=IF({canc},"n/a",IF(COUNTIFS(Itens!$A:$A,{k},Itens!$K:$K,"pendente")>0,"pendente",SUMIFS(Itens!$K:$K,Itens!$A:$A,{k})))')
    adic = (f'=IF({canc},"n/a",IF(COUNTIFS(Itens!$A:$A,{k},Itens!$L:$L,"pendente")+COUNTIFS(Itens!$A:$A,{k},Itens!$M:$M,"pendente")>0,"pendente",'
            f'SUMIFS(Itens!$L:$L,Itens!$A:$A,{k})+SUMIFS(Itens!$M:$M,Itens!$A:$A,{k})))')
    imposto = f'=IF({canc},"n/a",IF(ISNUMBER(Parâmetros!$B$2),G{n}*Parâmetros!$B$2,"pendente"))'
    indireto = f'=IF({canc},"n/a",IF(ISNUMBER(Parâmetros!$B$3),Parâmetros!$B$3,"pendente"))'
    reemb = (f'=IF({canc},"n/a",IF(COUNTIFS(Lançamentos!$A:$A,{k},Lançamentos!$B:$B,"Reembolso")+COUNTIFS(Lançamentos!$A:$A,{k},Lançamentos!$B:$B,"Estorno")>0,'
             f'SUMIFS(Lançamentos!$C:$C,Lançamentos!$A:$A,{k},Lançamentos!$B:$B,"Reembolso")+SUMIFS(Lançamentos!$C:$C,Lançamentos!$A:$A,{k},Lançamentos!$B:$B,"Estorno"),'
             f'IF(ISNUMBER(SEARCH("Devol",$F{n})),"pendente",0)))')
    status = f'=IF({canc},"Fora do resultado",IF(COUNTIF(O{n}:W{n},"pendente")>0,"Incompleto","Completo"))'
    lucro = f'=IF(Z{n}="Completo",J{n}-SUM(O{n}:V{n})-N(W{n}),IF(Z{n}="Fora do resultado","n/a","pendente"))'
    margem = f'=IF(ISNUMBER(X{n}),IF(J{n}=0,0,X{n}/J{n}),"")'
    return [
        p["chave"], p["numero"], p["data_pedido"], p["canal"] or "(sem canal)", mod, p["situacao"], p["total_produtos"], p["valor_frete"], p["valor_desconto"],
        f"=G{n}+H{n}-I{n}", nf_emitida(p), p["data_envio"] or "", p["data_entrega"] or "",
        "n/a" if p["situacao"] == "Cancelado" else "pendente", cmv, adic, comissao, tarifa, frete, ful, imposto, indireto, reemb, lucro, margem, status,
        agora, p.get("forma_envio") or "", p.get("deposito") or "",
    ]
