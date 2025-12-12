import requests
import config
from logger import log


def request(method: str, url: str, **kwargs) -> requests.Response | None:
    try:
        return requests.request(
            method=method,
            url=url,
            cert=(config.CERT_CRT, config.CERT_KEY),
            timeout=30,
            **kwargs,
        )
    except requests.RequestException as e:
        log.error(f"Requisição falhou: {e}")
        return None
