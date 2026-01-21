from config import (
    POCKETBASE_EMAIL,
    POCKETBASE_PASSWORD,
    POCKETBASE_URL,
)
from pocketbase import PocketBase
import json


class PocketBaseClient:
    def __init__(self):
        self.pb = PocketBase(POCKETBASE_URL)

        if POCKETBASE_EMAIL and POCKETBASE_PASSWORD:
            self.pb.admins.auth_with_password(POCKETBASE_EMAIL, POCKETBASE_PASSWORD)

    def collection(self, name):
        return self.pb.collection(name)

    def health(self):
        return self.pb.health.check()


def get_all_items(collection, page_size=500):
    """Busca todos os itens de uma collection usando paginação."""
    all_items = []
    page = 1

    while True:
        result = collection.get_list(page, page_size)
        all_items.extend(result.items)

        if page >= result.total_pages:
            break

        page += 1

    return all_items


def serialize_items(items):
    """Converte items do PocketBase para dicionários serializáveis."""
    items_dict = [dict(item.__dict__) for item in items]
    return json.loads(json.dumps(items_dict, default=str))


def get_data(limit=None, collections=[]):
    pb = PocketBaseClient()

    data = {}
    for name in collections:
        items = get_all_items(pb.collection(name))

        if limit:
            items = items[:limit]

        data[name] = serialize_items(items)

    return data
