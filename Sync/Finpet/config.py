"""Configurações da aplicação."""

from os import getenv
from dotenv import load_dotenv

load_dotenv()

POCKETBASE_URL = getenv("POCKETBASE_URL")
PB_ADMIN_EMAIL = getenv("PB_ADMIN_EMAIL")
PB_ADMIN_PASSWORD = getenv("PB_ADMIN_PASSWORD")
COLLECTION_FINPET = getenv("COLLECTION_FINPET", "finpet")

FINPET_EMAIL = getenv("FINPET_EMAIL")
FINPET_PASSWORD = getenv("FINPET_PASSWORD")

DAYS_RANGE = int(getenv("DAYS_RANGE", "5"))
SYNC_INTERVAL_MINUTES = int(getenv("SYNC_INTERVAL_MINUTES", "30"))