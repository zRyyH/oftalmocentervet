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
    for fmt in [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%fZ",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
    ]:
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
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
                "info": clean_str(b.get("info")),
                "gateway": clean_str(b.get("gateway")),
                "type": clean_str(b.get("type")),
            }
        )

    sicoob = []
    for s in dados.get("sicoob", []):
        sicoob.append(
            {
                "tipo": clean_str(s.get("tipo")),
                "valor": float(s.get("valor", 0)),
                "descricao": clean_str(s.get("descricao")),
                "desc_inf_complementar": clean_str(s.get("desc_inf_complementar")),
                "data": parse_date(s.get("data")),
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

    return {"brands": brands, "sicoob": sicoob, "stone": stone}
