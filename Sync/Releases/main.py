"""Sincronização SimplesVet → PocketBase (Cron)."""

import time
import schedule
from datetime import datetime, timedelta

from config import SYNC_INTERVAL_MINUTES, SIMPLESVET_EMAIL, SIMPLESVET_PASSWORD
from repository import ReleaseRepository
from service import get_releases
from logger import log


def sync():
    hoje = datetime.now()
    data_inicio = hoje - timedelta(days=60)
    data_fim = hoje + timedelta(days=60)

    log.info("Buscando releases do SimplesVet...")
    releases = get_releases(
        email=SIMPLESVET_EMAIL,
        password=SIMPLESVET_PASSWORD,
        data_inicio=data_inicio.strftime("%Y-%m-%d"),
        data_fim=data_fim.strftime("%Y-%m-%d"),
    )

    log.info(f"Encontrados {len(releases)} releases. Sincronizando...")
    stats = ReleaseRepository().sync(releases)

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

## EXEMPLO
