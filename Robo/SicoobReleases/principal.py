from .planilha import criar_planilha
from .conciliador import conciliar
import json


def executar_sicoob_releases(
    dados: dict, caminho: str = "sicoob_lancamentos.xlsx"
) -> dict:
    resultado = conciliar(dados)
    itens = resultado.get("itens", [])

    if itens:
        criar_planilha(itens, caminho)

    # with open("dados_sicoob_lancamentos.json", "w") as FileW:
    #     FileW.write(json.dumps(dados, indent=4))

    # with open("resultados_sicoob_lancamentos.json", "w") as FileW:
    #     FileW.write(json.dumps(resultado, indent=4))

    return resultado
