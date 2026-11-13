"""Busca pedidos do Olist (API 2.0) dos ultimos N dias, com itens e custo de cada produto.

Somente leitura. Guarda apenas campos necessarios para a rentabilidade, SEM dados
pessoais de clientes (nome, CPF, endereco, e-mail, telefone ficam de fora).
Saida: dados/olist_pedidos.json (pasta ignorada pelo git).

Uso: python scripts/olist_buscar_pedidos.py [dias=7]
Retomavel: o progresso fica em dados/olist_cache.json.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(RAIZ, "dados")
CACHE = os.path.join(DADOS, "olist_cache.json")
SAIDA = os.path.join(DADOS, "olist_pedidos.json")
PAUSA = 2.3


def token():
    for linha in open(os.path.join(RAIZ, ".env"), encoding="utf-8"):
        if linha.startswith("OLIST_API_TOKEN="):
            return linha.split("=", 1)[1].strip()
    raise SystemExit("OLIST_API_TOKEN nao encontrado no .env")


TOK = token()


def chamar(endpoint, **params):
    corpo = urllib.parse.urlencode({"token": TOK, "formato": "json", **params}).encode()
    for tentativa in range(6):
        try:
            req = urllib.request.Request(f"https://api.tiny.com.br/api2/{endpoint}", data=corpo)
            r = json.loads(urllib.request.urlopen(req, timeout=40).read())["retorno"]
        except Exception as e:  # rede, timeout
            print(f"  erro de rede ({e}); aguardando 20s", flush=True)
            time.sleep(20)
            continue
        if r.get("status") == "OK":
            time.sleep(PAUSA)
            return r
        erros = json.dumps(r.get("erros", ""), ensure_ascii=False)
        if "xcedido" in erros or "loqueada" in erros or str(r.get("codigo_erro")) == "6":
            print("  limite da API atingido; aguardando 70s", flush=True)
            time.sleep(70)
            continue
        raise RuntimeError(f"{endpoint}: {erros}")
    raise RuntimeError(f"{endpoint}: tentativas esgotadas")


def carregar_cache():
    if os.path.exists(CACHE):
        return json.load(open(CACHE, encoding="utf-8"))
    return {"pedidos": {}, "produtos": {}}


def salvar_cache(c):
    json.dump(c, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)


def listar_ids(dias):
    fim = datetime.now()
    ini = fim - timedelta(days=dias - 1)
    ids, pag = [], 1
    while True:
        r = chamar("pedidos.pesquisa.php", dataInicial=ini.strftime("%d/%m/%Y"), dataFinal=fim.strftime("%d/%m/%Y"), pagina=pag)
        ids += [p["pedido"]["id"] for p in r["pedidos"]]
        if pag >= int(r.get("numero_paginas", 1)):
            break
        pag += 1
    return ids, ini, fim


def enxugar_pedido(p):
    eco = p.get("ecommerce") or {}
    itens = []
    for i in p.get("itens", []):
        it = i["item"]
        itens.append({
            "sku": it.get("codigo"), "id_produto": it.get("id_produto"), "descricao": it.get("descricao"),
            "quantidade": float(it.get("quantidade") or 0), "valor_unitario": float(it.get("valor_unitario") or 0),
        })
    f = lambda k: float(p.get(k) or 0)
    return {
        "id": p.get("id"), "numero": p.get("numero"), "numero_ecommerce": p.get("numero_ecommerce"),
        "data_pedido": p.get("data_pedido"), "data_faturamento": p.get("data_faturamento"),
        "data_envio": p.get("data_envio"), "data_entrega": p.get("data_entrega"),
        "situacao": p.get("situacao"), "canal": eco.get("nomeEcommerce"), "deposito": p.get("deposito"),
        "forma_envio": p.get("forma_envio"), "valor_frete": f("valor_frete"), "valor_desconto": f("valor_desconto"),
        "outras_despesas": f("outras_despesas"), "total_produtos": f("total_produtos"), "total_pedido": f("total_pedido"),
        "id_nota_fiscal": p.get("id_nota_fiscal"), "itens": itens,
    }


def enxugar_produto(pr):
    f = lambda k: float(pr.get(k) or 0)
    kit = []
    for k in pr.get("kit") or []:
        c = k.get("item", k)
        kit.append({"id_produto": c.get("id_produto"), "quantidade": float(c.get("quantidade") or 0)})
    return {
        "id": pr.get("id"), "sku": pr.get("codigo"), "nome": pr.get("nome"), "classe": pr.get("classe_produto"),
        "preco_venda": f("preco"), "preco_custo": f("preco_custo"), "preco_custo_medio": f("preco_custo_medio"),
        "ncm": pr.get("ncm"), "origem": pr.get("origem"), "categoria": pr.get("categoria"),
        "peso_bruto": f("peso_bruto"), "unidade": pr.get("unidade"), "kit": kit,
        "consultado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def main():
    dias = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    os.makedirs(DADOS, exist_ok=True)
    cache = carregar_cache()
    ids, ini, fim = listar_ids(dias)
    print(f"{len(ids)} pedidos entre {ini:%d/%m} e {fim:%d/%m}", flush=True)

    for n, pid in enumerate(ids, 1):
        if pid in cache["pedidos"]:
            continue
        cache["pedidos"][pid] = enxugar_pedido(chamar("pedido.obter.php", id=pid)["pedido"])
        if n % 10 == 0:
            salvar_cache(cache)
            print(f"  pedidos {n}/{len(ids)}", flush=True)
    salvar_cache(cache)

    pendentes = {i["id_produto"] for p in cache["pedidos"].values() for i in p["itens"]} - set(cache["produtos"])
    print(f"{len(pendentes)} produtos para consultar", flush=True)
    for n, prod_id in enumerate(sorted(pendentes), 1):
        cache["produtos"][prod_id] = enxugar_produto(chamar("produto.obter.php", id=prod_id)["produto"])
        if n % 10 == 0:
            salvar_cache(cache)
            print(f"  produtos {n}/{len(pendentes)}", flush=True)

    componentes = {c["id_produto"] for pr in cache["produtos"].values() for c in pr["kit"]} - set(cache["produtos"])
    print(f"{len(componentes)} componentes de kit para consultar", flush=True)
    for prod_id in sorted(componentes):
        cache["produtos"][prod_id] = enxugar_produto(chamar("produto.obter.php", id=prod_id)["produto"])
    salvar_cache(cache)

    json.dump(
        {"gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M"), "periodo": [ini.strftime("%d/%m/%Y"), fim.strftime("%d/%m/%Y")],
         "pedidos": [cache["pedidos"][i] for i in ids], "produtos": cache["produtos"]},
        open(SAIDA, "w", encoding="utf-8"), ensure_ascii=False)
    print("FIM:", SAIDA, flush=True)


if __name__ == "__main__":
    main()
