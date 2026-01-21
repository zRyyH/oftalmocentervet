from .planilha import gerar_relatorio
from .vinculador import vincular


def executar_finpet_lancamentos(dados):
    finpet = dados.get("finpet", [])
    releases = dados.get("releases", [])

    resultado = vincular(finpet, releases)
    gerar_relatorio(resultado)

    return resultado
