"""Configurações da aplicação."""

from os import getenv
from dotenv import load_dotenv

load_dotenv()

POCKETBASE_URL = getenv("POCKETBASE_URL")
PB_ADMIN_EMAIL = getenv("PB_ADMIN_EMAIL")
PB_ADMIN_PASSWORD = getenv("PB_ADMIN_PASSWORD")
COLLECTION_RELEASES = getenv("COLLECTION_RELEASES")

SIMPLESVET_EMAIL = getenv("SIMPLESVET_EMAIL")
SIMPLESVET_PASSWORD = getenv("SIMPLESVET_PASSWORD")

SYNC_INTERVAL_MINUTES = int(getenv("SYNC_INTERVAL_MINUTES"))