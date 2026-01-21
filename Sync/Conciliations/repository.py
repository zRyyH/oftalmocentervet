"""Repositório para operações no PocketBase."""

from pocketbase import PocketBase

from config import (
    COLLECTION_CONCILIATIONS,
    POCKETBASE_URL,
    PB_ADMIN_EMAIL,
    PB_ADMIN_PASSWORD,
)
from logger import log


class ConciliationRepository:
    """Gerencia operações na collection de conciliações."""

    def __init__(self):
        self.pb = PocketBase(POCKETBASE_URL)
        self.pb.admins.auth_with_password(PB_ADMIN_EMAIL, PB_ADMIN_PASSWORD)
        self.collection = self.pb.collection(COLLECTION_CONCILIATIONS)

    def truncate(self):
        """Limpa todos os registros da collection."""
        self.pb.send(
            f"/api/collections/{COLLECTION_CONCILIATIONS}/truncate",
            {"method": "DELETE"},
        )
        log.info("Collection limpa via truncate")

    def batch_create(self, conciliations: list[dict]) -> dict:
        """Cria múltiplos registros de uma vez. Retorna estatísticas."""
        stats = {"created": 0, "errors": 0}

        if not conciliations:
            return stats

        requests = [
            {
                "method": "POST",
                "url": f"/api/collections/{COLLECTION_CONCILIATIONS}/records",
                "body": conciliation,
            }
            for conciliation in conciliations
        ]

        batch_size = 10000
        for i in range(0, len(requests), batch_size):
            batch = requests[i : i + batch_size]
            try:
                response = self.pb.send(
                    "/api/batch", {"method": "POST", "body": {"requests": batch}}
                )
                for result in response:
                    if result.get("status", 0) == 200:
                        stats["created"] += 1
                    else:
                        stats["errors"] += 1
            except Exception as e:
                log.error(f"Erro no batch {i//batch_size + 1}: {e}")
                stats["errors"] += len(batch)

        return stats

    def sync(self, conciliations: list[dict]) -> dict:
        """Limpa collection e recria todos os registros."""
        if not conciliations:
            return {"created": 0, "errors": 0}

        self.truncate()
        return self.batch_create(conciliations)
