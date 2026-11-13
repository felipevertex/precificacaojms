# Operação: onde as coisas rodam e como conferir

Registro de 2026-11-13. Sem credenciais neste arquivo.

## Arquitetura dividida (de propósito)
| Peça | Onde | Por quê |
|---|---|---|
| Token do Olist | `.env` local e `/opt/precificacao/olist.env` na VPS (modo 600, só root) | Acesso total à conta do Olist |
| Chave da conta de serviço do Google | Só na VPS, no `secrets.toml` do jmsecom (seção `google_service_account`) | Nunca sai do servidor |
| Scripts em produção | `/opt/precificacao/scripts/` na VPS (cópia de `scripts/` do repositório) | Rodam no cron |
| Planilha | Google Sheets, compartilhada com a conta de serviço | Interface |

A VPS é a mesma do jmsecom (Vertex). O Python usado é o do venv do jmsecom: `/opt/jmsecom/app/venv/bin/python`.

## O cron (instalado em 2026-11-13, autorizado pelo Felipe)
- No crontab do **root**. Frequência: `*/30 11-23,0-2 * * *` (UTC), ou seja **a cada 30 minutos, das 07h às 22h de Cuiabá**.
- Usa `flock -n /tmp/precificacao.lock` para não sobrepor execuções.
- Variáveis: `DIAS=30` (janela relida para mudança de situação), `DIAS_NOVOS=7` (só pedidos dos últimos 7 dias entram como novos), `SECRETS_PATH`, `SHEET_ID`, `OLIST_ENV`.
- Log do processo: `/var/log/precificacao.log`. Cada execução também grava uma linha na aba **Logs** da planilha (erros também).
- Backup do crontab de antes da mudança: `/root/crontab.bak-2026-11-13`.
- Os outros agendamentos já existentes (rastreio, régua de cobrança, mensalidades, alerta do Royal) não foram tocados.

## Conferir se está rodando
```bash
ssh root@<IP-da-VPS> "tail -n 30 /var/log/precificacao.log; crontab -l | grep precificacao"
```
E na planilha: aba **Logs**, uma linha nova a cada 30 minutos dentro da janela. A primeira rodada automática **ainda não foi observada** na data deste registro: só a execução manual foi testada.

## Rodar na mão
```bash
ssh root@<IP-da-VPS>
env DIAS=30 DIAS_NOVOS=7 SECRETS_PATH=/opt/jmsecom/app/.streamlit/secrets.toml SHEET_ID=<id-da-planilha> OLIST_ENV=/opt/precificacao/olist.env /opt/jmsecom/app/venv/bin/python /opt/precificacao/scripts/importar_pedidos.py
```
O ID da planilha está em `SHEET_ID_ANALISE_PEDIDOS` no `.env` local e em `docs/07-planilha-etapa1.md`.

## Desligar
Editar o crontab do root e remover a linha que contém `importar_pedidos.py`. Para voltar ao estado anterior: `crontab /root/crontab.bak-2026-11-13`.

## Atualizar os scripts na VPS
Depois de mudar `scripts/` no repositório, copiar para `/opt/precificacao/scripts/` (hoje é manual, via `scp`). Se mudar coluna ou fórmula, a mudança é **sempre em `scripts/regras.py`** (fonte única das linhas de Pedidos, Itens e Produtos e Custos), usada tanto por `montar_planilha.py` quanto por `importar_pedidos.py`.

## Rodar a planilha do zero (cuidado)
`montar_planilha.py --reset` reconstrói as abas e **apaga o que foi lançado à mão** (Lançamentos, Produtos e Custos, Parâmetros). Usar só com o Felipe ciente.

## Limites e armadilhas já encontrados
- **API 2.0 do Olist:** limite de chamadas. O cliente (`scripts/olist.py`) espera ~2,3 s entre chamadas e, se vier "Excedido/Bloqueada", espera 70 s e tenta de novo.
- **Google Sheets:** cota de ~60 leituras por minuto. Evitar muitas leituras seguidas.
- **Locale pt_BR** da planilha: fórmulas gravadas pela API precisam de `;` entre argumentos. `scripts/sheets_util.py` converte a vírgula automaticamente.
- **Colunas congeladas** não podem cortar células mescladas (por isso os grupos de cores não usam mesclagem).
- Todas as abas têm 3000 linhas × 30 colunas. Passar disso exige ampliar a grade.

## Segurança
- O token do Olist deve ser **trocado** (apareceu no chat). Atualizar os dois `olist.env`/`.env`.
- O Streamlit do jmsecom roda como root nessa VPS. Um token ali tem exposição maior do que numa máquina isolada. Se a Etapa 2 crescer, considerar usuário dedicado.
