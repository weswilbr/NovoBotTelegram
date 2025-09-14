# NOME DO ARQUIVO: utils/monitoring/decorators.py
# FEATURE: Decorador para rastrear o uso de comandos automaticamente.

from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from .tracker import UsageTracker

def track_command_usage(func):
    """
    Decorador que rastreia o uso de um comando antes de executá-lo.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        tracker: UsageTracker = context.bot_data.get("usage_tracker")
        user = update.effective_user

        if tracker and user:
            # Chama o tracker passando o ID e o nome do usuário
            tracker.track_usage(user_id=user.id, first_name=user.first_name)
        
        # Executa a função original do comando (ex: start, ajuda, etc.)
        return await func(update, context, *args, **kwargs)
    
    return wrapper