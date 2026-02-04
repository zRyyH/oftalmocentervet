from .normalizers import normalizar_dados
from .extract_data import extrair_dados
from .conciliador import conciliar
from .vinculador import vincular
from planilha import criar_planilha

HEADERS = [
    "Data Sicoob",
    "Data Stone",
    "Conciliado",
    "Valor Sicoob (R$)",
    "Valor Stone (R$)",
    "Descrição Sicoob",
    "Info Complementar",
    "Bandeira",
]

CAMPOS = [
    "data_sicoob",
    "data_stone",
    "conciliado",
    "valor_sicoob",
    "valor_stone",
    "descricao_sicoob",
    "info_complementar",
    "bandeira",
]

CONFIG = {
    "coluna_data": "data_sicoob",
    "colunas_status": [3],
    "colunas_moeda": [4, 5],
    "colunas_soma": [4, 5],
    "larguras": [12, 12, 12, 16, 18, 35, 50, 18],
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
                "label": "Registros Stone Link De Pagamento:",
                "tipo": "quantidade",
                "campo": "qtd_especiais",
                "cor": "verde",
            },
            {
                "label": "Valor Total Stone Link De Pagamento:",
                "tipo": "soma",
                "campo": "valor_especiais",
                "cor": "verde",
            },
        ],
    },
}


def _preparar_dados(resultado):
    dados_formatados = []
    for item in resultado:
        registro = item.copy()
        registro["conciliado"] = "SIM" if item.get("conciliado") else "NÃO"
        dados_formatados.append(registro)
    return dados_formatados


def executar_sicoob_stone(dados, caminho_stone="Stone/extrato.xlsx"):
    dados["stone"] = extrair_dados(caminho_stone)

    norm = normalizar_dados(dados)

    vinculados = vincular(norm["sicoob"], norm["stone"], norm["brands"])
    resultado = conciliar(vinculados)

    dados_formatados = _preparar_dados(resultado)
    criar_planilha(dados_formatados, "Relatorios/Sicoob Stone.xlsx", HEADERS, CAMPOS, CONFIG)

    return resultado