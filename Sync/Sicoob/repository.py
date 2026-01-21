"""Repositório PocketBase."""

from pocketbase import PocketBase
from config import COLLECTION_SICOOB, POCKETBASE_URL, PB_ADMIN_EMAIL, PB_ADMIN_PASSWORD
from logger import log


class Repository:
    def __init__(self):
        self.pb = PocketBase(POCKETBASE_URL)
        self.pb.admins.auth_with_password(PB_ADMIN_EMAIL, PB_ADMIN_PASSWORD)

    def truncate(self):
        self.pb.send(
            f"/api/collections/{COLLECTION_SICOOB}/truncate", {"method": "DELETE"}
        )

    def batch_create(self, records: list[dict]) -> int:
        if not records:
            return 0

        requests = [
            {
                "method": "POST",
                "url": f"/api/collections/{COLLECTION_SICOOB}/records",
                "body": r,
            }
            for r in records
        ]

        created = 0
        for i in range(0, len(requests), 10000):
            batch = requests[i : i + 10000]
            try:
                response = self.pb.send(
                    "/api/batch", {"method": "POST", "body": {"requests": batch}}
                )
                created += sum(1 for r in response if r.get("status") == 200)
            except Exception as e:
                log.error(f"Erro batch: {e}")
        return created

    def sync(self, records: list[dict]) -> int:
        """Truncate + insert de todos os registros."""
        self.truncate()
        return self.batch_create(records)
