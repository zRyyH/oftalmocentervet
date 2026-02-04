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


def criar_mapeamento_devolucoes(returns: list) -> list[dict]:
    """
    Retorna lista de dicts com description_return e description_payment.
    Usado para identificar devoluções e vinculá-las aos pagamentos.
    """
    return [
        {"description_return": r.get("description_return"), "description_payment": r.get("description_payment")}
        for r in returns
        if r.get("description_return")
    ]


def eh_devolucao(registro: dict, mapeamento_devolucoes: list) -> tuple[bool, str | None]:
    """
    Verifica se o registro é uma devolução comparando desc_inf_complementar
    com description_return do mapeamento.
    Retorna (is_devolucao, description_payment_vinculado).
    """
    desc_complementar = registro.get("desc_inf_complementar") or ""
    for item in mapeamento_devolucoes:
        description_return = item.get("description_return")
        if description_return and description_return in desc_complementar:
            return True, item.get("description_payment")
    return False, None


def eh_pagamento_com_devolucao(registro: dict, mapeamento_devolucoes: list) -> tuple[bool, str | None]:
    """
    Verifica se o registro é um pagamento que tem devolução vinculada.
    Compara desc_inf_complementar com description_payment do mapeamento.
    Retorna (is_pagamento_com_devolucao, description_return_vinculado).
    """
    desc_complementar = registro.get("desc_inf_complementar") or ""
    for item in mapeamento_devolucoes:
        description_payment = item.get("description_payment")
        if description_payment and description_payment in desc_complementar:
            return True, item.get("description_return")
    return False, None


def vincular_devolucoes(debitos: list, mapeamento_devolucoes: list) -> dict:
    """
    Vincula devoluções com pagamentos originais.
    Um vínculo é feito quando:
    - A devolução contém description_return
    - O pagamento contém description_payment correspondente
    - A diferença de datas é de até 1 dia

    Retorna dict com informações sobre vinculações e valores a subtrair.
    """
    devolucoes = []
    pagamentos_potenciais = []

    # Separar devoluções de pagamentos potenciais
    for d in debitos:
        is_devolucao, desc_payment = eh_devolucao(d, mapeamento_devolucoes)
        if is_devolucao:
            devolucoes.append((d, desc_payment))
        else:
            is_pagamento, desc_return = eh_pagamento_com_devolucao(d, mapeamento_devolucoes)
            if is_pagamento:
                pagamentos_potenciais.append((d, desc_return))

    vinculacoes = {}  # {id_devolucao: id_pagamento}
    devolucoes_vinculadas = set()
    pagamentos_vinculados = set()
    valores_subtrair = {}  # {id_pagamento: valor_a_subtrair}

    # Para cada devolução, encontrar o pagamento correspondente
    for devolucao, desc_payment in devolucoes:
        data_devolucao = parse_data(devolucao.get("data"))
        valor_devolucao = abs(devolucao.get("valor", 0))
        id_devolucao = id(devolucao)

        for pagamento, desc_return in pagamentos_potenciais:
            id_pagamento = id(pagamento)
            if id_pagamento in pagamentos_vinculados:
                continue

            # Verificar se o description_payment da devolução corresponde ao pagamento
            desc_complementar_pag = pagamento.get("desc_inf_complementar") or ""
            if desc_payment and desc_payment in desc_complementar_pag:
                data_pagamento = parse_data(pagamento.get("data"))

                # Verificar proximidade de data (máximo 1 dia)
                if datas_proximas(data_devolucao, data_pagamento, dias_tolerancia=1):
                    vinculacoes[id_devolucao] = id_pagamento
                    devolucoes_vinculadas.add(id_devolucao)
                    pagamentos_vinculados.add(id_pagamento)
                    valores_subtrair[id_pagamento] = valor_devolucao
                    break

    return {
        "vinculacoes": vinculacoes,
        "devolucoes_vinculadas": devolucoes_vinculadas,
        "pagamentos_vinculados": pagamentos_vinculados,
        "valores_subtrair": valores_subtrair,
    }


