import os
from dotenv import load_dotenv

load_dotenv()

CERT_CRT = os.getenv("CERT_CRT", "./keys/sicoob_cert.crt")
CERT_KEY = os.getenv("CERT_KEY", "./keys/sicoob_key.pem")
CLIENT_ID = os.getenv("CLIENT_ID")
CONTA_CORRENTE = os.getenv("CONTA_CORRENTE")

POCKETBASE_URL = os.getenv("POCKETBASE_URL")
PB_ADMIN_EMAIL = os.getenv("PB_ADMIN_EMAIL")
PB_ADMIN_PASSWORD = os.getenv("PB_ADMIN_PASSWORD")
COLLECTION_SICOOB = os.getenv("COLLECTION_SICOOB")
SYNC_INTERVAL_MINUTES = int(os.getenv("SYNC_INTERVAL_MINUTES"))

AUTH_URL = (
    "https://auth.sicoob.com.br/auth/realms/cooperado/protocol/openid-connect/token"
)
EXTRATO_URL = "https://api.sicoob.com.br/conta-corrente/v4/extrato/{mes}/{ano}"
AUTH_SCOPE = "cco_consulta cco_transferencias"