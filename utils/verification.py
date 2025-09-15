# NOME DO ARQUIVO: utils/verification.py
# REFACTOR: Lógica ajustada para ignorar a verificação se o comando for usado dentro de um grupo.

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatMemberStatus, ChatType
from telegram.error import BadRequest
from functools import wraps
from config import CANAL_ID_2

logger = logging.getLogger(__name__)

RESTRICTION_MSG = "🛡️ *Acesso Restrito*\n\nPara usar esta função, você precisa ser um membro ativo do nosso grupo de suporte."

async def is_user_member_in_support_group(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Verifica se um utilizador é membro do grupo de suporte principal (CANAL_ID_2)."""
    if not CANAL_ID_2:
        logger.error("CANAL_ID_2 não está definido na configuração para verificação.")
        return False
    try:
        chat_member = await context.bot.get_chat_member(chat_id=CANAL_ID_2, user_id=user_id)
        return chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        logger.error(f"Erro ao verificar membro {user_id} no grupo {CANAL_ID_2}: {e}")
        return False

def group_member_required(func):
    """
    Decorator que restringe o acesso.
    - Se o comando for usado num grupo, permite o acesso.
    - Se o comando for usado em privado, verifica se o utilizador pertence ao grupo de suporte.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat
        if not user or not chat:
            return

        # Se o comando for executado dentro de um grupo ou supergrupo, ignora a verificação.
        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            return await func(update, context, *args, **kwargs)

        # Se for numa conversa privada, verifica se o utilizador é membro do grupo de suporte.
        if await is_user_member_in_support_group(user.id, context):
            return await func(update, context, *args, **kwargs)
        else:
            logger.warning(f"Acesso negado para o utilizador {user.id} (não membro) ao handler {func.__name__} em chat privado.")
            await context.bot.send_message(
                chat_id=chat.id,
                text=RESTRICTION_MSG,
                parse_mode=ParseMode.MARKDOWN
            )
    return wrapper