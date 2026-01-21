"""Sync Sicoob -> PocketBase."""

import time
import schedule
from datetime import date, timedelta

import config
from scrapper import get_extrato
from repository import Repository
from logger import log


def parse(raw: dict) -> dict:
    data = raw.get("data", "")
    return {
        "transaction_id": raw.get("transactionId"),
        "tipo": raw.get("tipo"),
        "valor": float(raw.get("valor") or 0),
        "data": data.replace("T", " ") + ":00" if data else None,
        "data_lote": raw.get("dataLote"),
        "descricao": raw.get("descricao"),
        "numero_documento": raw.get("numeroDocumento"),
        "desc_inf_complementar": raw.get("descInfComplementar"),
        "cpf_cnpj": raw.get("cpfCnpj"),
    }


def buscar_ultimos_60_dias() -> list[dict]:
    """Busca extratos dos últimos 60 dias."""
    hoje = date.today()
    inicio = hoje - timedelta(days=60)

    # Identifica os meses no período
    meses = set()
    atual = inicio
    while atual <= hoje:
        meses.add((atual.month, atual.year))
        atual += timedelta(days=28)
    meses.add((hoje.month, hoje.year))

    transacoes = []
    for mes, ano in sorted(meses):
        transacoes.extend(get_extrato(mes, ano))
        log.info(f"Buscado {mes:02d}/{ano}")

    # Filtra só transações dentro do período
    parsed = []
    for t in transacoes:
        p = parse(t)
        if p["data"]:
            data_tx = date.fromisoformat(p["data"][:10])
            if inicio <= data_tx <= hoje:
                parsed.append(p)

    return parsed


def sync(repo: Repository):
    """Truncate + insert de todos os registros."""
    records = buscar_ultimos_60_dias()
    created = repo.sync(records)
    log.info(f"Sync: {created}/{len(records)} registros")


def main():
    log.info("Iniciado")
    repo = Repository()

    sync(repo)

    schedule.every(config.SYNC_INTERVAL_MINUTES).minutes.do(sync, repo)
    log.info(f"Agendado: cada {config.SYNC_INTERVAL_MINUTES} min")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
