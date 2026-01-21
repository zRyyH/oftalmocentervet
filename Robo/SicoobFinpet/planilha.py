from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from datetime import datetime
from collections import defaultdict


HEADERS = [
    "Data Sicoob",
    "Data Simplesvet",
    "Conciliado",
    "Valor Sicoob (R$)",
    "Valor Simplesvet (R$)",
    "Descrição Sicoob",
    "Info Complementar",
    "Bandeira",
]

LARGURAS = [12, 12, 12, 16, 18, 35, 50, 18]


def criar_estilos() -> dict:
    borda = Side(style="thin", color="808080")
    return {
        "header_font": Font(bold=True, color="000000", size=11),
        "header_fill": PatternFill("solid", fgColor="90EE90"),
        "cell_font": Font(size=10),
        "cell_font_erro": Font(size=10, color="CC0000"),
        "alt_fill": PatternFill("solid", fgColor="E8F5E9"),
        "borda": Border(left=borda, right=borda, top=borda, bottom=borda),
        "centro": Alignment(horizontal="center", vertical="center"),
        "sim_fill": PatternFill("solid", fgColor="C6EFCE"),
        "nao_fill": PatternFill("solid", fgColor="FFC7CE"),
        "vazio_fill": PatternFill("solid", fgColor="FFCCCC"),
    }


def aplicar_header(ws, estilos: dict):
    for col, nome in enumerate(HEADERS, 1):
        celula = ws.cell(row=1, column=col, value=nome)
        celula.font = estilos["header_font"]
        celula.fill = estilos["header_fill"]
        celula.alignment = estilos["centro"]
        celula.border = estilos["borda"]


def aplicar_linha(ws, linha: int, estilos: dict, conciliado: bool, zebra: bool = False):
    for col in range(1, len(HEADERS) + 1):
        celula = ws.cell(row=linha, column=col)
        celula.border = estilos["borda"]
        celula.alignment = estilos["centro"]

        valor = celula.value
        is_vazio = valor is None or valor == ""

        if is_vazio:
            celula.fill = estilos["vazio_fill"]
            celula.font = estilos["cell_font"]
        elif col == 3:
            celula.fill = estilos["sim_fill"] if conciliado else estilos["nao_fill"]
            celula.font = (
                estilos["cell_font"] if conciliado else estilos["cell_font_erro"]
            )
        else:
            celula.font = (
                estilos["cell_font"] if conciliado else estilos["cell_font_erro"]
            )
            if zebra:
                celula.fill = estilos["alt_fill"]


def aplicar_larguras(ws):
    for col, largura in enumerate(LARGURAS, 1):
        ws.column_dimensions[get_column_letter(col)].width = largura


def extrair_valores(item: dict) -> list:
    return [
        item.get("data_sicoob") or "",
        item.get("data_erp") or "",
        "SIM" if item.get("conciliado") else "NÃO",
        item.get("valor_sicoob") or 0,
        item.get("valor_erp") or 0,
        item.get("descricao_sicoob") or "",
        item.get("info_complementar") or "",
        item.get("bandeira") or "",
    ]


def parse_data(valor: str) -> datetime | None:
    if not valor:
        return None
    for fmt in ["%Y-%m-%d", "%d/%m/%Y"]:
        try:
            return datetime.strptime(valor, fmt)
        except ValueError:
            continue
    return None


def agrupar_por_mes(itens: list) -> dict:
    grupos = defaultdict(list)
    for item in itens:
        data = parse_data(item.get("data_sicoob", ""))
        if data:
            chave = f"{data.month:02d}-{data.year}"
            grupos[chave].append(item)
    return grupos


def ordenar_por_data(itens: list) -> list:
    return sorted(
        itens,
        key=lambda x: parse_data(x.get("data_sicoob", "")) or datetime.min,
        reverse=True,
    )


def ordenar_chaves_mes(chaves: list) -> list:
    def parse_chave(chave):
        mes, ano = chave.split("-")
        return (int(ano), int(mes))

    return sorted(chaves, key=parse_chave)


def criar_folha(wb, nome: str, itens: list, estilos: dict):
    ws = wb.create_sheet(title=nome)

    aplicar_header(ws, estilos)

    itens_ordenados = ordenar_por_data(itens)

    for i, item in enumerate(itens_ordenados, 2):
        valores = extrair_valores(item)
        for col, valor in enumerate(valores, 1):
            ws.cell(row=i, column=col, value=valor)
        aplicar_linha(ws, i, estilos, item.get("conciliado", False), zebra=(i % 2 == 0))

    aplicar_larguras(ws)
    ws.freeze_panes = "A2"

    if itens_ordenados:
        ultima_linha = len(itens_ordenados) + 1
        ultima_coluna = get_column_letter(len(HEADERS))
        ws.auto_filter.ref = f"A1:{ultima_coluna}{ultima_linha}"


def criar_planilha(itens: list, caminho: str) -> str:
    wb = Workbook()
    estilos = criar_estilos()

    grupos = agrupar_por_mes(itens)
    chaves_ordenadas = ordenar_chaves_mes(list(grupos.keys()))

    for chave in chaves_ordenadas:
        criar_folha(wb, chave, grupos[chave], estilos)

    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

    wb.save(caminho)
    return caminho


def filtrar_periodo(itens: list, mes: int, ano: int) -> list:
    resultado = []
    for item in itens:
        data = parse_data(item.get("data_sicoob", ""))
        if data and data.month == mes and data.year == ano:
            resultado.append(item)
    return resultado


def gerar_relatorio(dados: dict, mes: int, ano: int) -> str | None:
    itens = filtrar_periodo(dados.get("itens", []), mes, ano)
    if not itens:
        return None
    itens = ordenar_por_data(itens)
    caminho = f"sicoob_lancamento_{mes:02d}_{ano}.xlsx"
    return criar_planilha(itens, caminho)
