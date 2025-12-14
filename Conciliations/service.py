"""Serviço para buscar conciliações do SimplesVet."""

from datetime import datetime, timedelta

from scrapper import SimplesvetScrapper
from config import DAYS_RANGE, SIMPLESVET_EMAIL, SIMPLESVET_PASSWORD
from parser import parse_conciliations
import json


def fetch_conciliations(hoje: datetime) -> list[dict]:
    """Busca e retorna lista de conciliações."""
    data_inicial = (hoje - timedelta(days=DAYS_RANGE)).strftime("%Y-%m-%d")
    data_final = (hoje + timedelta(days=DAYS_RANGE)).strftime("%Y-%m-%d")

    with SimplesvetScrapper(SIMPLESVET_EMAIL, SIMPLESVET_PASSWORD) as scrapper:
        scrapper.login()
        raw = scrapper.get_conciliations(data_inicial, data_final)

        # with open("data.json", "w", encoding="utf-8") as f:
        #     json.dump(raw, f, ensure_ascii=False, indent=4)

        raw_parsed = parse_conciliations(raw)

        # with open("data_parsed.json", "w", encoding="utf-8") as f:
        #     json.dump(raw_parsed, f, ensure_ascii=False, indent=4)

    return raw_parsed
