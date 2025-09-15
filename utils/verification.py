import logging
from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps

logger = logging.getLogger(__name__)

CHAT_ID = -1002246574064  # substitua pelo ID do seu grupo

def group_member_required(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        try:
            member = await context.bot.get_chat_member(CHAT_ID, user_id)
            if member.status in ["member", "administrator", "creator"]:
                return await func(update, context, *args, **kwargs)
            else:
                if update.message:
                    await update.message.reply_text("⚠️ Acesso negado: apenas membros do grupo podem usar este comando.")
        except Exception as e:
            logger.error(f"Erro ao verificar membro {user_id} no grupo {CHAT_ID}: {e}")
            if update.message:
                await update.message.reply_text("⚠️ Erro ao verificar sua participação no grupo.")
        return None
    return wrapper
