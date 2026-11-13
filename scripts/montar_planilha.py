"""Monta a planilha "Analise de Pedidos" (Etapa 1) a partir de dados/olist_pedidos.json.

Cria as abas, formatos, formulas e regras de cor, e grava os pedidos e itens importados.
Idempotente: reconstroi as abas a cada execucao (a planilha e gerada, nao editada a mao
nas abas Pedidos e Itens; Produtos e Custos, Lancamentos, Parametros, Fulfillment e
Custos indiretos guardam dados do usuario, por isso so sao recriadas com --reset).

Credenciais: conta de servico do Google lida de um secrets.toml (secao google_service_account),
caminho em SECRETS_PATH. Nunca versionar o arquivo.

Uso (na VPS, onde esta a chave):
    SECRETS_PATH=/opt/jmsecom/app/.streamlit/secrets.toml SHEET_ID=<id> \
        python montar_planilha.py /tmp/olist_pedidos.json [--reset]
"""
import json
import os
import sys
import tomllib
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials


from regras import chave_pedido, linha_item, linha_pedido, linha_produto, modalidade, custo_do_produto  # noqa: E402,F401
from sheets_util import conectar  # noqa: E402

SHEET_ID = os.environ["SHEET_ID"]
SECRETS = os.environ["SECRETS_PATH"]
ARQ = sys.argv[1]
RESET = "--reset" in sys.argv

AZUL, AZUL_BG = (0.18, 0.37, 0.66), (0.87, 0.91, 0.96)
TEAL_BG = (0.86, 0.93, 0.94)
AMBAR_BG = (0.97, 0.93, 0.82)
CINZA_BG = (0.91, 0.93, 0.93)
VERDE_BG = (0.86, 0.94, 0.89)
VERM_BG = (0.97, 0.88, 0.87)
BRANCO = (1, 1, 1)
TEXTO = (0.08, 0.13, 0.17)


def cor(t):
    return {"red": t[0], "green": t[1], "blue": t[2]}


# ---------------------------------------------------------------- dados
def carregar():
    d = json.load(open(ARQ, encoding="utf-8"))
    produtos = d["produtos"]
    pedidos, vistos = [], {}
    for p in d["pedidos"]:
        chave = chave_pedido(p)
        vistos[chave] = vistos.get(chave, 0) + 1
        if vistos[chave] > 1:
            chave = f"{chave}#{vistos[chave]}"
        p["chave"] = chave
        pedidos.append(p)

    def ordem(p):
        try:
            return datetime.strptime(p["data_pedido"], "%d/%m/%Y")
        except Exception:
            return datetime.min
    pedidos.sort(key=lambda p: (ordem(p), int(p["numero"])), reverse=True)
    return d, pedidos, produtos


# ---------------------------------------------------------------- abas
def garantir_aba(sh, titulo, linhas, colunas, apagar=True):
    try:
        ws = sh.worksheet(titulo)
        if apagar:
            ws.clear()
        ws.resize(rows=linhas, cols=colunas)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(titulo, rows=linhas, cols=colunas)
    return ws


def req_fundo(sid, r0, r1, c0, c1, bg, bold=False, fg=TEXTO, wrap=False, halign=None):
    f = {"backgroundColor": cor(bg), "textFormat": {"foregroundColor": cor(fg), "bold": bold}}
    campos = "userEnteredFormat(backgroundColor,textFormat)"
    if wrap:
        f["wrapStrategy"] = "WRAP"
        campos = "userEnteredFormat(backgroundColor,textFormat,wrapStrategy)"
    if halign:
        f["horizontalAlignment"] = halign
        campos = campos[:-1] + ",horizontalAlignment)"
    return {"repeatCell": {"range": {"sheetId": sid, "startRowIndex": r0, "endRowIndex": r1, "startColumnIndex": c0, "endColumnIndex": c1},
                           "cell": {"userEnteredFormat": f}, "fields": campos}}


def req_numfmt(sid, r0, r1, c0, c1, tipo, padrao):
    return {"repeatCell": {"range": {"sheetId": sid, "startRowIndex": r0, "endRowIndex": r1, "startColumnIndex": c0, "endColumnIndex": c1},
                           "cell": {"userEnteredFormat": {"numberFormat": {"type": tipo, "pattern": padrao}}}, "fields": "userEnteredFormat.numberFormat"}}


