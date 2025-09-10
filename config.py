# NOME DO ARQUIVO: config.py
# REFACTOR: Centraliza a configuração do bot a partir de variáveis de ambiente.
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID_2 = os.getenv("CANAL_ID_2")
ADMIN_USER_IDS = os.getenv("ADMIN_USER_IDS")
DATABASE_URL = os.getenv("DATABASE_URL")


if not BOT_TOKEN:
    raise ValueError("CONFIG ERROR: BOT_TOKEN is not defined in environment variables or .env file.")

if not CANAL_ID_2:
    raise ValueError("CONFIG ERROR: CANAL_ID_2 is not defined in environment variables or .env file.")

if not DATABASE_URL:
    raise ValueError("CONFIG ERROR: DATABASE_URL is not defined in environment variables or .env file.")

try:
    CANAL_ID_2 = int(CANAL_ID_2)
except ValueError:
     raise ValueError("CONFIG ERROR: CANAL_ID_2 must be an integer.")

if ADMIN_USER_IDS:
    try:
        ADMIN_USER_IDS = [int(user_id.strip()) for user_id in ADMIN_USER_IDS.split(",")]
    except ValueError:
        raise ValueError("CONFIG ERROR: ADMIN_USER_IDS must be a comma-separated list of integer IDs.")
else:
    ADMIN_USER_IDS = []

