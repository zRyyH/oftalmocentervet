from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill, Border, Side, Font
from openpyxl.utils import get_column_letter
from .formatador import preparar_dados, ordenar_meses


HEADERS = [
    "Valor Finpet",
    "Data Estimada",
    "Bandeira",
    "Score",
    "Parcela Finpet",
    "Parcela Simplesvet",
    "Valor Finpet",
    "Valor Simplesvet",
    "Data Finpet",
    "Data Simplesvet",
    "Auth Finpet",
    "Auth Simplesvet",
    "Pedidos Extraidos",
    "Cliente Lancamento",
]

CAMPOS = [
    "valor_finpet",
    "data_estimada",
    "bandeira",
    "score",
    "parcela_finpet",
    "parcela_release",
    "valor_finpet_2",
    "valor_release",
    "data_finpet",
    "data_release",
    "auth_finpet",
    "auth_release",
    "pedidos",
    "cliente_release",
]

# Colunas que verificam match (índice 1-based)
COLUNAS_MATCH = {6: "parcela", 10: "data"}

# Estilos
HEADER_FILL = PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")
ROW_FILL = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")
VAZIO_FILL = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
FONTE_VERMELHA = Font(color="CC0000", bold=True)
BORDA = Border(
    left=Side(style="thin", color="808080"),
    right=Side(style="thin", color="808080"),
    top=Side(style="thin", color="808080"),
    bottom=Side(style="thin", color="808080"),
)
CENTRO = Alignment(horizontal="center", vertical="center")


def _adicionar_linha(ws, item):
    linha = [item.get(campo) for campo in CAMPOS]
    ws.append(linha)

    row_idx = ws.max_row
    matches = item.get("matches", {})

    for col_idx, match_key in COLUNAS_MATCH.items():
        if not matches.get(match_key, True):
            ws.cell(row=row_idx, column=col_idx).font = FONTE_VERMELHA

    # Valor Simplesvet vermelho quando exact_value é False
    if not item.get("exact_value", True):
        ws.cell(row=row_idx, column=8).font = FONTE_VERMELHA

    for col_idx, valor in enumerate(linha, 1):
        if valor is None or valor == "":
            ws.cell(row=row_idx, column=col_idx).fill = VAZIO_FILL


def _aplicar_estilos(ws):
    for cell in ws[1]:
        cell.fill = HEADER_FILL

    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        if row_idx % 2 == 0:
            for cell in row:
                if not cell.fill.start_color.rgb.endswith("FFCCCC"):
                    cell.fill = ROW_FILL

    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = CENTRO
            cell.border = BORDA

    for col_idx, col in enumerate(ws.columns, 1):
        max_len = max((len(str(c.value or "")) for c in col), default=0)
        ws.column_dimensions[get_column_letter(col_idx)].width = max_len + 2

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def _criar_aba(wb, nome, linhas):
    ws = wb.create_sheet(title=nome.replace("/", "-"))
    ws.append(HEADERS)

    for item in linhas:
        _adicionar_linha(ws, item)

    _aplicar_estilos(ws)


def gerar_relatorio(dados, caminho="Relatorios/Finpet Lancamentos.xlsx"):
    dados_agrupados = preparar_dados(dados)

    if not dados_agrupados:
        print("\nNenhum registro encontrado.")
        return

    wb = Workbook()
    wb.remove(wb.active)

    for mes_ano in ordenar_meses(dados_agrupados.keys()):
        _criar_aba(wb, mes_ano, dados_agrupados[mes_ano])

    wb.save(caminho)
    return caminho