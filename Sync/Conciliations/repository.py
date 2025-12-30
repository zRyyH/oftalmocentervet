"""Repositório para operações no PocketBase."""

from datetime import datetime
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

    def find_by_id(self, id_c: str):
        """Busca conciliação por id_c. Retorna o registro ou None."""
        result = self.collection.get_list(1, 1, {"filter": f'id_c = "{id_c}"'})
        return result.items[0] if result.items else None

    def get_changes(self, existing, new: dict) -> dict:
        """Retorna campos alterados: {campo: (antes, depois)}."""
        changes = {}
        for key, value in new.items():
            old_value = getattr(existing, key, None)
            if self._normalize(old_value) != self._normalize(value):
                changes[key] = (old_value, value)
        return changes

    def _normalize(self, value):
        """Normaliza valor para comparação."""
        if value is None or value == "" or value == 0 or value == 0.0:
            return None

        if isinstance(value, str):
            # Tenta parsear como data com timezone e converter para UTC
            try:
                from datetime import timezone

                # Formato com offset (-03:00)
                if len(value) >= 25 and value[19] in "+-":
                    dt = datetime.fromisoformat(value)
                    return dt.astimezone(timezone.utc).replace(tzinfo=None)

                # Formato UTC com Z
                if value.endswith("Z"):
                    clean = value.replace(".000Z", "").replace("Z", "")
                    return datetime.fromisoformat(clean)

                # Formato sem timezone (assume UTC)
                clean = value.replace(" ", "T")
                for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
                    try:
                        return datetime.strptime(clean, fmt)
                    except ValueError:
                        continue
            except (ValueError, AttributeError):
                pass

        if isinstance(value, (int, float)):
            return round(float(value), 2) if value else None

        return value

    def sync(self, conciliations: list[dict]) -> dict:
        """Sincroniza conciliações. Retorna estatísticas."""
        stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}

        for c in conciliations:
            try:
                existing = self.find_by_id(c["id_c"])

                if existing:
                    changes = self.get_changes(existing, c)
                    if changes:
                        self.collection.update(existing.id, c)
                        stats["updated"] += 1
                        log.info(f"Atualizada: {c['id_c']}")
                        for campo, (antes, depois) in changes.items():
                            log.info(f"  {campo}: {antes!r} → {depois!r}")
                    else:
                        stats["skipped"] += 1
                else:
                    self.collection.create(c)
                    stats["created"] += 1
                    log.info(f"Nova conciliação: {c['id_c']}")

            except Exception as e:
                stats["errors"] += 1
                log.error(f"Falha {c['id_c']}: {e}")

        return stats
