from datetime import datetime
from utils import parse_data, formatar_data as formatar_data_util


def valores_iguais(valor1: float, valor2: float, tolerancia: float = 0.01) -> bool:
    return abs(abs(valor1) - abs(valor2)) <= tolerancia


def datas_correspondem(data1: datetime, data2: datetime) -> bool:
    return data1.day == data2.day and data1.month == data2.month


def criar_mapeamento_payments(payments: list) -> dict:
    """Cria dicionário de mapeamento sicoob_payment -> simplesvet_payment."""
    return {p.get("sicoob_payment"): p.get("simplesvet_payment") for p in payments}


def encontrar_correspondente(debito: dict, releases: list) -> dict | None:
    valor_sicoob = abs(debito.get("valor", 0))
    data_sicoob = parse_data(debito.get("data"))

    if not data_sicoob:
        return None

    for release in releases:
        if not valores_iguais(release.get("valor", 0), valor_sicoob):
            continue
        data_release = parse_data(release.get("data"))
        if data_release and datas_correspondem(data_sicoob, data_release):
            return release
    return None


def eh_estorno(registro: dict) -> bool:
    """Verifica se o registro é um estorno."""
    descricao = (registro.get("descricao") or "").upper()
    desc_complementar = (registro.get("desc_inf_complementar") or "").upper()
    return "ESTORNO" in descricao or "ESTORNO" in desc_complementar


def filtrar_debitos(sicoob: list) -> list:
    resultado = []
    for s in sicoob:
        # Inclui DEBITOS normais
        if s.get("tipo", "").upper() == "DEBITO":
            resultado.append(s)
            continue
        # Inclui registros com ESTORNO na descrição, independente do tipo
        if eh_estorno(s):
            resultado.append(s)
    return resultado


def filtrar_despesas(releases: list) -> list:
    return [
        r
        for r in releases
        if r.get("tipo") == "despesa" and r.get("forma_pagamento") != "CRE"
    ]


def datas_proximas(data1: datetime, data2: datetime, dias_tolerancia: int = 1) -> bool:
    """Verifica se duas datas estão dentro de um período de tolerância em dias."""
    if not data1 or not data2:
        return False
    diferenca = abs((data1 - data2).days)
    return diferenca <= dias_tolerancia


def vincular_estornos(debitos: list) -> dict:
    """
    Vincula estornos com pagamentos refeitos pelo valor e proximidade de data.
    Um estorno é vinculado a um pagamento se:
    - Os valores são iguais
    - A diferença de datas é de até 1 dia
    Retorna um dicionário com informações sobre vinculações.
    """
    estornos = []
    pagamentos = []

    # Separar estornos de pagamentos normais
    for d in debitos:
        if eh_estorno(d):
            estornos.append(d)
        else:
            pagamentos.append(d)

    vinculacoes = {}  # {id_estorno: id_pagamento}
    estornos_vinculados = set()
    pagamentos_vinculados = set()

    # Para cada estorno, encontrar um pagamento correspondente (mesmo valor, data próxima)
    for estorno in estornos:
        valor_estorno = abs(estorno.get("valor", 0))
        data_estorno = parse_data(estorno.get("data"))
        id_estorno = id(estorno)

        # Procurar pagamento com mesmo valor e data próxima (até 1 dia de diferença)
        for pagamento in pagamentos:
            id_pagamento = id(pagamento)
            if id_pagamento in pagamentos_vinculados:
                continue

            valor_pagamento = abs(pagamento.get("valor", 0))
            data_pagamento = parse_data(pagamento.get("data"))

            if valores_iguais(valor_estorno, valor_pagamento) and datas_proximas(data_estorno, data_pagamento):
                vinculacoes[id_estorno] = id_pagamento
                estornos_vinculados.add(id_estorno)
                pagamentos_vinculados.add(id_pagamento)
                break  # Um estorno só vincula com um pagamento

    return {
        "vinculacoes": vinculacoes,
        "estornos_vinculados": estornos_vinculados,
        "pagamentos_vinculados": pagamentos_vinculados,
    }


def criar_item_conciliado(debito: dict, match: dict | None, mapeamento: dict) -> dict:
    descricao_sicoob = debito.get("descricao", "")
    tipo_pag_sicoob = mapeamento.get(descricao_sicoob, "OUTRO")
    forma_pag_erp = match.get("forma_pagamento") if match else None

    forma_confere = None
    if match and forma_pag_erp:
        forma_confere = tipo_pag_sicoob == forma_pag_erp

    # Se encontrou match mas a forma de pagamento não confere, considera não conciliado
    conciliado = match is not None and (forma_confere is None or forma_confere is True)

    return {
        "data_sicoob": formatar_data_util(debito.get("data", "")),
        "valor_sicoob": debito.get("valor", 0),
        "descricao_sicoob": descricao_sicoob,
        "info_complementar": debito.get("desc_inf_complementar", ""),
        "tipo_pag_sicoob": tipo_pag_sicoob,
        "conciliado": conciliado,
        "data_erp": formatar_data_util(match.get("data", "")) if match else None,
        "valor_erp": abs(match.get("valor", 0)) if match else None,
        "descricao_erp": match.get("descricao") if match else None,
        "fornecedor_erp": match.get("fornecedor") if match else None,
        "forma_pagamento_erp": forma_pag_erp,
        "forma_confere": forma_confere,
    }


def conciliar(dados: dict) -> dict:
    debitos = filtrar_debitos(dados.get("sicoob", []))
    despesas = filtrar_despesas(dados.get("releases", []))
    mapeamento = criar_mapeamento_payments(dados.get("payments", []))

    # Vincular estornos com pagamentos
    info_estornos = vincular_estornos(debitos)

    usados = set()
    itens = []

    for debito in debitos:
        id_debito = id(debito)
        is_estorno = eh_estorno(debito)
        estorno_vinculado = id_debito in info_estornos["estornos_vinculados"]
        pagamento_vinculado = id_debito in info_estornos["pagamentos_vinculados"]

        # Se é estorno vinculado ou pagamento vinculado, não conciliar com ERP
        if estorno_vinculado or pagamento_vinculado:
            item = criar_item_conciliado(debito, None, mapeamento)
            item["estorno_vinculado"] = True
            itens.append(item)
            continue

        # Se é estorno sem vinculação, marcar como estorno sem par
        if is_estorno:
            item = criar_item_conciliado(debito, None, mapeamento)
            item["estorno_sem_par"] = True
            itens.append(item)
            continue

        # Pagamento normal - tentar conciliar com ERP
        disponiveis = [r for r in despesas if r.get("id") not in usados]
        match = encontrar_correspondente(debito, disponiveis)

        if match:
            usados.add(match.get("id"))

        itens.append(criar_item_conciliado(debito, match, mapeamento))

    conciliados = [i for i in itens if i["conciliado"]]
    formas_ok = sum(1 for i in conciliados if i["forma_confere"] is True)
    formas_erro = sum(1 for i in conciliados if i["forma_confere"] is False)

    return {
        "itens": itens,
        "total": len(itens),
        "conciliados": len(conciliados),
        "formas_conferem": formas_ok,
        "formas_divergentes": formas_erro,
    }
