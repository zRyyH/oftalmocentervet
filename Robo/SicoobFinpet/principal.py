from .planilha import criar_planilha
from .conciliador import conciliar
from .vinculador import vincular
import json


def executar_sicoob_finpet(dados: dict, caminho: str = "sicoob_finpet.xlsx") -> list:
    sicoob = dados.get("sicoob", [])
    finpet = dados.get("finpet", [])
    brands = dados.get("brands", [])

    vinculados = vincular(sicoob, finpet, brands)
    conciliacoes = conciliar(vinculados)
    criar_planilha(conciliacoes, caminho)

    # with open("dados_sicoob_finpet.json", "w") as FileW:
    #     FileW.write(json.dumps(dados, indent=4))

    # with open("resultados_sicoob_finpet.json", "w") as FileW:
    #     FileW.write(json.dumps(conciliacoes, indent=4))

    return conciliacoes
