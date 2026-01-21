"""Sincronização SimplesVet → PocketBase (Cron)."""

import time
import schedule
from datetime import datetime, timedelta

from config import SYNC_INTERVAL_MINUTES, SIMPLESVET_EMAIL, SIMPLESVET_PASSWORD
from repository import ConciliationRepository
from scrapper import buscar_conciliacoes
from parser import parse_conciliations
from logger import log


def sync():
    hoje = datetime.now()
    data_inicio = (hoje - timedelta(days=60)).strftime("%Y-%m-%d")
    data_fim = (hoje + timedelta(days=60)).strftime("%Y-%m-%d")

    log.info(f"Buscando conciliações de {data_inicio} até {data_fim}...")
    raw = buscar_conciliacoes(
        email=SIMPLESVET_EMAIL,
        password=SIMPLESVET_PASSWORD,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )

    conciliations = parse_conciliations(raw)
    log.info(f"Encontradas {len(conciliations)} conciliações. Sincronizando...")

    stats = ConciliationRepository().sync(conciliations)

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
