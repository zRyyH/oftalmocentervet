"""Sincronização Finpet → PocketBase (Cron)."""

import time
import schedule
from datetime import datetime, timedelta

from config import SYNC_INTERVAL_MINUTES, FINPET_EMAIL, FINPET_PASSWORD
from repository import Repository
from parser import parse_all
from scrapper import scrape
from logger import log


def sync():
    hoje = datetime.now()
    inicio = (hoje - timedelta(days=60)).strftime("%Y-%m-%d")
    fim = (hoje + timedelta(days=60)).strftime("%Y-%m-%d")

    log.info("Buscando dados do Finpet...")
    dados = scrape(FINPET_EMAIL, FINPET_PASSWORD, inicio, fim)

    log.info(f"Encontrados {len(dados)} registros. Sincronizando...")
    transactions = parse_all(dados)
    stats = Repository().sync(transactions)

    log.info(
        f"Criados: {stats['created']} | Erros: {stats['errors']} | "
        f"Data: {hoje.strftime('%Y-%m-%d %H:%M')}"
    )


def main():
    log.info(f"Iniciado (intervalo: {SYNC_INTERVAL_MINUTES}min)")
    sync()
    schedule.every(SYNC_INTERVAL_MINUTES).minutes.do(sync)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
