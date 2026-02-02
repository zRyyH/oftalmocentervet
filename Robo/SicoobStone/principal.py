from .normalizers import normalizar_dados
from .extract_data import extrair_dados
from .planilha import criar_planilha
from .conciliador import conciliar
from .vinculador import vincular


def executar_sicoob_stone(dados, caminho_stone="Stone/extrato.xlsx"):
    dados["stone"] = extrair_dados(caminho_stone)

    norm = normalizar_dados(dados)

    vinculados = vincular(norm["sicoob"], norm["stone"], norm["brands"])
    resultado = conciliar(vinculados)

    criar_planilha(resultado, "Relatorios/Sicoob Stone.xlsx")

    return resultado