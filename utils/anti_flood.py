# NOME DO ARQUIVO: utils/anti_flood.py
# REFACTOR: Decorators para limitar a taxa de uso de comandos e cliques.
import time
import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from functools import wraps

logger = logging.getLogger(__name__)

user_last_command_time = {}
user_last_click_time = {}
COMMAND_LIMIT_SECONDS = 3
CLICK_LIMIT_SECONDS = 2

def command_rate_limit(func):
    """Decorator para limitar a frequência de comandos por usuário."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.effective_user: return
        user_id = update.effective_user.id
        current_time = time.time()
        
        last_time = user_last_command_time.get(user_id, 0)
        if current_time - last_time < COMMAND_LIMIT_SECONDS:
            logger.warning(f"Comando de {user_id} bloqueado por rate limit.")
            return # Ignora silenciosamente
        
        user_last_command_time[user_id] = current_time
        return await func(update, context, *args, **kwargs)
    return wrapper

async def check_flood(update: Update) -> bool:
    """Verifica se o usuário está clicando em botões rápido demais."""
    if not (update.callback_query and update.effective_user): return False
    
    query = update.callback_query
    user_id = update.effective_user.id
    current_time = time.time()
    
    last_time = user_last_click_time.get(user_id, 0)
    if current_time - last_time < CLICK_LIMIT_SECONDS:
        remaining = int(CLICK_LIMIT_SECONDS - (current_time - last_time))
        try:
            await query.answer(f"⌛ Por favor, aguarde {remaining}s.", show_alert=True)
        except TelegramError as e:
            logger.warning(f"Erro ao enviar alerta de flood: {e}")
        return False
        
    user_last_click_time[user_id] = current_time
    return True

