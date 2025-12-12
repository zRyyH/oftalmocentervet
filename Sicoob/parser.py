"""Parser de transações do extrato Sicoob."""

from datetime import datetime
from typing import Any


def parse_datetime(value: Any) -> str | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).isoformat()
    except (ValueError, TypeError):
        return None


def parse_date(value: Any) -> str | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except (ValueError, TypeError):
        return None


def parse_float(value: Any) -> float:
    if value is None:
        return 0.0
    return float(value)


def parse_str(value: Any) -> str | None:
    if value is None or value == "":
        return None
    return str(value)


def parse_transaction(raw: dict) -> dict:
    return {
        "transaction_id": parse_str(raw.get("transactionId")),
        "tipo": parse_str(raw.get("tipo")),
        "valor": parse_float(raw.get("valor")),
        "data": parse_datetime(raw.get("data")),
        "data_lote": parse_date(raw.get("dataLote")),
        "descricao": parse_str(raw.get("descricao")),
        "numero_documento": parse_str(raw.get("numeroDocumento")),
        "desc_inf_complementar": parse_str(raw.get("descInfComplementar")),
        "cpf_cnpj": parse_str(raw.get("cpfCnpj")),
    }


def parse_transactions(raw_list: list[dict]) -> list[dict]:
    return [parse_transaction(t) for t in raw_list]
