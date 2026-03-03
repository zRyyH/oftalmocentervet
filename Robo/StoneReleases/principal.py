from .extract_data import extrair_dados
from .normalizers import normalizar_dados
from .vinculador import vincular
from .conciliador import conciliar
from planilha import criar_planilha

HEADERS = [
    "Conciliado",
    "Score",
    "Bandeira",
    "Produto",
    "Data Stone",
    "Data ERP",
    "Valor Stone (R$)",
    "Valor ERP (R$)",
    "Diferença (R$)",
    "Stonecode Stone",
    "Stonecode ERP",
    "Parcela Stone",
    "Parcela ERP",
    "Forma Pag. ERP",
    "Fornecedor ERP",
    "Descrição ERP",
]

CAMPOS = [
    "conciliado",
    "score",
    "bandeira",
    "produto",
    "data_stone",
    "data_erp",
    "valor_stone",
    "valor_erp",
    "diferenca",
    "stonecode_stone",
    "stonecode_erp",
    "parcela_stone",
    "parcela_erp",
    "forma_pagamento_erp",
    "fornecedor_erp",
    "descricao_erp",
]

# colunas (1-based):
# 1=conciliado, 2=score, 3=bandeira, 4=produto
# 5=data_stone, 6=data_erp, 7=valor_stone, 8=valor_erp, 9=diferenca
# 10=stonecode_stone, 11=stonecode_erp, 12=parcela_stone, 13=parcela_erp
# 14=forma_pagamento_erp, 15=fornecedor_erp, 16=descricao_erp

CONFIG = {
    "coluna_data": "data_stone",
    "colunas_status": [1],
    "colunas_moeda": [7, 8, 9],
    "colunas_soma": [7, 8, 9],
    "larguras": [16, 7, 16, 10, 12, 12, 16, 16, 14, 18, 18, 14, 14, 14, 25, 50],
    "resumo": {
        "titulo": "RESUMO GERAL",
        "cor_header": "verde",
        "linhas": [
            {
                "label": "Total de Registros:",
                "tipo": "total_registros",
                "cor": "verde",
            },
            {
                "label": "Conciliados:",
                "tipo": "contagem",
                "filtro": {"conciliado": "SIM"},
                "cor": "verde",
            },
            {
                "label": "Falha Crítica (STONECODE não encontrado):",
                "tipo": "contagem",
                "filtro": {"conciliado": "FALHA CRÍTICA"},
                "cor": "verde",
            },
            {
                "label": "Sem Stone (ERP sem extrato):",
                "tipo": "contagem",
                "filtro": {"conciliado": "SEM STONE"},
                "cor": "verde",
            },
        ],
    },
}

_COR_STATUS = {
    "SIM": None,           # zebra padrão
    "FALHA CRÍTICA": "nao",  # vermelho
    "SEM STONE": "devolucao",  # lilás
}


def _preparar_dados(resultado):
    dados_formatados = []
    for item in resultado:
        registro = item.copy()
        cor = _COR_STATUS.get(item.get("conciliado"))
        if cor:
            registro["_cor_linha"] = cor

        if item.get("conciliado") == "SIM":
            erros = {}

            if item.get("data_erp") != item.get("data_stone"):
                erros["data_erp"] = "erro"

            if round(abs((item.get("valor_erp") or 0) - (item.get("valor_stone") or 0)), 2) != 0:
                erros["valor_erp"] = "erro"

            if item.get("stonecode_erp") != item.get("stonecode_stone"):
                erros["stonecode_erp"] = "erro"

            parcela_s = str(item.get("parcela_stone") or "").strip().upper()
            parcela_e = str(item.get("parcela_erp") or "").strip().upper()
            if parcela_s != parcela_e:
                erros["parcela_erp"] = "erro"

            if erros:
                registro["_erros"] = erros

        dados_formatados.append(registro)
    return dados_formatados


def get_stone_releases_filters(caminho_stone="Stone/extrato.xlsx"):
    """Lê o extrato Stone e retorna filtro PocketBase para o mês do extrato."""
    dados_stone = extrair_dados(caminho_stone)

    from .normalizers import parse_date

    meses = {}
    for row in dados_stone:
        d = parse_date(row.get("DATA DE VENCIMENTO"))
        if d:
            mes = d[:7]  # "YYYY-MM"
            meses[mes] = meses.get(mes, 0) + 1

    if not meses:
        return {}

    mes_extrato = max(meses, key=meses.get)
    ano, mes = int(mes_extrato[:4]), int(mes_extrato[5:7])

    if mes == 12:
        ano_fim, mes_fim = ano + 1, 1
    else:
        ano_fim, mes_fim = ano, mes + 1

    inicio = f"{ano}-{mes:02d}-01 00:00:00"
    fim = f"{ano_fim}-{mes_fim:02d}-01 00:00:00"

    filter_str = f"vencimento >= '{inicio}' && vencimento < '{fim}'"
    print(f"  Filtro releases: {filter_str}")
    return {"releases": filter_str}


def executar_stone_releases(dados, caminho_stone="Stone/extrato.xlsx"):
    print(f"  Extraindo dados de {caminho_stone}...")
    dados["stone"] = extrair_dados(caminho_stone)

    print("  Normalizando dados...")
    norm = normalizar_dados(dados)

    print(
        f"  Vinculando {len(norm['stone'])} registros Stone com {len(norm['releases'])} lançamentos ERP..."
    )
    vinculados = vincular(norm["stone"], norm["releases"], norm["brands"])

    resultado = conciliar(vinculados)

    conciliados = sum(1 for r in resultado if r["conciliado"] == "SIM")
    falha = sum(1 for r in resultado if r["conciliado"] == "FALHA CRÍTICA")
    sem_stone = sum(1 for r in resultado if r["conciliado"] == "SEM STONE")
    print(f"  Resultado: {conciliados} SIM | {falha} FALHA CRÍTICA | {sem_stone} SEM STONE")

    dados_formatados = _preparar_dados(resultado)
    criar_planilha(dados_formatados, "Relatorios/Stone Releases.xlsx", HEADERS, CAMPOS, CONFIG)

    return resultado
