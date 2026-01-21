import re

REGEX_PEDIDO = re.compile(r"(?<!\d)\d{1,10}(?!\d)")


def extrair_pedidos(texto: str) -> list:
    if not texto:
        return []
    limpo = re.sub(r"[/,\-]", " ", str(texto))
    limpo = re.sub(r"\bE\b", " ", limpo, flags=re.IGNORECASE)
    return list(dict.fromkeys(REGEX_PEDIDO.findall(limpo)))


def extrair_auth_codes(descricao: str) -> list:
    if not descricao:
        return []
    return [t.upper() for t in descricao.split() if len(t) == 6 and t.isalnum()]


def pedidos_contidos(pedidos: list, descricao: str) -> bool:
    if not pedidos:
        return False
    pedidos_desc = set(extrair_pedidos(descricao))
    return any(p in pedidos_desc for p in pedidos)
