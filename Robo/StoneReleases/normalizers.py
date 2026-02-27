from unicodedata import normalize, category
from datetime import datetime


def clean_str(value):
    if not value:
        return ""
    text = "".join(c for c in normalize("NFD", str(value)) if category(c) != "Mn")
    return text.upper()


def parse_date(value):
    if not value:
        return None
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")
    s = str(value).strip()
    for fmt in [
        "%Y-%m-%d %H:%M:%S.%fZ",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%Y-%m-%d",
    ]:
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except:
            pass
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
    except:
        pass
    return None


def parse_decimal_br(value):
    if not value:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace(".", "").replace(",", "."))
    except:
        return 0.0


def normalizar_produto(valor):
    v = clean_str(valor)
    if "CREDITO" in v or "CREDIT" in v:
        return "CREDITO"
    if "DEBITO" in v or "DEBIT" in v:
        return "DEBITO"
    return v


def normalizar_dados(dados):
    brands = []
    for b in dados.get("brands", []):
        brands.append(
            {
                "brand_stone": clean_str(b.get("brand_stone")),
                "brand_simplesvet": clean_str(b.get("brand_simplesvet")),
                "type": clean_str(b.get("type")),
                "type_simplesvet": clean_str(b.get("type_simplesvet")),
                "gateway": clean_str(b.get("gateway")),
            }
        )

    stone = []
    for s in dados.get("stone", []):
        stone.append(
            {
                "bandeira": clean_str(s.get("BANDEIRA")),
                "produto": normalizar_produto(s.get("PRODUTO")),
                "valor_liquido": parse_decimal_br(s.get("VALOR LÍQUIDO")),
                "data_vencimento": parse_date(s.get("DATA DE VENCIMENTO")),
                "stonecode": str(s.get("STONECODE", "")).strip(),
            }
        )

    releases = []
    for r in dados.get("releases", []):
        releases.append(
            {
                "data": parse_date(r.get("data")),
                "vencimento": parse_date(r.get("vencimento")),
                "valor": float(r.get("valor", 0) or 0),
                "forma_pagamento": clean_str(r.get("forma_pagamento")),
                "descricao": clean_str(r.get("descricao")),
                "fornecedor": clean_str(r.get("fornecedor")),
                "parcela": clean_str(r.get("parcela")),
                "status": clean_str(r.get("status")),
                "tipo": clean_str(r.get("tipo")),
                "origem": clean_str(r.get("origem")),
                "id_r": r.get("id_r", ""),
            }
        )

    return {"brands": brands, "stone": stone, "releases": releases}