def req_largura(sid, c0, c1, px):
    return {"updateDimensionProperties": {"range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": c0, "endIndex": c1},
                                          "properties": {"pixelSize": px}, "fields": "pixelSize"}}


def req_congelar(sid, linhas, colunas):
    return {"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": linhas, "frozenColumnCount": colunas}},
                                      "fields": "gridProperties(frozenRowCount,frozenColumnCount)"}}


def req_merge(sid, r0, r1, c0, c1):
    return {"mergeCells": {"range": {"sheetId": sid, "startRowIndex": r0, "endRowIndex": r1, "startColumnIndex": c0, "endColumnIndex": c1}, "mergeType": "MERGE_ALL"}}


def req_regra_texto(sid, c0, c1, r0, texto, bg, fg=TEXTO, tipo="TEXT_EQ", idx=0):
    return {"addConditionalFormatRule": {"index": idx, "rule": {
        "ranges": [{"sheetId": sid, "startRowIndex": r0, "endRowIndex": 3000, "startColumnIndex": c0, "endColumnIndex": c1}],
        "booleanRule": {"condition": {"type": tipo, "values": [{"userEnteredValue": texto}]},
                        "format": {"backgroundColor": cor(bg), "textFormat": {"foregroundColor": cor(fg)}}}}}}


def req_regra_num(sid, c0, c1, r0, tipo, valor, bg, fg=TEXTO):
    return {"addConditionalFormatRule": {"index": 0, "rule": {
        "ranges": [{"sheetId": sid, "startRowIndex": r0, "endRowIndex": 3000, "startColumnIndex": c0, "endColumnIndex": c1}],
        "booleanRule": {"condition": {"type": tipo, "values": [{"userEnteredValue": str(valor)}]},
                        "format": {"backgroundColor": cor(bg), "textFormat": {"foregroundColor": cor(fg)}}}}}}


def limpar_regras(sh, ws):
    meta = sh.fetch_sheet_metadata()
    for s in meta["sheets"]:
        if s["properties"]["sheetId"] == ws.id:
            n = len(s.get("conditionalFormats", []))
            if n:
                sh.batch_update({"requests": [{"deleteConditionalFormatRule": {"sheetId": ws.id, "index": 0}} for _ in range(n)]})


def validacao_lista(sid, r0, c, itens):
    return {"setDataValidation": {"range": {"sheetId": sid, "startRowIndex": r0, "endRowIndex": 3000, "startColumnIndex": c, "endColumnIndex": c + 1},
                                  "rule": {"condition": {"type": "ONE_OF_LIST", "values": [{"userEnteredValue": i} for i in itens]},
                                           "showCustomUi": True, "strict": False}}}


