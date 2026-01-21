from datetime import datetime
import re


def parse_data(valor: str) -> datetime | None:
    if not valor:
        return None
    valor = str(valor).replace("Z", "").strip()
    for fmt in ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            return datetime.strptime(valor, fmt)
        except ValueError:
            continue
    return None


def valores_iguais(valor1: float, valor2: float, tolerancia: float = 0.01) -> bool:
    return abs(abs(valor1) - abs(valor2)) <= tolerancia


def datas_correspondem(data1: datetime, data2: datetime) -> bool:
    return data1.day == data2.day and data1.month == data2.month


def extrair_tipo_pagamento_sicoob(descricao: str) -> str:
    descricao = (descricao or "").upper()

    padroes = {
        "PIX": [r"\bPIX\b", r"PIX\s*-", r"PIX\s*TRANSF", r"PIX\s*ENV"],
        "TED": [r"\bTED\b", r"TRANSF\s*TED"],
        "DOC": [r"\bDOC\b"],
        "BOLETO": [r"\bBOLETO\b", r"PAGTO\s*TITULO", r"PAG\s*TITULO"],
        "DEBITO": [r"\bDEBITO\b", r"DEB\s*AUTO", r"DEBITO\s*AUTO"],
        "CARTAO": [r"\bCARTAO\b", r"CART[AÃ]O"],
        "CHEQUE": [r"\bCHEQUE\b", r"\bCHQ\b"],
        "TRANSFERENCIA": [r"\bTRANSF\b", r"TRANSFER[EÊ]NCIA"],
    }

    for tipo, lista_padroes in padroes.items():
        for padrao in lista_padroes:
            if re.search(padrao, descricao):
                return tipo

    return "OUTRO"


def normalizar_forma_pagamento(forma: str) -> str:
    forma = (forma or "").upper().strip()
    forma = forma.replace("É", "E").replace("Ã", "A").replace("Ç", "C")

    mapeamento = {
        "PIX": ["PIX"],
        "TED": ["TED", "TRANSFERENCIA TED"],
        "DOC": ["DOC"],
        "BOLETO": ["BOLETO", "TITULO", "COBRANCA"],
        "DEBITO": ["DEBITO", "DEB AUTO", "AUTOMATICO"],
        "CARTAO": ["CARTAO", "CREDITO"],
        "CHEQUE": ["CHEQUE", "CHQ"],
        "TRANSFERENCIA": ["TRANSFERENCIA", "TRANSF"],
        "DINHEIRO": ["DINHEIRO", "ESPECIE"],
    }

    for tipo, variantes in mapeamento.items():
        for variante in variantes:
            if variante in forma:
                return tipo

    return "OUTRO"


def formas_pagamento_correspondem(tipo_sicoob: str, forma_erp: str) -> bool:
    tipo_sicoob = tipo_sicoob.upper()
    forma_erp_norm = normalizar_forma_pagamento(forma_erp)

    if tipo_sicoob == forma_erp_norm:
        return True

    equivalencias = {
        "TRANSFERENCIA": ["TED", "DOC", "PIX"],
        "TED": ["TRANSFERENCIA"],
        "DOC": ["TRANSFERENCIA"],
        "PIX": ["TRANSFERENCIA"],
    }

    if tipo_sicoob in equivalencias:
        if forma_erp_norm in equivalencias[tipo_sicoob]:
            return True

    return False


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


def filtrar_debitos(sicoob: list) -> list:
    return [s for s in sicoob if s.get("tipo", "").upper() == "DEBITO"]


def filtrar_despesas(releases: list) -> list:
    return [r for r in releases if r.get("tipo") == "despesa"]


def formatar_data(data_str: str) -> str:
    return data_str[:10] if data_str else ""


def criar_item_conciliado(debito: dict, match: dict | None) -> dict:
    descricao_sicoob = debito.get("descricao", "")
    tipo_pag_sicoob = extrair_tipo_pagamento_sicoob(descricao_sicoob)
    forma_pag_erp = match.get("forma_pagamento") if match else None

    forma_confere = None
    if match and forma_pag_erp:
        forma_confere = formas_pagamento_correspondem(tipo_pag_sicoob, forma_pag_erp)

    return {
        "data_sicoob": formatar_data(debito.get("data", "")),
        "valor_sicoob": debito.get("valor", 0),
        "descricao_sicoob": descricao_sicoob,
        "info_complementar": debito.get("desc_inf_complementar", ""),
        "tipo_pag_sicoob": tipo_pag_sicoob,
        "conciliado": match is not None,
        "data_erp": formatar_data(match.get("data", "")) if match else None,
        "valor_erp": abs(match.get("valor", 0)) if match else None,
        "descricao_erp": match.get("descricao") if match else None,
        "fornecedor_erp": match.get("fornecedor") if match else None,
        "forma_pagamento_erp": forma_pag_erp,
        "forma_confere": forma_confere,
    }


def conciliar(dados: dict) -> dict:
    debitos = filtrar_debitos(dados.get("sicoob", []))
    despesas = filtrar_despesas(dados.get("releases", []))

    usados = set()
    itens = []

    for debito in debitos:
        disponiveis = [r for r in despesas if r.get("id") not in usados]
        match = encontrar_correspondente(debito, disponiveis)

        if match:
            usados.add(match.get("id"))

        itens.append(criar_item_conciliado(debito, match))

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
