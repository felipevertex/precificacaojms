"""Importacao incremental do Olist para a planilha "Analise de Pedidos". Pensado para rodar no cron.

A cada execucao:
  1. lista os pedidos dos ultimos DIAS dias (poucas chamadas: a listagem ja traz a situacao);
  2. pedidos que ainda nao estao na planilha: le o pedido e os produtos e acrescenta linhas em Pedidos e Itens
     (SKU novo tambem entra em Produtos e Custos);
  3. pedidos que ja estao na planilha e mudaram de situacao: atualiza situacao, nota e datas;
  4. registra a execucao na aba Logs.
Somente leitura no Olist. Nunca apaga nem sobrescreve nada que o usuario lancou (Lancamentos, Produtos e Custos, Parametros).

Configuracao por variaveis de ambiente:
  OLIST_ENV     arquivo com OLIST_API_TOKEN=... (padrao /opt/precificacao/olist.env)
  SECRETS_PATH  secrets.toml com a secao google_service_account
  SHEET_ID      id da planilha
  DIAS          janela relida para detectar mudanca de situacao (padrao 30)
  DIAS_NOVOS    so pedidos dos ultimos N dias entram como novos (padrao 7)
"""
import json
import os
import sys
import time
import traceback
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from olist import Olist  # noqa: E402
from regras import chave_pedido, linha_item, linha_pedido, linha_produto, nf_emitida  # noqa: E402
from sheets_util import conectar  # noqa: E402

DIAS = int(os.environ.get("DIAS", "30"))            # janela relida para detectar mudanca de situacao
DIAS_NOVOS = int(os.environ.get("DIAS_NOVOS", "7"))  # so pedidos desta janela entram como novos (evita carga historica sem querer)
SHEET_ID = os.environ["SHEET_ID"]
OLIST_ENV = os.environ.get("OLIST_ENV", "/opt/precificacao/olist.env")


def token():
    for linha in open(OLIST_ENV, encoding="utf-8"):
        if linha.startswith("OLIST_API_TOKEN="):
            return linha.split("=", 1)[1].strip()
    raise SystemExit("OLIST_API_TOKEN nao encontrado em " + OLIST_ENV)


def main():
    inicio = time.time()
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    ol = Olist(token())
    sh = conectar().open_by_key(SHEET_ID)
    ws_p, ws_i, ws_pc, ws_log = (sh.worksheet(n) for n in ("Pedidos", "Itens", "Produtos e Custos", "Logs"))

    linhas_p = ws_p.get("A3:F")
    existentes = {}
    for i, l in enumerate(linhas_p, start=3):
        if len(l) >= 2 and l[1]:
            existentes[str(l[1])] = {"linha": i, "chave": l[0], "situacao": l[5] if len(l) > 5 else ""}
    chaves_usadas = {v["chave"] for v in existentes.values()}
    proxima_p = 3 + len(linhas_p)

    resumo = ol.listar(datetime.now() - timedelta(days=DIAS - 1), datetime.now())
    limite_novos = (datetime.now() - timedelta(days=DIAS_NOVOS - 1)).replace(hour=0, minute=0, second=0, microsecond=0)

    def recente(r):
        try:
            return datetime.strptime(r["data_pedido"], "%d/%m/%Y") >= limite_novos
        except Exception:
            return True
    novos = [r for r in resumo if str(r["numero"]) not in existentes and recente(r)]
    mudaram = [r for r in resumo if str(r["numero"]) in existentes and (r.get("situacao") or "") != existentes[str(r["numero"])]["situacao"]]
    print(f"{len(resumo)} pedidos na janela | {len(novos)} novos | {len(mudaram)} com situacao alterada (janela {DIAS}d, novos {DIAS_NOVOS}d)", flush=True)

    # ---- novos
    n_itens = n_prod_novos = 0
    if novos:
        produtos = {}
        skus_planilha = {l[0] for l in ws_pc.get("A2:A") if l}
        proxima_i = 2 + len(ws_i.get("A2:A"))
        proxima_pc = 2 + len(ws_pc.get("A2:A"))
        pedidos = []
        for r in sorted(novos, key=lambda x: int(x["numero"])):
            p = ol.pedido(r["id"])
            chave = chave_pedido(p)
            if chave in chaves_usadas:
                k = 2
                while f"{chave}#{k}" in chaves_usadas:
                    k += 1
                chave = f"{chave}#{k}"
            chaves_usadas.add(chave)
            p["chave"] = chave
            pedidos.append(p)
        for p in pedidos:
            for it in p["itens"]:
                if it["id_produto"] not in produtos:
                    produtos[it["id_produto"]] = ol.produto(it["id_produto"])
        for pid in {c["id_produto"] for pr in list(produtos.values()) for c in pr["kit"]} - set(produtos):
            produtos[pid] = ol.produto(pid)

        linhas_pedidos, linhas_itens, linhas_prod = [], [], []
        for p in pedidos:
            linhas_pedidos.append(linha_pedido(p, proxima_p + len(linhas_pedidos), agora))
            for it in p["itens"]:
                linhas_itens.append(linha_item(p, it, produtos, proxima_i + len(linhas_itens)))
                if it["sku"] not in skus_planilha:
                    skus_planilha.add(it["sku"])
                    linhas_prod.append(linha_produto(it["sku"], produtos.get(it["id_produto"]), produtos, proxima_pc + len(linhas_prod)))
        ws_p.update(range_name=f"A{proxima_p}", values=linhas_pedidos, value_input_option="USER_ENTERED")
        if linhas_itens:
            ws_i.update(range_name=f"A{proxima_i}", values=linhas_itens, value_input_option="USER_ENTERED")
        if linhas_prod:
            ws_pc.update(range_name=f"A{proxima_pc}", values=linhas_prod, value_input_option="USER_ENTERED")
        n_itens, n_prod_novos = len(linhas_itens), len(linhas_prod)

    # ---- situacao alterada
    atualizacoes = []
    for r in mudaram:
        p = ol.pedido(r["id"])
        ln = existentes[str(r["numero"])]["linha"]
        atualizacoes.append({"range": f"F{ln}", "values": [[p["situacao"]]]})
        atualizacoes.append({"range": f"K{ln}:M{ln}", "values": [[nf_emitida(p), p["data_envio"] or "", p["data_entrega"] or ""]]})
        atualizacoes.append({"range": f"AA{ln}", "values": [[agora]]})
    if atualizacoes:
        ws_p.batch_update(atualizacoes, value_input_option="USER_ENTERED")

    ws_log.append_row([agora, "Importação incremental do Olist", len(novos), n_itens, n_prod_novos, 0,
                       f"{len(mudaram)} pedidos com situação atualizada. Janela de {DIAS} dias, novos dos últimos {DIAS_NOVOS}. {round(time.time() - inicio)}s."],
                      value_input_option="USER_ENTERED")
    print("OK", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        try:
            sh = conectar().open_by_key(SHEET_ID)
            sh.worksheet("Logs").append_row([datetime.now().strftime("%d/%m/%Y %H:%M"), "ERRO na importação incremental", 0, 0, 0, 1, str(e)[:300]])
        except Exception:
            pass
        sys.exit(1)
