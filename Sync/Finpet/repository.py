"""Repositório para operações no PocketBase."""

from pocketbase import PocketBase

from config import (
    COLLECTION_FINPET,
    POCKETBASE_URL,
    PB_ADMIN_EMAIL,
    PB_ADMIN_PASSWORD,
)
from logger import log


class FinpetRepository:
    """Gerencia operações na collection finpet."""

    def __init__(self):
        self.pb = PocketBase(POCKETBASE_URL)
        self.pb.admins.auth_with_password(PB_ADMIN_EMAIL, PB_ADMIN_PASSWORD)
        self.collection = self.pb.collection(COLLECTION_FINPET)

    def find_by_id_t(self, id_t: str):
        """Busca transação por id_t. Retorna o registro ou None."""
        result = self.collection.get_list(1, 1, {"filter": f'id_t = "{id_t}"'})
        return result.items[0] if result.items else None

    def _normalize(self, value):
        """Normaliza valor para comparação."""
        from datetime import datetime

        if value is None or value == "":
            return None

        if isinstance(value, str):
            for fmt in (
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%d %H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d",
            ):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue

        return value

    def get_changes(self, existing, new: dict) -> dict:
        """Retorna campos alterados: {campo: (antes, depois)}."""
        changes = {}
        for key, value in new.items():
            old_value = getattr(existing, key, None)
            if self._normalize(old_value) != self._normalize(value):
                changes[key] = (old_value, value)
        return changes

    def sync(self, transactions: list[dict]) -> dict:
        """Sincroniza transações. Retorna estatísticas."""
        stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}

        for t in transactions:
            try:
                existing = self.find_by_id_t(t["id_t"])

                if existing:
                    changes = self.get_changes(existing, t)
                    if changes:
                        self.collection.update(existing.id, t)
                        stats["updated"] += 1
                        log.info(f"Atualizada: {t['id_t']}")
                        for campo, (antes, depois) in changes.items():
                            log.info(f"  {campo}: {antes!r} → {depois!r}")
                    else:
                        stats["skipped"] += 1
                else:
                    self.collection.create(t)
                    stats["created"] += 1
                    log.info(f"Nova transação: {t['id_t']}")

            except Exception as e:
                stats["errors"] += 1
                log.error(f"Falha {t['id_t']}: {e}")

        return stats
