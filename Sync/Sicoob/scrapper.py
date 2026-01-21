"""Scraper Sicoob - busca extratos via API."""

import requests
from config import CERT_CRT, CERT_KEY, CLIENT_ID, CONTA_CORRENTE

AUTH_URL = (
    "https://auth.sicoob.com.br/auth/realms/cooperado/protocol/openid-connect/token"
)
EXTRATO_URL = "https://api.sicoob.com.br/conta-corrente/v4/extrato"


def _get_token() -> str | None:
    try:
        r = requests.post(
            AUTH_URL,
            data={
                "grant_type": "client_credentials",
                "scope": "cco_consulta",
                "client_id": CLIENT_ID,
            },
            cert=(CERT_CRT, CERT_KEY),
            timeout=30,
        )
        return r.json().get("access_token") if r.ok else None
    except:
        return None


def get_extrato(mes: int, ano: int) -> list[dict]:
    token = _get_token()
    if not token:
        return []
    try:
        r = requests.get(
            f"{EXTRATO_URL}/{mes}/{ano}",
            headers={"Authorization": f"Bearer {token}", "client_id": CLIENT_ID},
            params={"numeroContaCorrente": CONTA_CORRENTE},
            cert=(CERT_CRT, CERT_KEY),
            timeout=30,
        )
        return r.json().get("resultado", {}).get("transacoes", []) if r.ok else []
    except:
        return []
