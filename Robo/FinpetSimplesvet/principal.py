from .relatorio import gerar_relatorio
from .vinculador import vincular
import json


def executar_finpet_lancamentos(dados: dict):
    finpet = dados.get("finpet", [])
    releases = dados.get("releases", [])

    resultados = vincular(finpet, releases)

    # with open("dados.json", "w") as FileW:
    #     FileW.write(json.dumps(dados, indent=4))

    # with open("resultados.json", "w") as FileW:
    #     FileW.write(json.dumps(resultados, indent=4))

    gerar_relatorio(resultados)
