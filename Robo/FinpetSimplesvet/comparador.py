from .extratores import extrair_pedidos, extrair_auth_codes, pedidos_contidos
from .normalizadores import (
    normalizar_parcela,
    normalizar_valor,
    normalizar_data,
    normalizar_tipo,
    formatar_parcela,
)


def calcular_match(finpet: dict, release: dict) -> dict:
    resultado = {"score": 0, "comparacoes": {}}
    comp = resultado["comparacoes"]

    pedidos = extrair_pedidos(finpet.get("client_name"))
    descricao = release.get("descricao") or ""

    cliente_match = pedidos_contidos(pedidos, descricao)
    comp["cliente"] = {"finpet": pedidos, "release": descricao, "match": cliente_match}

    if not cliente_match:
        return _criar_resultado_sem_match(finpet, release, comp)

    score = 1
    is_supplier = finpet.get("type") == "SUPPLIER"

    comp["tipo"] = _comparar_tipo(finpet, release)
    comp["parcela"] = _comparar_parcela(finpet, release, is_supplier)
    comp["valor"] = _comparar_valor(finpet, release)
    comp["data"] = _comparar_data(finpet, release)
    comp["auth"] = _comparar_auth(finpet, descricao, is_supplier)

    for campo in ["parcela", "valor", "data", "auth"]:
        if comp[campo]["match"]:
            score += 1

    resultado["score"] = score
    return resultado


def _criar_resultado_sem_match(finpet: dict, release: dict, comp: dict) -> dict:
    comp["tipo"] = {
        "finpet": finpet.get("type"),
        "release": release.get("tipo"),
        "match": False,
    }
    comp["parcela"] = {
        "finpet": formatar_parcela(finpet.get("installment_number")),
        "release": formatar_parcela(release.get("parcela")),
        "match": False,
    }
    comp["valor"] = {
        "finpet": finpet.get("value"),
        "release": release.get("valor"),
        "match": False,
    }
    comp["data"] = {
        "finpet_estimated": finpet.get("date_estimated"),
        "release": release.get("data"),
        "match": False,
    }
    comp["auth"] = {
        "finpet": finpet.get("authorization_number"),
        "release": None,
        "match": False,
    }
    return {"score": 0, "comparacoes": comp}


def _comparar_tipo(finpet: dict, release: dict) -> dict:
    tipo_fp = normalizar_tipo(finpet.get("type"))
    return {
        "finpet": finpet.get("type"),
        "release": release.get("tipo"),
        "match": tipo_fp == release.get("tipo"),
    }


def _comparar_parcela(finpet: dict, release: dict, is_supplier: bool) -> dict:
    p1 = normalizar_parcela(finpet.get("installment_number"))
    p2 = normalizar_parcela(release.get("parcela"))
    is_unica = p1 == (1, 1)

    parcela_fp = formatar_parcela(finpet.get("installment_number"))
    parcela_rel = formatar_parcela(release.get("parcela"))

    if is_supplier or is_unica:
        return {
            "finpet": parcela_fp,
            "release": parcela_fp,
            "match": True,
        }

    return {
        "finpet": parcela_fp,
        "release": parcela_rel,
        "match": bool(p1 and p2 and p1 == p2),
    }


def _comparar_valor(finpet: dict, release: dict) -> dict:
    v1 = normalizar_valor(finpet.get("value"))
    v2 = normalizar_valor(release.get("valor"))
    return {
        "finpet": finpet.get("value"),
        "release": release.get("valor"),
        "match": abs(v1 - v2) <= 0.05,
    }


def _comparar_data(finpet: dict, release: dict) -> dict:
    d_estimada = normalizar_data(finpet.get("date_estimated"))
    d_recebida = normalizar_data(finpet.get("date_received"))
    d_release = normalizar_data(release.get("data"))
    return {
        "finpet_estimated": finpet.get("date_estimated"),
        "release": release.get("data"),
        "match": bool(
            d_release and (d_estimada == d_release or d_recebida == d_release)
        ),
    }


def _comparar_auth(finpet: dict, descricao: str, is_supplier: bool) -> dict:
    auth_fp = (finpet.get("authorization_number") or "").upper()
    auths_release = extrair_auth_codes(descricao)

    if is_supplier:
        return {
            "finpet": auth_fp or None,
            "release": auth_fp,
            "auths_encontrados": auths_release,
            "match": True,
        }

    auth_match = auth_fp in auths_release if auth_fp else False
    auth_rel = auth_fp if auth_match else (auths_release[0] if auths_release else None)

    return {
        "finpet": auth_fp or None,
        "release": auth_rel,
        "auths_encontrados": auths_release,
        "match": auth_match,
    }


def criar_comparacoes_vazias(finpet: dict) -> dict:
    return {
        "cliente": {
            "finpet": extrair_pedidos(finpet.get("client_name")),
            "release": "",
            "match": False,
        },
        "tipo": {"finpet": finpet.get("type"), "release": None, "match": False},
        "parcela": {
            "finpet": formatar_parcela(finpet.get("installment_number")),
            "release": None,
            "match": False,
        },
        "valor": {"finpet": finpet.get("value"), "release": None, "match": False},
        "data": {
            "finpet_estimated": finpet.get("date_estimated"),
            "release": None,
            "match": False,
        },
        "auth": {
            "finpet": finpet.get("authorization_number"),
            "release": None,
            "match": False,
        },
    }
