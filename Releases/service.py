"""Serviço para buscar releases do SimplesVet."""

from datetime import datetime, timedelta
import json

from scrapper import SimplesvetScrapper
from config import DAYS_RANGE, SIMPLESVET_EMAIL, SIMPLESVET_PASSWORD
from parser import parse_releases


def fetch_releases(hoje: datetime) -> list[dict]:
    """Busca e retorna lista de releases."""
    data_inicial = (hoje - timedelta(days=DAYS_RANGE)).strftime("%Y-%m-%d")
    data_final = (hoje + timedelta(days=DAYS_RANGE)).strftime("%Y-%m-%d")

    with SimplesvetScrapper(SIMPLESVET_EMAIL, SIMPLESVET_PASSWORD) as scrapper:
        scrapper.login()
        raw = scrapper.get_releases(data_inicial, data_final)

        # with open("data.json", "w", encoding="utf-8") as f:
        #     json.dump(raw, f, ensure_ascii=False, indent=4)

        parsed = parse_releases(raw)

        # with open("data_parsed.json", "w", encoding="utf-8") as f:
        #     json.dump(parsed, f, ensure_ascii=False, indent=4)

    return parsed
