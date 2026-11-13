"""Cliente minimo, somente leitura, da API 2.0 do Olist (Tiny).

Guarda apenas campos necessarios para rentabilidade, SEM dados pessoais de clientes.
"""
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime


class Olist:
    def __init__(self, token, pausa=2.3):
        self.token = token
        self.pausa = pausa

    def chamar(self, endpoint, **params):
        corpo = urllib.parse.urlencode({"token": self.token, "formato": "json", **params}).encode()
        for _ in range(6):
            try:
                req = urllib.request.Request(f"https://api.tiny.com.br/api2/{endpoint}", data=corpo)
                r = json.loads(urllib.request.urlopen(req, timeout=40).read())["retorno"]
            except Exception as e:
                print(f"  erro de rede ({e}); aguardando 20s", flush=True)
                time.sleep(20)
                continue
            if r.get("status") == "OK":
                time.sleep(self.pausa)
                return r
            erros = json.dumps(r.get("erros", ""), ensure_ascii=False)
            if "xcedido" in erros or "loqueada" in erros or str(r.get("codigo_erro")) == "6":
                print("  limite da API atingido; aguardando 70s", flush=True)
                time.sleep(70)
                continue
            if str(r.get("codigo_erro")) == "20" or "nao retornou registros" in erros.lower():
                return {"status": "OK", "pedidos": [], "numero_paginas": 1}
            raise RuntimeError(f"{endpoint}: {erros}")
        raise RuntimeError(f"{endpoint}: tentativas esgotadas")

    def listar(self, ini, fim):
        """Resumo dos pedidos entre duas datas (datetime). Inclui a situacao atual."""
        saida, pag = [], 1
        while True:
            r = self.chamar("pedidos.pesquisa.php", dataInicial=ini.strftime("%d/%m/%Y"), dataFinal=fim.strftime("%d/%m/%Y"), pagina=pag)
            saida += [p["pedido"] for p in r.get("pedidos", [])]
            if pag >= int(r.get("numero_paginas", 1)):
                return saida
            pag += 1

    def pedido(self, pid):
        return enxugar_pedido(self.chamar("pedido.obter.php", id=pid)["pedido"])

    def produto(self, prod_id):
        return enxugar_produto(self.chamar("produto.obter.php", id=prod_id)["produto"])


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
