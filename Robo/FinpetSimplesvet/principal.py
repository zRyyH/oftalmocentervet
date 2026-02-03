import sys
from pathlib import Path

# Adiciona a raiz ao path para importar planilha
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


def _preparar_item_para_planilha(item):
    """Prepara item adicionando metadados de formatação para a planilha genérica."""
    matches = item.get("matches", {})
    exact = item.get("exact_value", True)
    approximate = item.get("approximate_value", True)

    # Adiciona erros/avisos baseados nos matches
    item["_erros"] = {}

    # Parcela (coluna 6)
    if not matches.get("parcela", True):
        item["_erros"]["parcela_release"] = "erro"

    # Data (coluna 10)
    if not matches.get("data", True):
        item["_erros"]["data_release"] = "erro"

    # Valor Simplesvet (coluna 8) - lógica especial
    if not exact:
        if approximate:
            item["_erros"]["valor_release"] = "aviso"
        else:
            item["_erros"]["valor_release"] = "erro"

    return item


def gerar_relatorio(dados, caminho="Relatorios/Finpet Lancamentos.xlsx"):
    """Gera relatório usando a função genérica criar_planilha."""
    dados_agrupados = preparar_dados(dados)

    if not dados_agrupados:
        print("\nNenhum registro encontrado.")
        return

    # Prepara todos os itens para a planilha
    todos_dados = []
    for mes_ano in ordenar_meses(dados_agrupados.keys()):
        for item in dados_agrupados[mes_ano]:
            item_preparado = _preparar_item_para_planilha(item.copy())
            todos_dados.append(item_preparado)

    # Configuração para a planilha genérica
    config = {
        "coluna_data": "data_estimada",
        "colunas_moeda": [1, 7, 8],  # Valor Finpet, Valor Finpet 2, Valor Simplesvet
        "marcar_vazios": True,
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

    resultado = vincular(finpet, releases)
    gerar_relatorio(resultado)

    return resultado