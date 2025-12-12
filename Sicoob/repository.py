from pocketbase import PocketBase
from datetime import datetime

from config import (
    POCKETBASE_URL,
    POCKETBASE_EMAIL,
    POCKETBASE_PASSWORD,
    COLLECTION_NAME,
)
from logger import log


class ExtratoRepository:

    def __init__(self):
        self.pb = PocketBase(POCKETBASE_URL)
        self.pb.admins.auth_with_password(POCKETBASE_EMAIL, POCKETBASE_PASSWORD)
        self.collection = self.pb.collection(COLLECTION_NAME)

    def find_by_transaction_id(self, transaction_id: str):
        try:
            result = self.collection.get_list(
                1, 1, {"filter": f'transaction_id = "{transaction_id}"'}
            )
            return result.items[0] if result.items else None
        except Exception:
            return None

    def _normalize(self, value):
        if value is None or value == "":
            return None

        if isinstance(value, str):
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S.%fZ", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue

        return value

    def get_changes(self, existing, new: dict) -> dict:
        changes = {}
        for key, value in new.items():
            old = self._normalize(getattr(existing, key, None))
            if old != self._normalize(value):
                changes[key] = (old, value)
        return changes

    def sync(self, transactions: list[dict]) -> dict:
        stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}

        for t in transactions:
            tid = t.get("transaction_id")
            try:
                existing = self.find_by_transaction_id(tid)

                if existing:
                    changes = self.get_changes(existing, t)
                    if changes:
                        self.collection.update(existing.id, t)
                        stats["updated"] += 1
                        diff = ", ".join(
                            f"{k} [{old} → {new}]" for k, (old, new) in changes.items()
                        )
                        log.info(f"~ {tid}: {diff}")
                    else:
                        stats["skipped"] += 1
                else:
                    self.collection.create(t)
                    stats["created"] += 1
                    log.info(
                        f"+ {tid}: {t['tipo']} R${t['valor']:.2f} - {t['descricao']}"
                    )

            except Exception as e:
                stats["errors"] += 1
                log.error(f"Transação {tid}: {e}")

        return stats
