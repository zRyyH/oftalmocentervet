"""Repositório para operações no PocketBase."""

from datetime import datetime, timezone
from pocketbase import PocketBase

from config import (
    COLLECTION_RELEASES,
    POCKETBASE_URL,
    PB_ADMIN_EMAIL,
    PB_ADMIN_PASSWORD,
)
from logger import log


class ReleaseRepository:
    """Gerencia operações na collection de releases."""

    def __init__(self):
        self.pb = PocketBase(POCKETBASE_URL)
        self.pb.admins.auth_with_password(PB_ADMIN_EMAIL, PB_ADMIN_PASSWORD)
        self.collection = self.pb.collection(COLLECTION_RELEASES)

    def find_by_id(self, id_r: str):
        """Busca release por id_r. Retorna o registro ou None."""
        result = self.collection.get_list(1, 1, {"filter": f'id_r = "{id_r}"'})
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
            try:
                if len(value) >= 25 and value[19] in "+-":
                    dt = datetime.fromisoformat(value)
                    return dt.astimezone(timezone.utc).replace(tzinfo=None)

                if value.endswith("Z"):
                    clean = value.replace(".000Z", "").replace("Z", "")
                    return datetime.fromisoformat(clean)

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

    def sync(self, releases: list[dict]) -> dict:
        """Sincroniza releases. Retorna estatísticas."""
        stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}

        for r in releases:
            try:
                existing = self.find_by_id(r["id_r"])

                if existing:
                    changes = self.get_changes(existing, r)
                    if changes:
                        self.collection.update(existing.id, r)
                        stats["updated"] += 1
                        log.info(f"Atualizado: {r['id_r']}")
                        for campo, (antes, depois) in changes.items():
                            log.info(f"  {campo}: {antes!r} → {depois!r}")
                    else:
                        stats["skipped"] += 1
                else:
                    self.collection.create(r)
                    stats["created"] += 1
                    log.info(f"Novo release: {r['id_r']}")

            except Exception as e:
                stats["errors"] += 1
                log.error(f"Falha {r['id_r']}: {e}")

        return stats
