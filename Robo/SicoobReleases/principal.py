from .planilha import criar_planilha
from .conciliador import conciliar


def executar_sicoob_releases(dados):
    dados_brutos = conciliar(dados)
    resultado = dados_brutos.get("itens", [])

    if resultado:
        criar_planilha(resultado, "Relatorios/Sicoob Lançamentos.xlsx")

    return resultado