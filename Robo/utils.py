from datetime import datetime

FORMATOS_DATA = [
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S.%fZ",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y",
]


def parse_data(valor):
    """Converte string em datetime. Retorna None se falhar."""
    if not valor:
        return None
    if isinstance(valor, datetime):
        return valor
    texto = str(valor).replace("Z", "").replace("T", " ").strip()[:26]
    for fmt in FORMATOS_DATA:
        try:
            return datetime.strptime(texto, fmt)
        except ValueError:
            continue
    return None


def formatar_data(valor, formato_saida="%Y-%m-%d"):
    dt = parse_data(valor)
    return dt.strftime(formato_saida) if dt else ""


def extrair_mes_ano(valor, formato="%m-%Y"):
    dt = parse_data(valor)
    return dt.strftime(formato) if dt else None


def agrupar_por_mes(itens, campo_data="data"):
    from collections import defaultdict

    grupos = defaultdict(list)
    for item in itens:
        valor = (
            item.get(campo_data, "")
            if isinstance(item, dict)
            else getattr(item, campo_data, "")
        )
        mes_ano = extrair_mes_ano(valor) or "Sem Data"
        grupos[mes_ano].append(item)
    return grupos


def ordenar_por_data(itens, campo_data="data", reverso=True):
    return sorted(
        itens,
        key=lambda x: parse_data(x.get(campo_data, "")) or datetime.min,
        reverse=reverso,
    )


def ordenar_chaves_mes(chaves):
    def chave_sort(c):
        if c == "Sem Data":
            return (9999, 99)
        partes = c.replace("/", "-").split("-")
        if len(partes) == 2:
            return (int(partes[1]), int(partes[0]))
        return (0, 0)

    return sorted(chaves, key=chave_sort)
