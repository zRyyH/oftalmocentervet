import sys
from pathlib import Path

# Adiciona a raiz ao path para importar utils
raiz = Path(__file__).parent.parent
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))

# Importa funções reutilizáveis do utils.py
from utils import parse_data, formatar_data, extrair_mes_ano, ordenar_chaves_mes


def extrair_linha(item):
    finpet = item.get("finpet", {})
    comp = item.get("comparacoes", {})
    pedidos = comp.get("cliente", {}).get("finpet", [])

    return {
        "valor_finpet": comp.get("valor", {}).get("finpet"),
        "data_estimada": formatar_data(comp.get("data", {}).get("finpet_estimated")),
        "bandeira": finpet.get("payment_brand"),
        "beneficiario": finpet.get("beneficiary"),
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
    """Ordena dados por data estimada do finpet."""
    from datetime import datetime
    return sorted(
        dados,
        key=lambda x: parse_data(x.get("finpet", {}).get("date_estimated"))
        or datetime.min,
        reverse=True,
    )


def agrupar_por_mes(dados):
    """Agrupa dados por mês/ano baseado na data estimada."""
    from collections import defaultdict
    grupos = defaultdict(list)
    for item in dados:
        data_str = item.get("comparacoes", {}).get("data", {}).get("finpet_estimated")
        mes_ano = extrair_mes_ano(data_str, formato="%m/%Y") or "Sem Data"
        grupos[mes_ano].append(extrair_linha(item))
    return grupos


def ordenar_meses(meses):
    """Ordena as chaves de mês/ano."""
    return ordenar_chaves_mes(meses)


def preparar_dados(dados):
    if not dados:
        return {}
    dados_ordenados = ordenar_dados(dados)
    return agrupar_por_mes(dados_ordenados)
