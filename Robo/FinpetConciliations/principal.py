from .planilha import criar_planilha
from .conciliador import conciliar
import json


def executar_finpet_conciliacoes(dados: dict):
    finpet = dados.get("finpet", [])
    conciliations = dados.get("conciliations", [])
    brands = dados.get("brands", [])

    resultado = conciliar(finpet, conciliations, brands)

    # with open("resultados_finpet_conciliacao.json", "w", encoding="utf-8") as f:
    #     json.dump(resultado, f, ensure_ascii=False, indent=2)

    # with open("dados_finpet_conciliacao.json", "w", encoding="utf-8") as f:
    #     json.dump(dados, f, ensure_ascii=False, indent=2)

    criar_planilha(resultado)

    return resultado