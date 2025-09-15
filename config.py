# NOME DO ARQUIVO: config.py
import os
from dotenv import load_dotenv
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Carregamento das Variáveis de Ambiente ---
BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
CANAL_ID_2_STR: str | None = os.getenv("CANAL_ID_2")
ADMIN_USER_IDS_STR: str | None = os.getenv("ADMIN_USER_IDS")

# --- Validação e Processamento das Configurações ---

# 1. Validação do Token do Bot (obrigatório)
if not BOT_TOKEN:
    logger.critical("ERRO DE CONFIGURAÇÃO: A variável BOT_TOKEN não foi definida.")
    raise ValueError("ERRO DE CONFIGURAÇÃO: A variável BOT_TOKEN não foi definida no ambiente ou no arquivo .env.")

# 2. Validação e conversão do ID do Canal (obrigatório e deve ser numérico)
CANAL_ID_2: int = 0
if not CANAL_ID_2_STR:
    logger.critical("ERRO DE CONFIGURAÇÃO: A variável CANAL_ID_2 não foi definida.")
    raise ValueError("ERRO DE CONFIGURAÇÃO: A variável CANAL_ID_2 não foi definida no ambiente ou no arquivo .env.")
try:
    CANAL_ID_2 = int(CANAL_ID_2_STR)
except ValueError:
    logger.critical(f"ERRO DE CONFIGURAÇÃO: CANAL_ID_2 ('{CANAL_ID_2_STR}') deve ser um número inteiro.")
    raise ValueError(f"ERRO DE CONFIGURAÇÃO: CANAL_ID_2 ('{CANAL_ID_2_STR}') deve ser um número inteiro.")

# 3. Validação e conversão dos IDs de Administrador (opcional)
ADMIN_USER_IDS: list[int] = []
if ADMIN_USER_IDS_STR:
    try:
        ADMIN_USER_IDS = [int(user_id.strip()) for user_id in ADMIN_USER_IDS_STR.split(",")]
    except (ValueError, TypeError):
        logger.error(f"ERRO DE CONFIGURAÇÃO: ADMIN_USER_IDS ('{ADMIN_USER_IDS_STR}') está mal formatado.")
else:
    logger.info("Nenhum ADMIN_USER_IDS foi definido na configuração.")