"""Conexao com o Google Sheets pela conta de servico (chave lida de um secrets.toml, nunca versionado).

A planilha usa locale pt_BR: formulas gravadas pela API precisam de ";" como separador de argumentos.
"""
import os
import tomllib

import gspread
from google.oauth2.service_account import Credentials

_update_original = gspread.Worksheet.update


def _converter(valores):
    return [[(c.replace(",", ";") if isinstance(c, str) and c.startswith("=") else c) for c in linha] for linha in valores]


def _update(self, *args, **kwargs):
    if kwargs.get("values") is not None:
        kwargs["values"] = _converter(kwargs["values"])
    return _update_original(self, *args, **kwargs)


gspread.Worksheet.update = _update


def conectar(secrets_path=None):
    s = dict(tomllib.load(open(secrets_path or os.environ["SECRETS_PATH"], "rb"))["google_service_account"])
    s["private_key"] = s["private_key"].replace("\\n", "\n")
    c = Credentials.from_service_account_info(
        s, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.readonly"])
    return gspread.authorize(c)
