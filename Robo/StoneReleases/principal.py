from .extract_data import extrair_dados
from .normalizers import normalizar_dados
from .vinculador import vincular
from .conciliador import conciliar
from planilha import criar_planilha

HEADERS = [
    "Conciliado",
    "Data Stone",
    "Bandeira",
    "Produto",
    "Valor Stone (R$)",
    "Data ERP",
    "Fornecedor ERP",
    "Parcela ERP",
    "Forma Pag. ERP",
    "Valor ERP (R$)",
    "Diferença (R$)",
    "Descrição ERP",
]

CAMPOS = [
    "conciliado",
    "data_stone",
    "bandeira",
    "produto",
    "valor_stone",
    "data_erp",
    "fornecedor_erp",
    "parcela_erp",
    "forma_pagamento_erp",
    "valor_erp",
    "diferenca",
    "descricao_erp",
]

# colunas (1-based):
# 1=conciliado, 2=data_stone, 3=bandeira, 4=produto
# 5=valor_stone, 6=data_erp, 7=fornecedor_erp, 8=parcela_erp
# 9=forma_pagamento_erp, 10=valor_erp, 11=diferenca, 12=descricao_erp

CONFIG = {
    "coluna_data": "data_stone",
    "colunas_status": [1],
    "colunas_moeda": [5, 10, 11],
    "colunas_soma": [5, 10, 11],
    "larguras": [12, 12, 16, 10, 16, 12, 30, 12, 12, 16, 14, 50],
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
                "label": "Não Conciliados (valor divergente):",
                "tipo": "contagem",
                "filtro": {"conciliado": "NÃO"},
                "cor": "verde",
            },
            {
                "label": "Sem ERP (Stone sem lançamento):",
                "tipo": "contagem",
                "filtro": {"conciliado": "SEM ERP"},
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
    "SIM": None,           # usa zebra padrão (verde já vem de colunas_status)
    "NÃO": "nao",
    "SEM ERP": "estorno",  # laranja
    "SEM STONE": "devolucao",  # lilás
}


def _preparar_dados(resultado):
    dados_formatados = []
    for item in resultado:
        registro = item.copy()
        cor = _COR_STATUS.get(item.get("conciliado"))
        if cor:
            registro["_cor_linha"] = cor
        # Erro de valor: destacar colunas valor_erp e diferenca em vermelho
        if item.get("conciliado") == "NÃO":
            registro["_erros"] = {
                "valor_erp": "erro",
                "diferenca": "erro",
            }
        dados_formatados.append(registro)
    return dados_formatados


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
    sem_erp = sum(1 for r in resultado if r["conciliado"] == "SEM ERP")
    sem_stone = sum(1 for r in resultado if r["conciliado"] == "SEM STONE")
    nao = sum(1 for r in resultado if r["conciliado"] == "NÃO")
    print(f"  Resultado: {conciliados} SIM | {nao} NÃO | {sem_erp} SEM ERP | {sem_stone} SEM STONE")

    dados_formatados = _preparar_dados(resultado)
    criar_planilha(dados_formatados, "Relatorios/Stone Releases.xlsx", HEADERS, CAMPOS, CONFIG)

    return resultado