def filtrar_debitos(sicoob: list, mapeamento_devolucoes: list = None) -> list:
    resultado = []
    mapeamento_devolucoes = mapeamento_devolucoes or []
    for s in sicoob:
        # Inclui DEBITOS normais
        if s.get("tipo", "").upper() == "DEBITO":
            resultado.append(s)
            continue
        # Inclui registros com ESTORNO na descrição, independente do tipo
        if eh_estorno(s):
            resultado.append(s)
            continue
        # Inclui devoluções (independente de crédito ou débito)
        is_devolucao, _ = eh_devolucao(s, mapeamento_devolucoes)
        if is_devolucao:
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
    mapeamento_devolucoes = criar_mapeamento_devolucoes(dados.get("returns", []))
    debitos = filtrar_debitos(dados.get("sicoob", []), mapeamento_devolucoes)
    despesas = filtrar_despesas(dados.get("releases", []))
    mapeamento = criar_mapeamento_payments(dados.get("payments", []))

    # Vincular estornos com pagamentos
    info_estornos = vincular_estornos(debitos)

    # Vincular devoluções com pagamentos originais
    info_devolucoes = vincular_devolucoes(debitos, mapeamento_devolucoes)

    usados = set()
    itens = []

    for debito in debitos:
        id_debito = id(debito)
        is_estorno = eh_estorno(debito)
        is_devolucao, pagamento_vinculado_desc = eh_devolucao(debito, mapeamento_devolucoes)
        estorno_vinculado = id_debito in info_estornos["estornos_vinculados"]
        pagamento_estorno_vinculado = id_debito in info_estornos["pagamentos_vinculados"]

        # Verificar se é devolução vinculada ou pagamento com devolução vinculada
        devolucao_vinculada = id_debito in info_devolucoes["devolucoes_vinculadas"]
        pagamento_com_devolucao = id_debito in info_devolucoes["pagamentos_vinculados"]
        valor_subtrair = info_devolucoes["valores_subtrair"].get(id_debito, 0)

        # Se é devolução vinculada, marcar com roxo
        if is_devolucao and devolucao_vinculada:
            item = criar_item_conciliado(debito, None, mapeamento)
            item["devolucao"] = True
            item["pagamento_vinculado_desc"] = pagamento_vinculado_desc
            itens.append(item)
            continue

        # Se é devolução sem vínculo (data fora do range)
        if is_devolucao:
            item = criar_item_conciliado(debito, None, mapeamento)
            item["devolucao"] = True
            item["devolucao_sem_vinculo"] = True
            item["pagamento_vinculado_desc"] = pagamento_vinculado_desc
            itens.append(item)
            continue

        # Se é pagamento com devolução vinculada - conciliar normalmente mas subtrair valor e marcar roxo
        if pagamento_com_devolucao:
            disponiveis = [r for r in despesas if r.get("id") not in usados]
            # Criar cópia do debito com valor ajustado para conciliação
            debito_ajustado = debito.copy()
            debito_ajustado["valor"] = abs(debito.get("valor", 0)) - valor_subtrair
            match = encontrar_correspondente(debito_ajustado, disponiveis)

            if match:
                usados.add(match.get("id"))

            item = criar_item_conciliado(debito, match, mapeamento)
            # Ajustar o valor do sicoob para mostrar o valor após subtração
            item["valor_sicoob"] = abs(debito.get("valor", 0)) - valor_subtrair
            item["valor_original"] = abs(debito.get("valor", 0))
            item["valor_devolucao"] = valor_subtrair
            item["pagamento_com_devolucao"] = True
            itens.append(item)
            continue

        # Se é estorno vinculado ou pagamento vinculado a estorno, não conciliar com ERP
        if estorno_vinculado or pagamento_estorno_vinculado:
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
