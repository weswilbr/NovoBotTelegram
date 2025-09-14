# NOME DO ARQUIVO: config.py
# REFACTOR: Centraliza a configuração do bot a partir de variáveis de ambiente.

import os
from dotenv import load_dotenv
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega as variáveis de ambiente do arquivo .env
# Isso é ideal para desenvolvimento local. Em produção, as variáveis devem ser setadas diretamente no ambiente.
load_dotenv()

# --- Carregamento das Variáveis de Ambiente ---
# Usar .getenv() é seguro, pois retorna None se a variável não existir.
BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
CANAL_ID_2_STR: str | None = os.getenv("CANAL_ID_2")
ADMIN_USER_IDS_STR: str | None = os.getenv("ADMIN_USER_IDS")
DATABASE_URL: str | None = os.getenv("DATABASE_URL")
KV_URL: str | None = os.getenv("KV_URL") # Adicionado para o tracker

# --- Validação e Processamento das Configurações ---
# É uma prática crucial validar as configurações antes de o bot iniciar.

# 1. Validação do Token do Bot (obrigatório)
if not BOT_TOKEN:
    logger.critical("ERRO DE CONFIGURAÇÃO: A variável BOT_TOKEN não foi definida.")
    raise ValueError("ERRO DE CONFIGURAÇÃO: A variável BOT_TOKEN não foi definida no ambiente ou no arquivo .env.")

# 2. Validação da URL do Banco de Dados (opcional, mas recomendado)
if not DATABASE_URL:
    logger.warning("AVISO DE CONFIGURAÇÃO: A variável DATABASE_URL não foi definida.")

# 3. Validação da URL do Vercel KV (opcional, mas recomendado para o tracker)
if not KV_URL:
    logger.warning("AVISO DE CONFIGURAÇÃO: A variável KV_URL não foi definida. O tracker de uso não funcionará com persistência.")

# 4. Validação e conversão do ID do Canal (obrigatório e deve ser numérico)
CANAL_ID_2: int = 0  # Inicializa com um valor padrão
if not CANAL_ID_2_STR:
    logger.critical("ERRO DE CONFIGURAÇÃO: A variável CANAL_ID_2 não foi definida.")
    raise ValueError("ERRO DE CONFIGURAÇÃO: A variável CANAL_ID_2 não foi definida no ambiente ou no arquivo .env.")
try:
    CANAL_ID_2 = int(CANAL_ID_2_STR)
except ValueError:
     logger.critical(f"ERRO DE CONFIGURAÇÃO: CANAL_ID_2 ('{CANAL_ID_2_STR}') deve ser um número inteiro.")
     raise ValueError(f"ERRO DE CONFIGURAÇÃO: CANAL_ID_2 ('{CANAL_ID_2_STR}') deve ser um número inteiro.")

# 5. Validação e conversão dos IDs de Administrador (opcional)
# Espera-se uma string de números separados por vírgula, ex: "12345,67890"
ADMIN_USER_IDS: list[int] = []
if ADMIN_USER_IDS_STR:
    try:
        # .strip() remove espaços em branco antes ou depois dos IDs
        ADMIN_USER_IDS = [int(user_id.strip()) for user_id in ADMIN_USER_IDS_STR.split(",")]
    except (ValueError, TypeError):
        logger.error(f"ERRO DE CONFIGURAÇÃO: ADMIN_USER_IDS ('{ADMIN_USER_IDS_STR}') está mal formatado.")
        # Opcional: pode querer levantar um erro aqui dependendo da criticidade
        # raise ValueError(...)
else:
    logger.info("Nenhum ADMIN_USER_IDS foi definido na configuração.")
