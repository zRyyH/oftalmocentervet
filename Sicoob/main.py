"""Sincroniza extrato bancário com PocketBase."""

import time
import schedule
from datetime import date

from repository import ExtratoRepository
from parser import parse_transactions
from api import get_extrato
from config import SYNC_INTERVAL_MINUTES
from logger import log


def sync():
    hoje = date.today()
    repo = ExtratoRepository()

    response = get_extrato(hoje.month, hoje.year)
    if not response:
        log.warning("Falha ao obter extrato")
        return

    raw = response.get("resultado", {}).get("transacoes", [])
    if not raw:
        log.info("Nenhuma transação")
        return

    transactions = parse_transactions(raw)
    stats = repo.sync(transactions)

    log.info("-" * 80)
    log.info(
        f"Syncronizado: {stats['created']} | Atualizado: {stats['updated']} Erro: {stats['errors']} | Data: {hoje}"
    )
    log.info("-" * 80)


def main():
    log.info(f"Iniciado (intervalo: {SYNC_INTERVAL_MINUTES}min)")
    sync()
    schedule.every(SYNC_INTERVAL_MINUTES).minutes.do(sync)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
