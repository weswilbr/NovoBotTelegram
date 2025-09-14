# NOME DO ARQUIVO: config.py
# REFACTOR: Carrega .env apenas localmente e lê variáveis da Vercel em produção.

import os

# --- Lógica para carregar o .env apenas em ambiente de desenvolvimento ---
# A Vercel define a variável 'VERCEL_ENV'. Se ela existir, não carregamos o .env.
if "VERCEL_ENV" not in os.environ:
    from dotenv import load_dotenv
    print("INFO: Ambiente local detectado. Carregando variáveis do arquivo .env")
    load_dotenv()
# --------------------------------------------------------------------

BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_ID_2 = os.getenv("CANAL_ID_2")
ADMIN_USER_IDS = os.getenv("ADMIN_USER_IDS")

# As verificações abaixo estão perfeitas e devem ser mantidas.
# Elas garantirão que você receba um erro claro se esquecer de configurar
# as variáveis no painel da Vercel.

if not BOT_TOKEN:
    raise ValueError("CONFIG ERROR: BOT_TOKEN is not defined in environment variables or .env file.")

if not CANAL_ID_2:
    raise ValueError("CONFIG ERROR: CANAL_ID_2 is not defined in environment variables or .env file.")

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