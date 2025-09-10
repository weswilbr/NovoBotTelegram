# features/business/reading_guide.py
import logging
from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps

# Placeholders
def group_member_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs): return await func(*args, **kwargs)
    return wrapper
def command_rate_limit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs): return await func(*args, **kwargs)
    return wrapper

logger = logging.getLogger(__name__)

@group_member_required
@command_rate_limit
async def leitura(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informa o usuário que o guia de leitura está em manutenção."""
    await update.message.reply_text(
        "⚠️ *O Guia de Desenvolvimento está em manutenção.*\n\n"
        "Uma nova versão será disponibilizada em breve. Agradecemos a sua compreensão.",
        parse_mode='Markdown'
    )
    logger.info(f"Usuário {update.effective_user.id} informado sobre a manutenção do Guia.")
