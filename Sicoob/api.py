import config
import client
from logger import log


def get_access_token() -> str | None:
    resp = client.request(
        "POST",
        config.AUTH_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "scope": config.AUTH_SCOPE,
            "client_id": config.CLIENT_ID,
        },
    )

    if resp and resp.status_code == 200:
        return resp.json()["access_token"]

    log.error(f"Token inválido: {resp.status_code if resp else 'sem resposta'}")
    return None


def get_extrato(mes: int, ano: int) -> dict | None:
    token = get_access_token()
    if not token:
        return None

    url = config.EXTRATO_URL.format(mes=mes, ano=ano)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "client_id": config.CLIENT_ID,
    }
    params = {"numeroContaCorrente": config.CONTA_CORRENTE}

    resp = client.request("GET", url, headers=headers, params=params)

    if resp and resp.status_code == 200:
        return resp.json()

    log.error(f"Extrato falhou: {resp.status_code if resp else 'sem resposta'}")
    return None