# ---------------------------------------------------------------- construcao
def main():
    d, pedidos, produtos = carregar()
    gc = conectar()
    sh = gc.open_by_key(SHEET_ID)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    periodo = f"{d['periodo'][0]} a {d['periodo'][1]}"

    sh.batch_update({"requests": [{"updateSpreadsheetProperties": {"properties": {"locale": "pt_BR", "timeZone": "America/Cuiaba",
                                                                                   "title": "Análise de Pedidos"}, "fields": "locale,timeZone"}}]})

    # abas na ordem final; a aba inicial "Página1" e removida no fim
    nomes = ["LEIA-ME", "Dashboard", "Pedidos", "Itens", "Produtos e Custos", "Lançamentos", "Fulfillment (lotes)", "Custos indiretos", "Parâmetros", "Logs"]
    ws = {}
    manter = {"Produtos e Custos", "Lançamentos", "Fulfillment (lotes)", "Custos indiretos", "Parâmetros", "Logs"}
    existentes = {w.title: w for w in sh.worksheets()}
    reconstruidas = set()
    for n in nomes:
        existe = n in existentes
        apagar = RESET or not existe or n not in manter
        if existe:
            w = existentes[n]
            if apagar:
                w.clear()
            w.resize(rows=3000, cols=30)
        else:
            w = sh.add_worksheet(n, rows=3000, cols=30)
        ws[n] = w
        if apagar:
            reconstruidas.add(n)
    meta = sh.fetch_sheet_metadata()
    limpar = []
    for s_ in meta["sheets"]:
        if s_["properties"]["title"] in reconstruidas:
            limpar += [{"deleteConditionalFormatRule": {"sheetId": s_["properties"]["sheetId"], "index": 0}} for _ in s_.get("conditionalFormats", [])]
    if limpar:
        sh.batch_update({"requests": limpar})
    # ordem das abas
    sh.batch_update({"requests": [{"updateSheetProperties": {"properties": {"sheetId": ws[n].id, "index": i}, "fields": "index"}} for i, n in enumerate(nomes)]})
    for s in sh.worksheets():
        if s.title not in nomes:
            sh.del_worksheet(s)

    reqs = []

    # ============ ITENS
    itens_pares = [(p, it) for p in pedidos for it in p["itens"]]
    itens_linhas = itens_pares
    cab_itens = ["Pedido no canal", "Nº Olist", "SKU", "Descrição", "Qtd", "Valor unitário", "Valor total",
                 "Custo unit. (médio Olist)", "Custo unit. (último, referência)", "Custo lido em", "Custo total (CMV)",
                 "Custos adicionais (embalagem e preparação)", "Frete aos centros (rateado)", "Obs. do custo", "Tipo", "NCM", "Origem"]
    w = ws["Itens"]
    w.update(range_name="A1", values=[cab_itens], value_input_option="USER_ENTERED")
    linhas = [linha_item(p, it, produtos, n) for n, (p, it) in enumerate(itens_pares, start=2)]
    if linhas:
        w.update(range_name="A2", values=linhas, value_input_option="USER_ENTERED")
    sid = w.id
    reqs += [req_fundo(sid, 0, 1, 0, 17, AZUL_BG, bold=True, wrap=True), req_congelar(sid, 1, 3),
             req_numfmt(sid, 1, 3000, 5, 12, "CURRENCY", "R$ #,##0.00"), req_numfmt(sid, 1, 3000, 4, 5, "NUMBER", "0"),
             req_numfmt(sid, 1, 3000, 9, 10, "DATE_TIME", "dd/mm/yyyy hh:mm"),
             req_largura(sid, 0, 1, 170), req_largura(sid, 1, 2, 70), req_largura(sid, 2, 3, 90), req_largura(sid, 3, 4, 330),
             req_largura(sid, 4, 5, 50), req_largura(sid, 5, 12, 120), req_largura(sid, 12, 13, 130), req_largura(sid, 13, 14, 200),
             req_largura(sid, 14, 17, 90),
             {"setBasicFilter": {"filter": {"range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": max(2, len(linhas) + 1), "startColumnIndex": 0, "endColumnIndex": 17}}}},
             req_regra_texto(sid, 5, 14, 1, "pendente", AMBAR_BG, (0.69, 0.44, 0.06)),
             req_regra_texto(sid, 5, 14, 1, "n/a", CINZA_BG, (0.42, 0.48, 0.51))]

    # ============ PRODUTOS E CUSTOS
    wp = ws["Produtos e Custos"]
    if "Produtos e Custos" in reconstruidas:
        skus = {}
        for p in pedidos:
            for it in p["itens"]:
                skus.setdefault(it["sku"], it["id_produto"])
        cab_p = ["SKU", "Nome", "Tipo", "Custo médio (Olist)", "Custo último (Olist)", "Custo lido em", "Embalagem (R$/un)", "Caixa e proteção (R$/un)",
                 "Fita e etiqueta (R$/un)", "Mão de obra de preparação (R$/un)", "Outros (R$/un)", "Custo adicional unit.", "Custo total unit.",
                 "NCM", "Origem", "Categoria", "Peso (kg)", "Observação"]
        lp = [linha_produto(sku, produtos.get(pid), produtos, n) for n, (sku, pid) in enumerate(sorted(skus.items()), start=2)]
        wp.update(range_name="A1", values=[cab_p], value_input_option="USER_ENTERED")
        if lp:
            wp.update(range_name="A2", values=lp, value_input_option="USER_ENTERED")
        sid = wp.id
        reqs += [req_fundo(sid, 0, 1, 0, 6, AZUL_BG, bold=True, wrap=True), req_fundo(sid, 0, 1, 6, 11, CINZA_BG, bold=True, wrap=True),
                 req_fundo(sid, 0, 1, 11, 13, VERDE_BG, bold=True, wrap=True), req_fundo(sid, 0, 1, 13, 18, AZUL_BG, bold=True, wrap=True),
                 req_congelar(sid, 1, 2), req_numfmt(sid, 1, 3000, 3, 5, "CURRENCY", "R$ #,##0.00"), req_numfmt(sid, 1, 3000, 6, 13, "CURRENCY", "R$ #,##0.00"),
                 req_numfmt(sid, 1, 3000, 5, 6, "DATE_TIME", "dd/mm/yyyy hh:mm"),
                 req_largura(sid, 0, 1, 100), req_largura(sid, 1, 2, 330), req_largura(sid, 2, 3, 70), req_largura(sid, 3, 13, 115),
                 req_largura(sid, 13, 17, 95), req_largura(sid, 17, 18, 220),
                 {"setBasicFilter": {"filter": {"range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": max(2, len(lp) + 1), "startColumnIndex": 0, "endColumnIndex": 18}}}},
                 req_regra_texto(sid, 3, 13, 1, "pendente", AMBAR_BG, (0.69, 0.44, 0.06))]

    # ============ LANÇAMENTOS
    wl = ws["Lançamentos"]
    if "Lançamentos" in reconstruidas:
        wl.update(range_name="A1", values=[["Pedido no canal", "Tipo", "Valor (R$, custo = positivo)", "Data", "Fonte", "Referência (arquivo ou ID)", "Observação"]],
                  value_input_option="USER_ENTERED")
        sid = wl.id
        reqs += [req_fundo(sid, 0, 1, 0, 7, AMBAR_BG, bold=True, wrap=True), req_congelar(sid, 1, 0),
                 validacao_lista(sid, 1, 1, ["Comissão", "Tarifa fixa", "Frete pago", "Fulfillment", "Outras cobranças", "Reembolso", "Estorno"]),
                 validacao_lista(sid, 1, 4, ["Relatório Mercado Livre", "Relatório Amazon", "Relatório Shopee", "Relatório Magalu", "Relatório KaBuM", "API", "Manual"]),
                 req_numfmt(sid, 1, 3000, 2, 3, "CURRENCY", "R$ #,##0.00"), req_numfmt(sid, 1, 3000, 3, 4, "DATE", "dd/mm/yyyy"),
                 req_largura(sid, 0, 1, 190), req_largura(sid, 1, 2, 130), req_largura(sid, 2, 3, 150), req_largura(sid, 3, 4, 90),
                 req_largura(sid, 4, 5, 170), req_largura(sid, 5, 6, 210), req_largura(sid, 6, 7, 260)]

    # ============ FULFILLMENT (LOTES)
    wf = ws["Fulfillment (lotes)"]
    if "Fulfillment (lotes)" in reconstruidas:
        wf.update(range_name="A1", values=[["Lote", "Data do envio", "Centro (canal)", "Transportadora", "Frete (R$)", "Preparação e embalagem do lote (R$)", "Outros (R$)",
                                            "SKU", "Qtd enviada", "Critério de rateio", "Custo unit. rateado", "Observação"]], value_input_option="USER_ENTERED")
        sid = wf.id
        reqs += [req_fundo(sid, 0, 1, 0, 12, CINZA_BG, bold=True, wrap=True), req_congelar(sid, 1, 0),
                 validacao_lista(sid, 1, 9, ["Valor", "Peso", "Unidade", "Volume"]),
                 req_numfmt(sid, 1, 3000, 4, 7, "CURRENCY", "R$ #,##0.00"), req_numfmt(sid, 1, 3000, 10, 11, "CURRENCY", "R$ #,##0.00"),
                 req_numfmt(sid, 1, 3000, 1, 2, "DATE", "dd/mm/yyyy"), req_largura(sid, 0, 12, 130), req_largura(sid, 11, 12, 240)]

    # ============ CUSTOS INDIRETOS
    wc = ws["Custos indiretos"]
    if "Custos indiretos" in reconstruidas:
        wc.update(range_name="A1", values=[["Descrição", "Categoria", "Valor mensal (R$)", "Mês de referência", "Critério de rateio", "Observação"]], value_input_option="USER_ENTERED")
        sid = wc.id
        reqs += [req_fundo(sid, 0, 1, 0, 6, CINZA_BG, bold=True, wrap=True), req_congelar(sid, 1, 0),
                 validacao_lista(sid, 1, 4, ["Por pedido", "Por item", "Por valor vendido", "Por volume"]),
                 validacao_lista(sid, 1, 1, ["Administrativo", "Estoque", "Materiais gerais", "Expedição", "Ferramentas", "Pessoal", "Outros"]),
                 req_numfmt(sid, 1, 3000, 2, 3, "CURRENCY", "R$ #,##0.00"), req_largura(sid, 0, 1, 260), req_largura(sid, 1, 6, 150), req_largura(sid, 5, 6, 260)]

    # ============ PARÂMETROS
    wpar = ws["Parâmetros"]
    if "Parâmetros" in reconstruidas:
        canais = sorted({p["canal"] or "(sem canal)" for p in pedidos})
        linhas_par = [
            ["PARÂMETROS GERAIS", "", "", ""],
            ["Alíquota estimada de impostos sobre produtos", 0.025, "Herdado da planilha manual (2,5%). Estimativa gerencial, a validar com o contador. Não é apuração fiscal.", ""],
            ["Custo indireto por pedido (R$)", "", "Preencher depois de cadastrar os custos indiretos e escolher o critério de rateio. Vazio = pendente.", ""],
            ["", "", "", ""],
            ["HISTÓRICO DE ALÍQUOTAS", "", "", ""],
            ["Início da vigência", "Alíquota", "Origem", "Validada pelo contador?"],
            [datetime.now().strftime("%d/%m/%Y"), 0.025, "Planilha manual anterior", "Não"],
            ["", "", "", ""],
            ["FONTE DOS DADOS FINANCEIROS POR CANAL", "", "", ""],
            ["Canal", "Fonte hoje", "Situação", "Observação"],
        ]
        for c in canais:
            linhas_par.append([c, "Relatório do marketplace (a definir)", "Aguardando relatório de exemplo", "Comissão, tarifa fixa, frete pago, fulfillment, reembolsos e repasse"])
        wpar.update(range_name="A1", values=linhas_par, value_input_option="USER_ENTERED")
        sid = wpar.id
        reqs += [req_fundo(sid, 0, 1, 0, 4, CINZA_BG, bold=True), req_fundo(sid, 4, 5, 0, 4, CINZA_BG, bold=True), req_fundo(sid, 8, 9, 0, 4, CINZA_BG, bold=True),
                 req_fundo(sid, 5, 6, 0, 4, AZUL_BG, bold=True), req_fundo(sid, 9, 10, 0, 4, AZUL_BG, bold=True),
                 req_numfmt(sid, 1, 2, 1, 2, "PERCENT", "0.00%"), req_numfmt(sid, 6, 7, 1, 2, "PERCENT", "0.00%"), req_numfmt(sid, 2, 3, 1, 2, "CURRENCY", "R$ #,##0.00"),
                 req_largura(sid, 0, 1, 330), req_largura(sid, 1, 2, 220), req_largura(sid, 2, 3, 420), req_largura(sid, 3, 4, 320)]

    # ============ LOGS
    wlog = ws["Logs"]
    if "Logs" in reconstruidas:
        wlog.update(range_name="A1", values=[["Data e hora", "Ação", "Pedidos lidos", "Itens gravados", "Produtos consultados", "Erros", "Detalhe"]], value_input_option="USER_ENTERED")
        reqs += [req_fundo(wlog.id, 0, 1, 0, 7, CINZA_BG, bold=True), req_congelar(wlog.id, 1, 0), req_largura(wlog.id, 0, 1, 140), req_largura(wlog.id, 1, 2, 220),
                 req_largura(wlog.id, 2, 6, 120), req_largura(wlog.id, 6, 7, 400)]
    wlog.append_row([agora, "Importação inicial do Olist (somente leitura)", len(pedidos), len(itens_linhas), len(produtos), 0,
                     f"Período {periodo}. Custo = custo médio do cadastro no momento da leitura."], value_input_option="USER_ENTERED")

    # ============ PEDIDOS
    wpd = ws["Pedidos"]
    cab = ["Pedido no canal", "Nº Olist", "Data do pedido", "Canal", "Modalidade", "Situação", "Produtos", "Frete cobrado do cliente", "Descontos",
           "Receita", "NF emitida", "Data de envio", "Data de entrega",
           "ICMS da nota", "Custo dos produtos (CMV)", "Custos adicionais", "Comissão", "Tarifa fixa", "Frete pago", "Fulfillment e outras cobranças",
           "Imposto estimado", "Custos indiretos", "Reembolsos e estornos", "Lucro", "Margem", "Dado", "Importado em", "Forma de envio (Olist)", "Depósito (Olist)"]
    grupos = [("Olist", 0, 13, AZUL_BG), ("XML da nota", 13, 14, TEAL_BG), ("Custos próprios", 14, 16, CINZA_BG), ("Marketplace", 16, 20, AMBAR_BG),
              ("Calculado", 20, 26, VERDE_BG), ("Controle e origem", 26, 29, CINZA_BG)]
    topo = [[""] * len(cab)]
    for nome, a, b, _ in grupos:
        topo[0][a] = nome
    wpd.update(range_name="A1", values=topo + [cab], value_input_option="USER_ENTERED")
    dados = [linha_pedido(p, n, agora) for n, p in enumerate(pedidos, start=3)]
    wpd.update(range_name="A3", values=dados, value_input_option="USER_ENTERED")
    sid = wpd.id
    ult = len(dados) + 2
    for nome, a, b, bg in grupos:
        reqs.append(req_fundo(sid, 0, 1, a, b, bg, bold=True))
    reqs += [req_fundo(sid, 1, 2, 0, 29, BRANCO, bold=True, wrap=True), req_congelar(sid, 2, 1),
             req_numfmt(sid, 2, 3000, 6, 10, "CURRENCY", "R$ #,##0.00"), req_numfmt(sid, 2, 3000, 14, 23, "CURRENCY", "R$ #,##0.00"),
             req_numfmt(sid, 2, 3000, 23, 24, "CURRENCY", "R$ #,##0.00"), req_numfmt(sid, 2, 3000, 24, 25, "PERCENT", "0.0%"),
             req_numfmt(sid, 2, 3000, 13, 14, "CURRENCY", "R$ #,##0.00"), req_numfmt(sid, 2, 3000, 26, 27, "DATE_TIME", "dd/mm/yyyy hh:mm"), req_numfmt(sid, 2, 3000, 2, 3, "DATE", "dd/mm/yyyy"), req_numfmt(sid, 2, 3000, 11, 13, "DATE", "dd/mm/yyyy"),
             req_largura(sid, 0, 1, 170), req_largura(sid, 1, 2, 65), req_largura(sid, 2, 3, 95), req_largura(sid, 3, 4, 170), req_largura(sid, 4, 5, 190),
             req_largura(sid, 5, 6, 100), req_largura(sid, 6, 10, 105), req_largura(sid, 10, 13, 90), req_largura(sid, 13, 23, 115),
             req_largura(sid, 23, 25, 100), req_largura(sid, 25, 26, 130), req_largura(sid, 26, 29, 130),
             {"setBasicFilter": {"filter": {"range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": max(3, ult), "startColumnIndex": 0, "endColumnIndex": 29}}}},
             req_regra_texto(sid, 13, 23, 2, "pendente", AMBAR_BG, (0.69, 0.44, 0.06)),
             req_regra_texto(sid, 13, 24, 2, "n/a", CINZA_BG, (0.42, 0.48, 0.51)),
             req_regra_texto(sid, 23, 24, 2, "pendente", AMBAR_BG, (0.69, 0.44, 0.06)),
             req_regra_num(sid, 23, 24, 2, "NUMBER_LESS", 0, VERM_BG, (0.70, 0.22, 0.18)),
             req_regra_num(sid, 23, 24, 2, "NUMBER_GREATER", 0, VERDE_BG, (0.16, 0.49, 0.31)),
             req_regra_texto(sid, 25, 26, 2, "Completo", VERDE_BG, (0.16, 0.49, 0.31)),
             req_regra_texto(sid, 25, 26, 2, "Incompleto", AMBAR_BG, (0.69, 0.44, 0.06)),
             req_regra_texto(sid, 25, 26, 2, "Fora do resultado", CINZA_BG, (0.42, 0.48, 0.51)),
             req_regra_texto(sid, 5, 6, 2, "Cancelado", CINZA_BG, (0.42, 0.48, 0.51)),
             req_regra_texto(sid, 5, 6, 2, "Devol", VERM_BG, (0.70, 0.22, 0.18), tipo="TEXT_CONTAINS")]

    # ============ DASHBOARD
    wd = ws["Dashboard"]
    P = lambda col: f"Pedidos!${col}$3:${col}$3000"
    canais = sorted({p["canal"] or "(sem canal)" for p in pedidos})
    mods = sorted({modalidade(p) for p in pedidos})
    L = [["Painel de rentabilidade (Etapa 1)", "", "", "", ""],
         [f"Pedidos de {periodo} · importado em {agora}", "", "", "", ""],
         ["", "", "", "", ""],
         ["INDICADORES", "Valor", "", "", ""],
         ["Pedidos importados", f"=COUNTA({P('A')})", "", "", ""],
         ["Cancelados (fora do resultado)", f'=COUNTIF({P("F")},"Cancelado")', "", "", ""],
         ["Pedidos no resultado", "=B5-B6", "", "", ""],
         ["Receita dos pedidos no resultado", f'=SUMIFS({P("J")},{P("F")},"<>Cancelado")', "", "", ""],
         ["Ticket médio", '=IF(B7=0,0,B8/B7)', "", "", ""],
         ["Pedidos com dado completo", f'=COUNTIF({P("Z")},"Completo")', "", "", ""],
         ["Pedidos com dado incompleto", f'=COUNTIF({P("Z")},"Incompleto")', "", "", ""],
         ["Lucro (somente pedidos completos)", f'=IF(B10=0,"aguardando dados",SUM({P("X")}))', "", "", ""],
         ["Pedidos com prejuízo (completos)", f'=IF(B10=0,"aguardando dados",COUNTIF({P("X")},"<0"))', "", "", ""],
         ["", "", "", "", ""],
         ["POR CANAL", "Pedidos", "Cancelados", "Receita (sem cancelados)", "Completos"]]
    base_canal = len(L) + 1
    for i, c in enumerate(canais):
        r = base_canal + i
        L.append([c, f'=COUNTIF({P("D")},A{r})', f'=COUNTIFS({P("D")},A{r},{P("F")},"Cancelado")',
                  f'=SUMIFS({P("J")},{P("D")},A{r},{P("F")},"<>Cancelado")', f'=COUNTIFS({P("D")},A{r},{P("Z")},"Completo")'])
    L += [["", "", "", "", ""], ["POR MODALIDADE", "Pedidos", "Cancelados", "Receita (sem cancelados)", "Completos"]]
    base_mod = len(L) + 1
    for i, m in enumerate(mods):
        r = base_mod + i
        L.append([m, f'=COUNTIF({P("E")},A{r})', f'=COUNTIFS({P("E")},A{r},{P("F")},"Cancelado")',
                  f'=SUMIFS({P("J")},{P("E")},A{r},{P("F")},"<>Cancelado")', f'=COUNTIFS({P("E")},A{r},{P("Z")},"Completo")'])
    L += [["", "", "", "", ""],
          ["Enquanto comissão, tarifas, frete pago e custos adicionais não forem lançados, o lucro aparece como pendente. Isso é proposital: dado ausente nunca vira zero.", "", "", "", ""]]
    wd.update(range_name="A1", values=L, value_input_option="USER_ENTERED")
    sid = wd.id
    reqs += [req_fundo(sid, 0, 1, 0, 5, BRANCO, bold=True), req_fundo(sid, 3, 4, 0, 5, AZUL_BG, bold=True),
             req_fundo(sid, 14, 15, 0, 5, AZUL_BG, bold=True), req_fundo(sid, base_mod - 2, base_mod - 1, 0, 5, AZUL_BG, bold=True),
             req_numfmt(sid, 7, 9, 1, 2, "CURRENCY", "R$ #,##0.00"), req_numfmt(sid, 11, 12, 1, 2, "CURRENCY", "R$ #,##0.00"),
             req_numfmt(sid, 14, 80, 3, 4, "CURRENCY", "R$ #,##0.00"),
             req_largura(sid, 0, 1, 330), req_largura(sid, 1, 5, 150),
             {"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 1},
                             "cell": {"userEnteredFormat": {"textFormat": {"fontSize": 16, "bold": True}}}, "fields": "userEnteredFormat.textFormat"}}]

    # ============ LEIA-ME
    wr = ws["LEIA-ME"]
    txt = [
        ["ANÁLISE DE PEDIDOS · Etapa 1", ""],
        [f"Pedidos do Olist de {periodo}. Importado em {agora}.", ""],
        ["", ""],
        ["Objetivo", "Saber o lucro ou prejuízo real de cada pedido e, a partir disso, precificar com segurança."],
        ["Como ler", "Cada pedido é uma linha da aba Pedidos. As colunas estão agrupadas por origem do dado (faixa colorida no topo)."],
        ["", ""],
        ["CORES DAS ORIGENS", ""],
        ["Azul · Olist", "Pedido, itens, datas, situação e nota fiscal (somente leitura da API)."],
        ["Verde-água · XML da nota", "ICMS e tributos reais destacados na nota. Ainda a ligar."],
        ["Cinza · Custos próprios", "Custo do produto (fotografia do custo médio do Olist no dia da leitura) e custos adicionais cadastrados por você."],
        ["Amarelo · Marketplace", "Comissão, tarifa fixa, frete pago, fulfillment e reembolsos. Vêm dos relatórios dos marketplaces, lançados na aba Lançamentos."],
        ["Verde · Calculado", "Imposto estimado, custos indiretos, lucro, margem e situação do dado. Fórmulas, não edite."],
        ["", ""],
        ["STATUS DE CADA VALOR", ""],
        ["pendente", "O dado existe, mas ainda não chegou. Nunca é tratado como zero. O lucro só é calculado quando todos os valores aplicáveis estão preenchidos."],
        ["n/a", "A coluna não se aplica ao pedido (por exemplo, frete pago em fulfillment, ou qualquer custo em pedido cancelado)."],
        ["Completo / Incompleto", "Coluna Dado da aba Pedidos. Só pedidos Completos têm lucro."],
        ["Fora do resultado", "Pedido cancelado."],
        ["", ""],
        ["ABAS", ""],
        ["Dashboard", "Totais e quebra por canal e modalidade."],
        ["Pedidos", "Uma linha por pedido. Gerada pelo script, não digite aqui."],
        ["Itens", "Uma linha por SKU vendido, com a fotografia do custo. Gerada pelo script."],
        ["Produtos e Custos", "Cadastro por SKU: custo do Olist e seus custos adicionais (embalagem, caixa, fita, mão de obra). Preencha as colunas cinzas."],
        ["Lançamentos", "Cobranças e ajustes dos marketplaces, uma linha por valor (comissão, tarifa, frete, fulfillment, reembolso). Cole aqui os dados dos relatórios."],
        ["Fulfillment (lotes)", "Frete e preparação do envio de lotes aos centros, para ratear no custo dos produtos."],
        ["Custos indiretos", "Despesas gerais e critério de rateio."],
        ["Parâmetros", "Alíquota estimada (2,5% herdada da planilha manual, a validar com o contador), custo indireto por pedido e fonte dos dados de cada canal."],
        ["Logs", "Histórico das importações."],
        ["", ""],
        ["REGRAS", ""],
        ["Custo congelado", "O custo do produto é copiado para o item no dia da leitura. Mudar o custo no Olist depois não altera pedidos já importados."],
        ["Imposto", "É estimativa gerencial, não apuração fiscal. O ICMS real virá da nota."],
        ["Esta é a primeira versão", "Os pedidos foram lidos do Olist. Comissões, tarifas e custos adicionais ainda precisam ser lançados."],
    ]
    wr.update(range_name="A1", values=txt, value_input_option="USER_ENTERED")
    sid = wr.id
    reqs += [req_largura(sid, 0, 1, 250), req_largura(sid, 1, 2, 760),
             {"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 1},
                             "cell": {"userEnteredFormat": {"textFormat": {"fontSize": 16, "bold": True}}}, "fields": "userEnteredFormat.textFormat"}},
             {"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 60, "startColumnIndex": 1, "endColumnIndex": 2},
                             "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP"}}, "fields": "userEnteredFormat.wrapStrategy"}}]
    for i, linha in enumerate(txt):
        if linha[0] in ("CORES DAS ORIGENS", "STATUS DE CADA VALOR", "ABAS", "REGRAS"):
            reqs.append(req_fundo(sid, i, i + 1, 0, 2, CINZA_BG, bold=True))
    for i, (a, b, c) in enumerate([(7, AZUL_BG, 0), (8, TEAL_BG, 0), (9, CINZA_BG, 0), (10, AMBAR_BG, 0), (11, VERDE_BG, 0)]):
        reqs.append(req_fundo(sid, a, a + 1, 0, 1, b, bold=True))

    sh.batch_update({"requests": reqs})
    print(f"OK: {len(pedidos)} pedidos, {len(itens_linhas)} itens, {len(produtos)} produtos")


if __name__ == "__main__":
    main()
