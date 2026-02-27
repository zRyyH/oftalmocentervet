import openpyxl


def extrair_dados(caminho_arquivo):
    wb = openpyxl.load_workbook(caminho_arquivo, data_only=True)
    ws = wb.active

    linhas = list(ws.iter_rows(values_only=True))
    cabecalho = linhas[0]
    dados = linhas[1:]

    def limpar_valor(v):
        if isinstance(v, (list, tuple)):
            return str(v)
        return v

    return [{k: limpar_valor(v) for k, v in zip(cabecalho, linha)} for linha in dados]
