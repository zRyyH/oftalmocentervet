from .cartao_credito import obter_faturas_cartao
from .planilha import gerar_planilha_sicoob


def executar_sicoob_fatura(dados):
    print("  Processando faturas de cartão de crédito...")
    resultado = obter_faturas_cartao(dados)

    gerar_planilha_sicoob(resultado)

    return resultado
