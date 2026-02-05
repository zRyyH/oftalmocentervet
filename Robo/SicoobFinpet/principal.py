from planilha import criar_planilha
from .conciliador import conciliar
from .vinculador import vincular

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

CAMPOS = [
    "data_sicoob",
    "data_erp",
    "conciliado",
    "valor_sicoob",
    "valor_erp",
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
}


def _preparar_dados(resultado):
    dados = []
    for item in resultado:
        dados.append({
            **item,
            "conciliado": "SIM" if item.get("conciliado") else "NÃO",
        })
    return dados


def executar_sicoob_finpet(dados):
    sicoob = dados.get("sicoob", [])
    finpet = dados.get("finpet", [])
    brands = dados.get("brands", [])

    print(f"  Vinculando {len(sicoob)} registros Sicoob com {len(finpet)} Finpet...")
    vinculados = vincular(sicoob, finpet, brands)
    resultado = conciliar(vinculados)

    dados_planilha = _preparar_dados(resultado)
    criar_planilha(dados_planilha, "Relatorios/Sicoob Finpet.xlsx", HEADERS, CAMPOS, CONFIG)

    return resultado
