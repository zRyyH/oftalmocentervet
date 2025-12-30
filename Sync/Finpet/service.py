"""Serviço para buscar transações do Finpet."""

from datetime import timedelta

from scrapper import FinpetScrapper

from config import DAYS_RANGE, FINPET_EMAIL, FINPET_PASSWORD

from parser import parse_transactions

import json


def fetch_transactions(hoje) -> list[dict]:
    """Busca e retorna lista de transações."""

    data_inicial = (hoje - timedelta(days=DAYS_RANGE)).strftime("%Y-%m-%d")
    data_final = (hoje + timedelta(days=DAYS_RANGE)).strftime("%Y-%m-%d")

    with FinpetScrapper(email=FINPET_EMAIL, password=FINPET_PASSWORD) as scrapper:
        scrapper.login()
        raw = scrapper.get_receipts(data_inicial, data_final)

        data = (
            raw.get("merchantPaymentSearchDTO", {})
            .get("paymentList", {})
            .get("list", [])
        )

        data_parsed = parse_transactions(data)

    return data_parsed
