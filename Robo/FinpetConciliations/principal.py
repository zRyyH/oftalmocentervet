from planilha import criar_planilha
from .conciliador import conciliar

HEADERS = [
    "Data",
    "Bandeira",
    "Tipo",
    "Valor ERP",
    "Valor Finpet",
    "Diferença",
    "Taxa Bandeira",
    "Taxa Aluguel",
    "Descrição",
    "Trans. Finpet",
    "Conciliado ERP",
    "Bateu",
]

CAMPOS = [
    "data",
    "bandeira",
    "tipo",
    "valor_erp",
    "valor_finpet",
    "diferenca",
    "taxa_bandeira",
    "taxa_aluguel",
    "descricao",
    "transacoes_finpet",
    "conciliado_erp",
    "bateu",
]

CONFIG = {
    "coluna_data": "data",
    "colunas_status": [11, 12],
    "colunas_moeda": [4, 5, 6, 7, 8],
    "colunas_soma": [4, 5],
    "marcar_vazios": True,
    "larguras": [12, 15, 10, 14, 14, 12, 12, 12, 20, 12, 12, 10],
}


def executar_finpet_conciliacoes(dados, caminho="Relatorios/Finpet Conciliações.xlsx"):
    finpet = dados.get("finpet", [])
    conciliations = dados.get("conciliations", [])
    brands = dados.get("brands", [])

    print(f"  Conciliando {len(finpet)} Finpet com {len(conciliations)} ERP...")
    resultado = conciliar(finpet, conciliations, brands)

    criar_planilha(resultado, caminho, headers=HEADERS, campos=CAMPOS, config=CONFIG)

    return resultado
