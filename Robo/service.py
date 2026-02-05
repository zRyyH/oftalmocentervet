from pocketbase import PocketBase
from pathlib import Path
from config import (
    POCKETBASE_EMAIL,
    POCKETBASE_URL,
)
import json
import time

Path("./Entradas").mkdir(exist_ok=True)


class PocketBaseClient:
    def __init__(self, password):
        self.pb = PocketBase(POCKETBASE_URL)

        if POCKETBASE_EMAIL and password:
            self.pb.admins.auth_with_password(POCKETBASE_EMAIL, password)

    def collection(self, name):
        return self.pb.collection(name)

    def health(self):
        return self.pb.health.check()


def get_all_items(collection, page_size=500, max_retries=10, retry_delay=5):
    """Busca todos os itens de uma collection usando paginação.

    Se não houver registros, tenta novamente até max_retries vezes.
    """
    for attempt in range(1, max_retries + 1):
        all_items = []
        page = 1

        while True:
            result = collection.get_list(page, page_size)
            all_items.extend(result.items)

            if page >= result.total_pages:
                break

            page += 1

        if len(all_items) > 0:
            return all_items

        if attempt < max_retries:
            print(
                f"⏳ Nenhum registro encontrado. Tentativa {attempt}/{max_retries}. Tentando novamente..."
            )
            time.sleep(retry_delay)
        else:
            print(f"⚠ Nenhum registro encontrado após {max_retries} tentativas.")

    return all_items


def serialize_items(items):
    """Converte items do PocketBase para dicionários serializáveis."""
    items_dict = [dict(item.__dict__) for item in items]
    return json.loads(json.dumps(items_dict, default=str))


def get_data(password, limit=None, collections=[]):
    pb = PocketBaseClient(password)

    data = {}
    for name in collections:
        print(f"  Carregando {name}...")
        items = get_all_items(pb.collection(name))

        if limit:
            items = items[:limit]

        data[name] = serialize_items(items)
        print(f"  ✔ {name}: {len(data[name])} registros")

    json_name = "_".join(collections)
    arquivo_saida = f"Entradas/{json_name}.json"

    with open(arquivo_saida, "w") as FileW:
        FileW.write(json.dumps(data, indent=4))

    return data
