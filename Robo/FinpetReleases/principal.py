import sys
from pathlib import Path

raiz = Path(__file__).parent.parent
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))

from planilha import criar_planilha
from .vinculador import vincular
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
    "Beneficiário",
    "Motivo Zerado",
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
    "beneficiario",
    "motivo_zerado",
]


def _preparar_item_para_planilha(item):
    matches = item.get("matches", {})
    exact = item.get("exact_value", True)
    approximate = item.get("approximate_value", True)

    item["_erros"] = {}

    if not matches.get("parcela", True):
        item["_erros"]["parcela_release"] = "erro"

    if not matches.get("data", True):
        item["_erros"]["data_release"] = "erro"

    if not exact:
        if approximate:
            item["_erros"]["valor_release"] = "aviso"
        else:
            item["_erros"]["valor_release"] = "erro"

    return item


def gerar_relatorio(dados, caminho="Relatorios/Finpet Lancamentos.xlsx"):
    dados_agrupados = preparar_dados(dados)

    if not dados_agrupados:
        print("⚠ Nenhum registro encontrado para gerar relatório")
        return

    todos_dados = []
    for mes_ano in ordenar_meses(dados_agrupados.keys()):
        for item in dados_agrupados[mes_ano]:
            item_preparado = _preparar_item_para_planilha(item.copy())
            todos_dados.append(item_preparado)

    config = {
        "coluna_data": "data_estimada",
        "colunas_moeda": [1, 7, 8],
        "marcar_vazios": True,
        "ignorar_vazios": [16],
    }

    criar_planilha(
        dados=todos_dados,
        arquivo=caminho,
        headers=HEADERS,
        campos=CAMPOS,
        config=config,
    )

    return caminho


def executar_finpet_lancamentos(dados):
    finpet = dados.get("finpet", [])
    releases = dados.get("releases", [])

    print(f"  Vinculando {len(finpet)} Finpet com {len(releases)} lançamentos...")
    resultado = vincular(finpet, releases)
    gerar_relatorio(resultado)

    return resultado
