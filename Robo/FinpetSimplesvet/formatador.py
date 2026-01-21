from datetime import datetime
from collections import defaultdict


def parse_data(valor):
    if not valor or not isinstance(valor, str):
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(valor[:10], fmt)
        except ValueError:
            continue
    return None


def formatar_data(valor):
    return valor[:10] if isinstance(valor, str) and len(valor) >= 10 else None


def extrair_mes_ano(valor):
    if isinstance(valor, str) and len(valor) >= 7:
        partes = valor[:10].split("-")
        if len(partes) >= 2:
            return f"{partes[1]}/{partes[0]}"
    return None


def extrair_linha(item):
    finpet = item.get("finpet", {})
    comp = item.get("comparacoes", {})
    pedidos = comp.get("cliente", {}).get("finpet", [])

    return {
        "valor_finpet": comp.get("valor", {}).get("finpet"),
        "data_estimada": formatar_data(comp.get("data", {}).get("finpet_estimated")),
        "bandeira": finpet.get("payment_brand"),
        "score": item.get("score"),
        "parcela_finpet": comp.get("parcela", {}).get("finpet"),
        "parcela_release": comp.get("parcela", {}).get("release"),
        "valor_finpet_2": comp.get("valor", {}).get("finpet"),
        "valor_release": comp.get("valor", {}).get("release"),
        "data_finpet": formatar_data(comp.get("data", {}).get("finpet_estimated")),
        "data_release": formatar_data(comp.get("data", {}).get("release")),
        "auth_finpet": comp.get("auth", {}).get("finpet"),
        "auth_release": comp.get("auth", {}).get("release"),
        "pedidos": ", ".join(pedidos) if pedidos else "",
        "cliente_release": comp.get("cliente", {}).get("release"),
        "exact_value": comp.get("valor", {}).get("exact_value", True),
        "approximate_value": comp.get("valor", {}).get("approximate_value", True),
        "matches": {
            "parcela": comp.get("parcela", {}).get("match", True),
            "valor": comp.get("valor", {}).get("match", True),
            "data": comp.get("data", {}).get("match", True),
            "auth": comp.get("auth", {}).get("match", True),
            "cliente": comp.get("cliente", {}).get("match", True),
        },
    }


def ordenar_dados(dados):
    return sorted(
        dados,
        key=lambda x: parse_data(x.get("finpet", {}).get("date_estimated"))
        or datetime.min,
        reverse=True,
    )


def agrupar_por_mes(dados):
    grupos = defaultdict(list)
    for item in dados:
        data_str = item.get("comparacoes", {}).get("data", {}).get("finpet_estimated")
        mes_ano = extrair_mes_ano(data_str) or "Sem Data"
        grupos[mes_ano].append(extrair_linha(item))
    return grupos


def ordenar_meses(meses):
    def chave(m):
        if m == "Sem Data":
            return (9999, 99)
        partes = m.split("/")
        return (int(partes[1]), int(partes[0]))

    return sorted(meses, key=chave)


def preparar_dados(dados):
    if not dados:
        return {}
    dados_ordenados = ordenar_dados(dados)
    return agrupar_por_mes(dados_ordenados)
