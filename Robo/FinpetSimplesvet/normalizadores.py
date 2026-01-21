import re


def normalizar_parcela(parcela: str) -> tuple:
    if not parcela:
        return None
    if "/" in str(parcela):
        partes = str(parcela).split("/")
        return (int(partes[0]), int(partes[1]))
    match = re.search(r"(\d+)\s*de\s*(\d+)", str(parcela))
    return (int(match.group(1)), int(match.group(2))) if match else None


def formatar_parcela(parcela: str) -> str:
    if not parcela:
        return None
    valor_str = str(parcela)
    if "/" in valor_str:
        partes = valor_str.split("/")
        return f"{int(partes[0])}/{int(partes[1])}"
    match = re.search(r"(\d+)\s*de\s*(\d+)", valor_str, re.IGNORECASE)
    if match:
        return f"{int(match.group(1))}/{int(match.group(2))}"
    if valor_str.isdigit():
        return f"{int(valor_str)}/1"
    return valor_str


def normalizar_valor(valor) -> float:
    return abs(float(valor)) if valor else 0.0


def normalizar_data(data: str) -> str:
    return data[:10] if data else None


def normalizar_tipo(tipo_finpet: str) -> str:
    return {"MERCHANT": "receita", "SUPPLIER": "despesa"}.get(tipo_finpet)
